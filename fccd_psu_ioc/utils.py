import logging

logger = logging.getLogger('caproto')


def power_on(resource0, resource1):
    logger.debug("Powering on FCCD Camera")
    resource0.write('OUTP:GEN 1 \n')
    resource1.write('OUTP:GEN 1 \n')


def power_off(resource0, resource1):
    logger.debug("Powering off FCCD Camera")
    resource0.write('OUTP:GEN 0 \n')
    resource1.write('OUTP:GEN 0 \n')


def configure(resource0, resource1):
    """resource0 is the bias and clocks; resource1 is the fcirc and fops"""
    configure_bias_clocks(resource0)
    configure_fcric_fops(resource1)


def configure_bias_clocks(resource0):
    logger.debug("******  Configuration of 4V/30V/30V FCCD Power Supplies  ******")

    resource0.write('OUTP:GEN 0 \n')
    ## Output 1 (Clocks 15VA)
    resource0.write('INST:NSEL 1 \n')
    resource0.write('OUTP:SEL 1 \n')
    resource0.write('APPL 15.0,1.0 \n')  # V=15.0, I=1.0
    resource0.write('SOUR:VOLT:PROT 15.5 \n')
    resource0.write('SOUR:VOLT:STEP 0.2 \n')
    volt = float(resource0.query('SOUR:VOLT? \n'))
    curr = float(resource0.query('SOUR:CURR? \n'))
    vpro = float(resource0.query('SOUR:VOLT:PROT? \n'))
    logger.debug('Out2 Set: %.4fV, %.4fA, %.4fV-OVP' % (volt, curr, vpro))

    ## Output 2 (Clocks 15VA)
    resource0.write('INST:NSEL 2 \n')
    resource0.write('OUTP:SEL 1 \n')
    resource0.write('APPL 15.0,1 \n')  # V=15.0, I=1.0
    resource0.write('SOUR:VOLT:PROT 15.5 \n')
    resource0.write('SOUR:VOLT:STEP 0.2 \n')
    volt = float(resource0.query('SOUR:VOLT? \n'))
    curr = float(resource0.query('SOUR:CURR? \n'))
    vpro = float(resource0.query('SOUR:VOLT:PROT? \n'))
    logger.debug('Out3 Set: %.4fV, %.4fA, %.4fV-OVP' % (volt, curr, vpro))

    ## Output 3 (Clocks 30VA)
    resource0.write('INST:NSEL 3 \n')
    resource0.write('OUTP:SEL 1 \n')
    resource0.write('APPL 30.0,1.0 \n')  # V=30.0, I=1.0
    resource0.write('SOUR:VOLT:PROT 30.5 \n')
    resource0.write('SOUR:VOLT:STEP 0.2 \n')
    volt = float(resource0.query('SOUR:VOLT? \n'))
    curr = float(resource0.query('SOUR:CURR? \n'))
    vpro = float(resource0.query('SOUR:VOLT:PROT? \n'))
    logger.debug('Out2 Set: %.4fV, %.4fA, %.4fV-OVP' % (volt, curr, vpro))

    ##Output 4 (Clocks 30VA)
    resource0.write('INST:NSEL 4 \n')
    resource0.write('OUTP:SEL 1 \n')
    resource0.write('APPL 30.0,1 \n')  # V=30.0, I=1.0
    resource0.write('SOUR:VOLT:PROT 30.5 \n')
    resource0.write('SOUR:VOLT:STEP 0.2 \n')
    volt = float(resource0.query('SOUR:VOLT? \n'))
    curr = float(resource0.query('SOUR:CURR? \n'))
    vpro = float(resource0.query('SOUR:VOLT:PROT? \n'))
    logger.debug('Out3 Set: %.4fV, %.4fA, %.4fV-OVP' % (volt, curr, vpro))


def configure_fcric_fops(resource1):
    logger.debug("\n  ******  Configuration of 5V/15V/15V FCCD Power Supplies  ******  \n")

    ##  Set up HMP2030_0
    ## Output 2 (FCRIC 4.0V)
    resource1.write('INST:NSEL 2 \n')
    resource1.write('OUTP:SEL 1 \n')
    resource1.write('APPL 4.0,2.5 \n')  # V=4.0, I=2.5
    resource1.write('SOUR:VOLT:PROT 4.5 \n')
    resource1.write('SOUR:VOLT:STEP 0.2 \n')
    volt = float(resource1.query('SOUR:VOLT? \n'))
    curr = float(resource1.query('SOUR:CURR? \n'))
    vpro = float(resource1.query('SOUR:VOLT:PROT? \n'))
    logger.debug('Out1 Set: %.4fV, %.4fA, %.4fV-OVP' % (volt, curr, vpro))

    ##  Set up HMP2030_0
    ## Output 1 (FIBOPT 5.0V)
    resource1.write('INST:NSEL 1 \n')
    resource1.write('OUTP:SEL 1 \n')
    resource1.write('APPL 5.0,8.0 \n')  # V=5.0, I=2.5
    resource1.write('SOUR:VOLT:PROT 5.5 \n')
    resource1.write('SOUR:VOLT:STEP 0.2 \n')
    volt = float(resource1.query('SOUR:VOLT? \n'))
    curr = float(resource1.query('SOUR:CURR? \n'))
    vpro = float(resource1.query('SOUR:VOLT:PROT? \n'))
    logger.debug('Out1 Set: %.4fV, %.4fA, %.4fV-OVP' % (volt, curr, vpro))
