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
#-----ENB Related code-------------

def ENB_Bringup(OAM,Cell):
    prompt = ['# ', pexpect.EOF]
    fout = open('../Logs/Board.log', 'wb')
    try:
        #logging into board
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.ENB_IP,
                logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.ENB_PASS)
        child.expect(prompt, timeout=30)
        #clean_Board()
        logger.debug('Board login successful')
        child.sendline('rm -r rsys')
        child.expect(prompt, timeout=30)
        logger.debug('deleted existing binaries on board')
        #copying binaries to the board
        cmd = "scp -r " + config.COPY_RSYS_PATH + " /root/"
        child.sendline(cmd)
        child.expect('(?i)password:',timeout=30)
        child.sendline(config.EPC_PASS)
        child.expect(prompt, timeout=30)
        logger.debug('copied rsys')
        child.sendline('umount /mnt/firmware')
        child.expect(prompt, timeout=30)
        child.sendline('mount -t vfat /dev/mmcblk0p1 /mnt/firmware/')
        child.expect(prompt, timeout=30)
        child.sendline('cp -f '+config.CLI_PATH+ '/mdm2_00.mbn /mnt/firmware')
        child.expect(prompt, timeout=30)
        #OAM related Changes
        if OAM == "OAM":
            logger.info('OAM configuration')
            OAM_Configurations(Cell)
        else:
            #wr_cfg configuration file changes
            child.sendline('cd '+ config.SCRIPT_PATH)
            child.expect(prompt, timeout=30)
            child.sendline("sed -i 's/WR_TAG_NOS_OF_CELLS .*/WR_TAG_NOS_OF_CELLS "+cell+"/' wr_cfg.txt")
            child.expect('# ', timeout=30)
            child.sendline("sed -i 's/WR_TAG_ENABLE_CA .*/WR_TAG_ENABLE_CA "+cell+"/' wr_cfg.txt")
            child.expect('# ', timeout=30)
            child.sendline("sed -i 's/WR_TAG_MME_INFO_IP .*/WR_TAG_MME_INFO_IP "++config.EPC_IP++"/' wr_cfg.txt")
            child.expect('# ', timeout=30)
            child.sendline("sed -i 's/WR_TAG_ENB_IP_ADDR .*/WR_TAG_ENB_IP_ADDR "+config.ENB_IP+"/' wr_cfg.txt")
            child.expect('# ', timeout=30)
            child.sendline("sed -i 's/WR_TAG_SCTP_IP_ADDR .*/WR_TAG_SCTP_IP_ADDR "+config.ENB_IP+"/' wr_cfg.txt")
            child.expect('# ', timeout=30)
            child.sendline('sync')
            child.expect('# ', timeout=30)
            child.sendline('reboot')
        #logging into board
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.ENB_IP,
                                        logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.ENB_PASS)
        child.expect(prompt, timeout=30)
        #Bringup Board
        child.sendline('cd ' + config.SCRIPT_PATH)
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
        Cell_Configuration(Cell)
        #child.sendline('tail -f TeNB_console.log')
        #ret = child.expect("THROUGHPUT DATA",timeout=60)
        #if ret == 0:
        #    logger.debug("EPC To ENB Connection is successfull")
        #if ret == 1:
        #    raise RuntimeError("EPC To ENB Connection is Not Found")
    except Exception as err:
        logger.error('Error in Bringing up Board' + str(err))

