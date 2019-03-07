#-----ENB Related code-------------

def ENB_Bringup():
    prompt = ['# ', pexpect.EOF]
    fout = open('../Logs/Board.log', 'wb')
    try:
        #logging into board
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enbconfig.ENB_IP,
                logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(enbconfig.ENB_PASS)
        child.expect(prompt, timeout=30)
        logger.debug('Board login successful')
        child.sendline('rm -r rsys')
        child.expect(prompt, timeout=30)
        logger.debug('deleted existing binaries on board')
        #copying binaries to the board
        cmd = "scp -r " + enbconfig.COPY_RSYS_PATH + " /root/"
        child.sendline(cmd)
        child.expect('(?i)password:',timeout=30)
        child.sendline(epcconfig.EPC_PASS)
        child.expect(prompt, timeout=30)
        logger.debug('copied rsys')
        child.sendline('umount /mnt/firmware')
        child.expect(prompt, timeout=30)
        child.sendline('mount -t vfat /dev/mmcblk0p1 /mnt/firmware/')
        child.expect(prompt, timeout=30)
        child.sendline('cp -f /root/rsys/bin/mdm2_00.mbn /mnt/firmware')
        child.expect(prompt, timeout=30)
        #configuration file changes
        
        child.sendline('exit')
        #OAM related Changes
        if enbconfig.OAM == "YES":
            logger.info('OAM configuration')
            OAM_Configurations()
        #logging into board
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enbconfig.ENB_IP,
                                        logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(enbconfig.ENB_PASS)
        child.expect(prompt, timeout=30)
        #Bringup Board
        child.sendline('cd ' + enbconfig.SCRIPT_PATH)
        child.expect(prompt, timeout=30)
        child.sendline('./install.sh')
        child.expect(prompt, timeout=30)
        child.sendline('./start_TeNB.sh > TeNB_console.log 2>&1 &')
        child.expect(prompt, timeout=30)
        time.sleep(40)
        child.sendline('tail -f TeNB_console.log')
        child.expect("address", timeout=50)
        logger.debug("EPC To ENB Connection is successfull")
        #Cell related changes
        Cell_Configuration()
        #child.sendline('tail -f TeNB_console.log')
        #ret = child.expect("THROUGHPUT DATA",timeout=60)
        #if ret == 0:
        #    logger.debug("EPC To ENB Connection is successfull")
        #if ret == 1:
        #    raise RuntimeError("EPC To ENB Connection is Not Found")
    except Exception as err:
        logger.error('Error in Bringing up Board' + str(err))

def OAM_Configurations():
    fout = open('../Logs/Board.log', 'a')
    logger.info("Inside OAM Configurations")
    try:
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enbconfig.ENB_IP,
                                logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(enbconfig.ENB_PASS)
        child.expect('# ', timeout=30)
        cmd = "grep 'LTE_SIGLINK_SERVER_LIST' "+ enbconfig.CONFIG_FILE + " | awk '{print $2}'"
        child.sendline(cmd)
        child.readline()
        current_ip = child.readline()
        logger.info(current_ip)
        if current_ip != epcconfig.EPC_IP:
            cmd = "sed -i 's/"+ current_ip.rstrip() +"/\""+ epcconfig.EPC_IP+"\"/g' " + enbconfig.CONFIG_FILE
            child.sendline(cmd)
            child.expect('# ', timeout=30)
            child.sendline('sync')
            child.expect('# ', timeout=30)
            child.sendline('reboot')
            time.sleep(30)
    except Exception as err:
            logger.error('Error in OAM Configurations' + str(err))

def Cell_Configuration():
    fout = open('../Logs/Board.log', 'a')
    try:
        logger.info('cell configurations')
        #CELL configuration
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enbconfig.ENB_IP,
                logfile=fout)  
        child.expect('(?i)password', timeout=10)
        child.sendline(enbconfig.ENB_PASS)
        child.expect('# ',timeout=30)
        child.sendline('cd ' + enbconfig.CLI_PATH)
        child.expect('# ',timeout=30)
        if enbconfig.CELL == "Single_Cell":
            child.sendline('./cli')
            child.expect("fap",timeout=30)
            child.sendline('tr69.addobject Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.Enable 1')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.FAPControl.LTE.AdminState 1')
            child.expect("fap", timeout=30)
        elif enbconfig.CELL == "CA":
            child.sendline('./cli')
            child.expect("fap",timeout=30)
            child.sendline('tr69.addobject Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.CellReservedForOperatorUse 1')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.Enable 1')
            child.expect("fap", timeout=30)
            child.sendline('tr69.addobject Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.CellReservedForOperatorUse 1')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.Enable 1')
            child.expect("fap", timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.FAPControl.LTE.AdminState 1')
            child.expect("fap", timeout=30)
        child.sendline('exit')
    except Exception as err:
        logger.error('Error in Cell Configurations' + str(err))
        
def Clean_ENB():
    fout = open('../Logs/Board.log', 'a')
    try:
        logger.debug('cleaning Board configurations')
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enbconfig.ENB_IP,
                            logfile=fout)
        child.expect('(?i)password', timeout=10)
        child.sendline(enbconfig.ENB_PASS)
        child.expect('# ',timeout=30)
        child.sendline('cd ' + enbconfig.SCRIPT_PATH)
        child.expect('# ', timeout=30)
        child.sendline('./stop_TeNB.sh')
        child.expect('# ', timeout=30)
        child.sendline('sync')
        child.expect('# ', timeout=30)
        child.sendline('reboot')
        time.sleep(30)
    except Exception as err:
        logger.error('Error in Cell Configurations' + str(err))

