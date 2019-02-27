import paramiko 
import fileinput
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
        child.sendline('exit')

def Execute_scenario(ue_ip,ue_passwd,ue):
    prompt = ['\w+\@\w+.*?\#', '\w+\@\w+.*?\$', '\#', '\$', '#', pexpect.EOF]
    fout = open('../Logs/UE.log', 'wb')
    try:
    #logging into board
        logger.info("let login into UE")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + ue_ip,
        logfile=fout)  # Creates a child obj for spawning ssh to ue
        child.expect('(?i)password:', timeout=25)
        child.sendline(ue_passwd)
        logger.debug('ue login successful')
        #Run scenario
        #child.sendline("/root/ue/lteue /root/ue/config/64_ue.cfg")
        #child.expect('SIB FOUND',timeout=20)
        logger.info("Scenario started successfully")
        #time.sleep(2000)
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username="root", password=passwd)
        res= wait_until(UE_Connected,timeout=20,ssh,ue,status="connected")
        if res:
            #send traffic
            check_uplink()
            time.sleep()
            check_downlink()
        time.sleep()
        #res=wait_until(UE_Disconnect,timeout=20,ssh,ue,status="disconnected")
        if res:
            #teardown
            pass
        child.sendline('exit')
    except Exception as err:
        logger.error('Error in Board Configurations SetUp' + str(err))
        child.sendline('exit')

def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs): return True
        time.sleep(period)
    return False

def UE_Monitor(ssh,ue,status):
    cmd= "/root/ue/doc/ws.js "  + ip+":9002 '{\"message\": \"ue_get\"}'"
    #print result
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr.read() == "":
        output_file = ssh_stdout.read()
        #Now i need to remove first 4 lines in this file
        remove_lines(output_file,1,3)
        remove_lines(output_file,2,1)
        #load it to object
        obj = json.loads(output_file)
        #get the status
        res=UE_Status(obj,status)
        if res == ue: return ue
        return 0


def UE_Status(obj,status):
    states=0
    for i in obj:
        for k in obj[i]:
            for l in k:
                if l == "rrc_state":
                    if k[l] == "connected":
                        states=states+1
    return states


def remove_lines(fname,start,count):
    for line in fileinput.input(fname, inplace=1, backup='.orig'):
        if start <= fileinput.lineno() < start + count:
            pass
        else:
            print line[:-1]
    fileinput.close()

def check_uplink():
    #client

    #server
    pass

def check_downlink():
    #client

    #server
    pass