def OAM_Configurations(Cell):
    fout = open('../Logs/Board.log', 'a')
    logger.info("Inside OAM Configurations")
    try:
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.ENB_IP,
                                logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.ENB_PASS)
        child.expect('# ', timeout=30)
        cmd = "grep 'LTE_SIGLINK_SERVER_LIST' "+ config.ENB_CONFIG_FILE + " | awk '{print $2}'"
        child.sendline(cmd)
        child.readline()
        current_ip = child.readline()
        logger.info(current_ip)
        if current_ip != config.EPC_IP:
            cmd = "sed -i 's/"+ current_ip.rstrip() +"/\""+ config.EPC_IP+"\"/g' " + config.ENB_CONFIG_FILE
            child.sendline(cmd)
            child.expect('# ', timeout=30)
        child.sendline('cd '+ config.CONFIG_PATH)
        child.expect(prompt, timeout=30)
        child.sendline("sed -i 's/OAM_NUM_CELL_ENTRIES .*/OAM_NUM_CELL_ENTRIES "+Cell+"/' configFile")
        child.expect('# ', timeout=30)
        child.sendline("grep LTE_X_RADISYS_NUM_OF_CELLS configFile | wc -l")
        count = child.readline().rstrip()
        if Cell == 1:
            child.sendline("sed -i 's/LTE_X_RADISYS_CA_ENABLE .*/LTE_X_RADISYS_CA_ENABLE 0/' configFile")
            child.expect(prompt, timeout=30)
            child.sendline("sed -i 's/LTE_X_RADISYS_NUM_OF_CELLS .*/LTE_X_RADISYS_NUM_OF_CELLS 1/' configFile")
            child.expect(prompt, timeout=30)
            elif count == 2:
                child.sendline("sed -e '/LTE_X_RADISYS_NUM_OF_CELLS 2 FAP.0.FAP_LTE.1/ s/^#*/#/' -i configFile")

        elif cell == 2:
            child.sendline("sed -i 's/LTE_X_RADISYS_CA_ENABLE .*/LTE_X_RADISYS_CA_ENABLE 1/' configFile")
            child.expect(prompt, timeout=30)
            child.sendline("sed -i 's/LTE_X_RADISYS_NUM_OF_CELLS .*/LTE_X_RADISYS_NUM_OF_CELLS 2/' configFile")
            child.expect(prompt, timeout=30)
            if count == 1:
                child.sendline('echo "LTE_X_RADISYS_NUM_OF_CELLS 2 FAP.0.FAP_LTE.1" >> configFile')
            elif count == 2:
                child.sendline('sed -i \'/LTE_X_RADISYS_NUM_OF_CELLS 2 FAP.0.FAP_LTE.1/s/^#//g\' configFile')

        child.expect('# ', timeout=30)
        child.sendline('sync')
        child.expect('# ', timeout=30)
        child.sendline('reboot')
        time.sleep(30)
    except Exception as err:
           logger.error('Error in OAM Configurations' + str(err))

def Cell_Configuration(CELL):
    fout = open('../Logs/Board.log', 'a')
    try:
        logger.info('cell configurations')
        #CELL configuration
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.ENB_IP,
                logfile=fout)  
        child.expect('(?i)password', timeout=10)
        child.sendline(config.ENB_PASS)
        child.expect('# ',timeout=30)
        child.sendline('cd ' + config.CLI_PATH)
        child.expect('# ',timeout=30)
        if CELL == "1":
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
        elif CELL == "2":
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
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.ENB_IP,
                            logfile=fout)
        child.expect('(?i)password', timeout=10)
        child.sendline(config.ENB_PASS)
        child.expect('# ',timeout=30)
        child.sendline('cd ' + config.SCRIPT_PATH)
        child.expect('# ', timeout=30)
        child.sendline('./stop_TeNB.sh')
        child.expect('# ', timeout=30)
        child.sendline('sync')
        child.expect('# ', timeout=30)
        child.sendline('reboot')
        time.sleep(30)
    except Exception as err:
        logger.error('Error in Cell Configurations' + str(err))


def ENB_Teardown():
    try:
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.ENB_IP,
                                logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.ENB_PASS)
        child.sendline('cd ' + config.SCRIPT_PATH)
        child.expect(prompt, timeout=30)
        child.sendline('./stop_TeNB.sh')
        child.expect(prompt, timeout=30)
        #collect logs 
        child.sendline('rm -r /rsys/setup')
        child.expect(prompt, timeout=30)
    except Exception as err:
        logger.error('Error while ENB Teardown' + str(err))

