import imports


#-----------EPC Related code--------------------


def EPC_Bringup():
    prompt = ['#', pexpect.EOF]
    fout = open('../Logs/EPC.log', 'wb')
    try:
    #logging into EPC
        logger.info("login into EPC")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.EPC_IP,
                        logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.EPC_PASS)
        logger.debug('EPC login successful')
        #configfile changes
        child.sendline('cd' + config.EPC_CONFIG_FILE)
        child.expect(prompt,timeout=30)
        cmd = "sed -i 's/MCC=.*MCC=" + config.MCC + "/' " + config.EPC_CONFIG_FILE
        child.sendline(cmd)
        child.expect(prompt,timeout=30)
        cmd = "sed -i 's/MNC=.*MNC=" + config.MNC + "/' " + config.EPC_CONFIG_FILE
        child.sendline(cmd)
        child.expect(prompt,timeout=30)
        #Restartcne
        child.sendline('./restart_cne.sh 1 > restartcne.log 2>&1 &')
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
        logger.info("login into EPC")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.EPC_IP,
                                                                    logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.EPC_PASS)
        logger.debug('EPC login successful')
        #kill the running process
        child.sendline('kill -9 mme_app')
        child.expect(prompt, timeout=30)
        child.sendline('kill -9 sgw_app')
        child.expect(prompt, timeout=30)
        child.sendline('kill -9 pgw_app')
        child.expect(prompt, timeout=30)
        child.sendline('kill -9 hss_app')
        child.expect(prompt, timeout=30)
        child.sendline('kill -9 pcrf_app')
        child.expect(prompt, timeout=30)
    except Exception as err:
        logger.error('Error in EPC clean up' + str(err))

def EPC_Teardown():
    Clean_EPC()
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

