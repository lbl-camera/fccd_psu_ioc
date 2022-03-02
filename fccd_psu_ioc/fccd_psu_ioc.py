from caproto.server import PVGroup, SubGroup, get_pv_pair_wrapper, ioc_arg_parser, pvproperty, run
import pyvisa

from . import pvproperty_with_rbv


rm = pyvisa.ResourceManager()

hmp2030_0_address = 'ASRL/dev/fcricps::INSTR'
hmp2030_1_address = 'ASRL/dev/fiboptps::INSTR'

hmp2030_0 = rm.open_resource(hmp2030_0_address)
hmp2030_1 = rm.open_resource(hmp2030_1_address)

## Output 2 (FCRIC 4.0V)
hmp2030_1.write('INST:NSEL 2 \n')
hmp2030_1.write('OUTP:SEL 1 \n')
hmp2030_1.write('APPL 4.0,2.5 \n')  # V=4.0, I=2.5
hmp2030_1.write('SOUR:VOLT:PROT 4.5 \n')
hmp2030_1.write('SOUR:VOLT:STEP 0.2 \n')
volt = float(hmp2030_1.query('SOUR:VOLT? \n'))
curr = float(hmp2030_1.query('SOUR:CURR? \n'))
vpro = float(hmp2030_1.query('SOUR:VOLT:PROT? \n'))
print ('Out1 Set: %.4fV, %.4fA, %.4fV-OVP' %(volt, curr, vpro))


class FCCDPowerSupply(PVGroup):

    @SubGroup(prefix='psu1:')
    class PSU1(PVGroup):
        FCRICVoltage = pvproperty(dtype=float, doc='FCRIC Voltage', precision=4, units='V')
        FCRICCurrent = pvproperty(dtype=float, doc='FCRIC Current', precision=4, units='A')
        FCRICVoltageOVP = pvproperty(dtype=float, doc='FCRIC Voltage OVP', precision=4, units='V')
        FIBOPTVoltage = pvproperty(dtype=float, doc='FIBOPT Voltage', precision=4, units='V')
        FIBOPTCurrent = pvproperty(dtype=float, doc='FIBOPT Current', precision=4, units='A')
        FIBOPTVoltageOVP = pvproperty(dtype=float, doc='FIBOPT Voltage OVP', precision=4, units='V')

        @FCRICVoltage.getter
        async def FCRICVoltage(self, instance, async_lib):
            hmp2030_1.write('INST:NSEL 2 \n')
            return hmp2030_1.query('MEAS:VOLT? \n')

        @FCRICCurrent.getter
        async def FCRICCurrent(self, instance, async_lib):
            hmp2030_1.write('INST:NSEL 2 \n')
            return hmp2030_1.query('MEAS:CURR? \n')

        @FIBOPTVoltage.getter
        async def FIBOPTVoltage(self, instance, async_lib):
            hmp2030_1.write('INST:NSEL 1 \n')
            hmp2030_1.query('MEAS:VOLT? \n')

        @FIBOPTVoltage.getter
        async def FIBOPTCurrent(self, instance, async_lib):
            hmp2030_1.write('INST:NSEL 1 \n')
            hmp2030_1.query('MEAS:CURR? \n')

    @SubGroup(prefix='psu2:')
    class PSU2(PVGroup):
        Out1Voltage = pvproperty(dtype=float, doc='Out1 (15V) Voltage', precision=4, units='V')
        Out1Current = pvproperty(dtype=float, doc='Out1 (15V) Current', precision=4, units='A')

        Out2Voltage = pvproperty(dtype=float, doc='Out2 (15V) Voltage', precision=4, units='V')
        Out2Current = pvproperty(dtype=float, doc='Out2 (15V) Current', precision=4, units='A')

        Out3Voltage = pvproperty(dtype=float, doc='Out3 (30V) Voltage', precision=4, units='V')
        Out3Current = pvproperty(dtype=float, doc='Out3 (30V) Current', precision=4, units='A')

        Out4Voltage = pvproperty(dtype=float, doc='Out4 (30V) Voltage', precision=4, units='V')
        Out4Current = pvproperty(dtype=float, doc='Out4 (30V) Current', precision=4, units='A')

def main():
    """Console script for fccd_psu_ioc."""

    ioc_options, run_options = ioc_arg_parser(
        default_prefix='ES7011:FastCCD:',
        desc=dedent(FCCDPowerSupply.__doc__))
    ioc = FCCDPowerSupply(**ioc_options)
    #run(ioc.pvdb, **run_options)

    return 0
