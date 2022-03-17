"""
NOTE: All lines commented with #* can be un-commented when deploying. They are commented to allow testing without a physical device
"""
import logging
from dataclasses import dataclass
from typing import List

from caproto import ChannelType
from caproto.server import PVGroup, SubGroup, ioc_arg_parser, pvproperty, run
import pyvisa
from humanfriendly.text import dedent

from fccd_psu_ioc.utils import power_on, configure, power_off

rm = pyvisa.ResourceManager()
com_lock = None


logger = logging.getLogger('caproto')


@dataclass
class PSUChannel:
    name: str
    voltage: int
    doc: str = ''
    voltage_pv: pvproperty = None
    current_pv: pvproperty = None


class _PSUChannel(PVGroup):
    Voltage = pvproperty(dtype=float, precision=4, units='V', read_only=True)
    Current = pvproperty(dtype=float, precision=4, units='A', read_only=True)


class PSU(PVGroup):
    resource_path = pvproperty(dtype=str)

    def __init__(self, prefix, resource_path: str, channels: List[PSUChannel], **kwargs):
        self.resource = rm.open_resource(resource_path)

        super(PSU, self).__init__(prefix, **kwargs)

        self.resource_path.pvspec._replace(value=resource_path)
        self.channels = channels

        for channel in channels:
            pv_path = prefix + channel.name + ':'
            channel_group = _PSUChannel(pv_path)
            self.pvdb.update(channel_group.pvdb)

    @resource_path.scan(period=3)
    async def resource_path(self, instance, async_lib):
        async with com_lock:
            for i, channel in enumerate(self.channels):
                self.resource.write(f'INST:NSEL {i + 1} \n')
                voltage = float(self.resource.query('MEAS:VOLT? \n'))
                current = float(self.resource.query('MEAS:CURR? \n'))
                await self.pvdb[self.prefix + channel.name + ':Voltage'].write(voltage)
                await self.pvdb[self.prefix + channel.name + ':Current'].write(current)


class PSUs(PVGroup):
    """

    """
    bias_clocks_psu = SubGroup(PSU,
                        prefix='BiasClocksPSU:',
                        resource_path='ASRL/dev/biasnclk::INSTR',  # NOTE: This path is MISLABELED, it is actually the bias and clocks
                        channels=[PSUChannel('Out1', 15),
                                  PSUChannel('Out2', 15),
                                  PSUChannel('Out3', 30),
                                  PSUChannel('Out4', 30)])

    fcric_fops_psu = SubGroup(PSU,
                          prefix='FCRICFOPSPSU:',
                          resource_path='ASRL/dev/fcricnfopt::INSTR',  # NOTE: This path is MISLABELED, it is actually the FCRIC and FOPS
                          channels=[PSUChannel('Out1', 5),
                                    PSUChannel('Out2', 4)])

    def __init__(self, *args, **kwargs):
        self.async_lib = None
        super(PSUs, self).__init__(*args, **kwargs)
        self.pvdb.update(self.bias_clocks_psu.pvdb)
        self.pvdb.update(self.fcric_fops_psu.pvdb)

    State = pvproperty(dtype=ChannelType.ENUM,
                       enum_strings=["Unknown", "On", "Powering On...", "Powering Off...", "Off", ],
                       value="Unknown")

    @State.startup
    async def State(self, instance, async_lib):
        global com_lock
        self.async_lib = async_lib
        com_lock = async_lib.library.locks.Lock()

    @State.putter
    async def State(self, instance, value):
        if value != instance.value:
            logger.debug(f"setting state: {value}")

            if value == "Powering On...":
                value = await self._power_on(None, None)

            elif value == "Powering Off...":
                value = await self._power_off(None, None)

        return value

    async def _power_on(self, instance, value):
        async with com_lock:
            configure(self.bias_clocks_psu.resource, self.fcric_fops_psu.resource)
            power_on(self.bias_clocks_psu.resource, self.fcric_fops_psu.resource)
            await self.async_lib.library.sleep(1)
            logger.debug(f"Powered On")
            return 'On'

    async def _power_off(self, instance, value):
        async with com_lock:
            power_off(self.bias_clocks_psu.resource, self.fcric_fops_psu.resource)
            await self.async_lib.library.sleep(1)
            logger.debug(f"Powered Off")
            return 'Off'

    async def power_on(self, instance, value):
        await self.State.write('Powering On...')

    async def power_off(self, instance, value):
        await self.State.write('Powering Off...')

    On = pvproperty(value=0, dtype=int, put=power_on)
    Off = pvproperty(value=0, dtype=int, put=power_off)


def main():
    """Console script for fccd_psu_ioc."""

    ioc_options, run_options = ioc_arg_parser(
        default_prefix='ES7011:FastCCD:',
        desc=dedent(PSUs.__doc__))
    ioc = PSUs(**ioc_options)
    run(ioc.pvdb, **run_options)

    return 0


if __name__ == '__main__':
    main()
