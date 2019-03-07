#-----------EPC Related code--------------------


def EPC_Bringup():
    prompt = ['#', pexpect.EOF]
    fout = open('../Logs/EPC.log', 'wb')
    try:
    #logging into EPC
        logger.info("login into EPC")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + epcconfig.EPC_IP,
                        logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(epcconfig.EPC_PASS)
        logger.debug('EPC login successful')
        #configfile changes
        child.sendline('cd' + epcconfig.CONFIG_FILE)
        child.expect(prompt,timeout=30)
        cmd = "sed -i 's/MCC=.*MCC=" + epcconfig.MCC + "/' " + epcconfig.CONFIG_FILE
        child.sendline(cmd)
        child.expect(prompt,timeout=30)
        cmd = "sed -i 's/MNC=.*MNC=" + epcconfig.MNC + "/' " + epcconfig.CONFIG_FILE
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
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + epcconfig.EPC_IP,
                                                                    logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(epcconfig.EPC_PASS)
        logger.debug('EPC login successful')
        #kill the running process
    except Exception as err:
        logger.error('Error in EPC Bring up' + str(err))

