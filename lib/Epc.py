import paramiko
import fileinput
import os
import json
import sys
import time
import pexpect
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
sys.path.append('../config/')
import config



#-----------EPC Related code--------------------


def EPC_Bringup():
    prompt = ['#', pexpect.EOF]
    fout = open('../Logs/EPC.log', 'a')
    try:
    #logging into EPC
        logger.info("login into EPC")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.EPC_IP,
                        logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.EPC_PASS)
        child.expect("# ",timeout=30)
        logger.debug('EPC login successful')
        #configfile changes
        cmd = "sed -i 's/MCC=.*/MCC=" +config.MCC+ "/' " + config.EPC_CONFIG_FILE
        logger.info(cmd)
        child.sendline(cmd)
        child.expect("# ",timeout=30)
        cmd = "sed -i 's/MNC=.*/MNC=" + config.MNC + "/' " + config.EPC_CONFIG_FILE
        logger.info(cmd)
        child.sendline(cmd)
        child.expect("# ",timeout=30)
        one=1
        cmd = "sed -n 's/PGW-IP=\(.*\)/\%d/p' < "% (one)
        child.sendline(cmd + config.EPC_CONFIG_FILE)
        child.readline()
        pgw = child.readline()
        config.pgw = pgw.rstrip()
        logger.info(config.pgw)
        #child.expect(prompt,timeout=30)
        time.sleep(5)
        #Restartcne
        child.sendline('cd ' + config.CNE_PATH)
        child.expect('# ',timeout=30)
        child.sendline('./restart_cne.sh 1 > restartcne.log 2>&1 &')
        child.expect("# ",timeout=30)
        child.sendline('tail -f restartcne.log')
        child.expect("Automation Started",timeout=100)
        logger.debug("restarted cne service successfully")
        child.sendline('exit')
    except Exception as err:
        logger.error('Error in EPC Bring up' + str(err))


def Clean_EPC():
    prompt = ['#', pexpect.EOF]
    fout = open('../Logs/EPC.log', 'wb')
    try:
        #logging into EPC
        logger.info("cleaning EPC")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.EPC_IP,
                                                                    logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.EPC_PASS)
        logger.info('EPC login successful in clean up')
        #kill the running process
        child.sendline('pkill -9 mme_app')
        child.expect("# ", timeout=30)
        child.sendline('pkill -9 sgw_app')
        child.expect("# ", timeout=30)
        child.sendline('pkill -9 pgw_app')
        child.expect("# ", timeout=30)
        child.sendline('pkill -9 hss_app')
        child.expect("# ", timeout=30)
        child.sendline('pkill -9 pcrf_app')
        child.expect("# ", timeout=30)
        child.sendline('exit')
    except Exception as err:
        logger.error('Error in EPC clean up' + str(err))

def EPC_Teardown():
    Clean_EPC()
    prompt = ['#', pexpect.EOF]
    fout = open('../Logs/EPC.log', 'wb')
    try:
        #logging into EPC
        logger.info("login into EPC")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.EPC_IP,
                        logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.EPC_PASS)
        child.sendline('kill -9 restart_cne.sh')
        child.expect(prompt, timeout=30)
    except Exception as err:
        logger.error('Error while EPC Teardown' + str(err))

