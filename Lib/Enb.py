import os
import sys
import time
import pexpect
from robot.api import logger 

def Check_Board_reachability(enb_ip,enb_passwd):
    logger.info("checking reachability")
    fout = open('../Logs/Board.log', 'wb')
    try:
    #logging into board
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enb_ip,
                    logfile=fout)  # Creates a child obj for spawning ssh to board
        logger.info("logging into it")
        child.expect('(?i)password:', timeout=10)
        child.sendline(enb_passwd)
        #child.expect(prompt, timeout=30)
        child.sendline('echo abcd >> kml12.txt')
        #child.expect(prompt, timeout=30)
        child.sendline('exit')
        child.sendline('exit')
        time.sleep(5)
    except Exception as err:
        logger.error('Error in bringup Board' + str(err))

def Enb_Configurations(enb_ip,enb_passwd,OAM,Cell):
    prompt = ['\w+\@\w+.*?\#', '\w+\@\w+.*?\$', '\#', '\$', '#', pexpect.EOF]
    fout = open('../Logs/Board.log', 'wb')
    try:
        #logging into board
        logger.info("let login into board")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enb_ip,
                            logfile=fout)  # Creates a child obj for spawning ssh to board
        child.expect('(?i)password:', timeout=25)
        child.sendline(enb_passwd)
        logger.debug('login successful')
        child.sendline('ls  \r')
        child.sendline('rm -r rsys \r')
        logger.info('deleted existing binaries on BCM/XEON board')
        #copying binaries to the board
        child.sendline('scp -r root@172.27.22.71:/root/Keerthi/Amarisoft/QCOM_FDD/SC/rsys/ /root/')
        child.expect('(?i)password:',timeout=20)
        child.sendline(enb_passwd)
        logger.info('Going to copy binaries')
        child.sendline('umount /mnt/firmware')
        child.sendline('mount -t vfat /dev/mmcblk0p1 /mnt/firmware/')
        child.sendline('cp -f /root/rsys/bin/mdm2_00.mbn /mnt/firmware')
        #OAM Configurations
        if OAM == "YES":
            pass
            child.sendline("grep 'LTE_SIGLINK_SERVER_LIST' /root/rsys/config/configFile | awk '{print $2}'")
            #child.expect(prompt, timeout=30)
            current_ip=child.read()
            logger.info("current_ip =" + str(current_ip))
            #if str(current_ip) != str(enb_ip):
                #child.sendline("sed -i 's/current_ip/enb_ip/g' /root/rsys/config/configfile")
                #child.sendline('sync')
                #child.sendline('reboot')
                #time.sleep(30)
                #child.sendline('exit')
                #child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enb_ip,logout=fout)
                #child.expect('(?i)password:', timeout=10)
                #child.sendline(enb_passwd)

        child.sendline('cd /root/rsys/script/')
        child.sendline('. ./install.sh')
        child.sendline('. ./start_TeNB.sh')
        child.sendline('exit')
        #opening new terminal
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enb_ip,
                                                logfile=fout)  # Creates a child obj for spawning ssh to board
        child.expect('password:', timeout=10)
        child.sendline(enb_passwd)
        child.sendline("echo 'now cell configurations' >> new")
        time.sleep(5)
        if Cell == "Single_Cell":
            child.sendline('tr69.addobject Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.Enable 1')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.FAPControl.LTE.AdminState 1')
            #child.expect(self.prompt, timeout=30)
        if Cell == "CA":
            child.sendline('tr69.addobject Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.CellReservedForOperatorUse 1')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.Enable 1')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.addobject Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.CellReservedForOperatorUse 1')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.Enable 1')
            #child.expect(self.prompt, timeout=30)
            child.sendline('tr69.set Device.Services.FAPService.1.FAPControl.LTE.AdminState 1')
            #child.expect(self.prompt, timeout=30)
        child.sendline('exit')
    except Exception as err:
            logger.error('Error in Board Configurations SetUp' + str(err))


def UE_configurations():
    ssh = paramiko.SSHClient()
    ssh.connect(ue, username=ue_user, password=ue_passwd)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('./root/trx_sdr/sdr_util upgrade')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('scp -r /root/ue/config/')
