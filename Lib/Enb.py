import paramiko 
import fileinput
import os
import json
import sys
import time
import pexpect
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

class RunTimeError(Exception):
        ROBOT_EXIT_ON_FAILURE = True

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
        #raise RunTimeError("Board Configurations SetUp Error")

def UE_Status(*args):
    logger.info("In UE status")
    res=wait_until(UE_Monitor,timeout=5,period=5,ssh=args[0],ue=args[1],ue_ip=args[2],state=args[3])
    logger.info("returning from uE status")
    logger.info(res)
    return res

def Execute_scenario(ue_ip,ue_passwd):
    prompt = ['\w+\@\w+.*?\#', '\w+\@\w+.*?\$', '\#', '\$', '#', pexpect.EOF]
    fout = open('../Logs/UE.log', 'wb')
    try:
    #logging into ue
        logger.info("let login into UE")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + ue_ip,
        logfile=fout)  # Creates a child obj for spawning ssh to ue
        child.expect('(?i)password:', timeout=25)
        child.sendline(ue_passwd)
        logger.debug('ue login successful')
        #Run scenario
        child.sendline("/root/ue/lteue /root/ue/config/64_ue.cfg")
        res=child.expect('(?i)SIB found',timeout=5)
        logger.info(res)
        logger.info("Scenario started successfully")
        child.sendline('power_on 1')
    except Exception as err:
        logger.error('Fail to Run Scenario : ' + str(err))

def Check_UE_Status(ue_ip,ue_passwd,ue,status):
    ssh = paramiko.SSHClient()
    #ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ue_ip, username="root", password=ue_passwd)
        #check UE status connected
        res= UE_Status(ssh,ue,ue_ip,status)
        if res == False:
            raise Exception("UE Not attached timeout")
        ssh.close()
    except Exception as err:
        logger.error('Error in checking UE Status :' + str(err))
        ssh.close()
        #raise RunTimeError("UE Status timeout")

def Check_traffic(ue_ip,ue_passwd,vs_ip,vs_passwd,tr_type,ue):
    try:
        if tr_type == "uplink":
            check_uplink(vs_ip,vs_passwd,ue_ip,ue_passwd,ue)
        elif tr_type == "downlink":
            check_downlink(vs_ip,vs_passwd,ue_ip,ue_passwd,ue)
    except Exception as err:
        logger.error('Error in Traffic exchange :' + str(err))
        #raise RunTimeError("Traffic Exchange failed")

def wait_until(somepredicate, ssh, ue, ue_ip, state, timeout=40, period=5):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(ssh,ue,ue_ip,state): return True
        time.sleep(period)
    return False

def UE_Monitor(ssh,ue,ip,state):
    logger.info("inside UE_Monitor")
    cmd= "/root/ue/doc/ws.js "  + ip+":9002 '{\"message\": \"ue_get\"}'"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr.read() == "":
        f = open("out.txt", 'w+')
        f.write(ssh_stdout.read())
        f.close()
        
        #Now i need to remove first 3 lines in this file
        remove_lines("out.txt",1,3)        
        
        #load it to json object
        f = open("out.txt", 'r')
        outfile = f.read()
        f.close()
        obj = json.loads(outfile)
        print obj 
        #get the status
        res=UE_Stats(obj,state)
        logger.info("after UE_Stats")
        logger.info(res)
        if res == ue: return ue
        return 0
    else:
        raise Exception("Error while connecting Nodejs server" + ssh_stderr.read())
        return 0

def UE_Stats(obj,status):
    logger.info("I am here to collect UE_Stats")
    n=0
    logger.info(status)
    for i in obj:
        for k in obj[i]:
            for l in k:
                if l == "rrc_state":
                    logger.info(k[l])
                    if str(k[l]) == status:
                        logger.info("equal")
                        n=n+1
    logger.info(n)
    return n


def remove_lines(fname,start,count):
    logger.info("removing lines")
    for line in fileinput.input(fname, inplace=1, backup='.orig'):
        if start <= fileinput.lineno() < start + count:
            pass
        else:
            print line[:-1]
    fileinput.close()

def check_uplink(server_ip,server_passwd,client_ip,client_passwd,ue):
    ssh = paramiko.SSHClient()
    #ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #server
    ssh.connect(server_ip, username="root", password=server_passwd)
    cmd="/root/IPERF_SIM/iperf_server_udp.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    ssh.close()
    #client
    ssh.connect(client_ip, username="root", password=client_passwd)
    cmd="/root/IPERF_SCRIPT/iperf_client_udp_1.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    ssh.close()

def check_downlink(server_ip,server_passwd,client_ip,client_passwd,ue):
    ssh = paramiko.SSHClient()
    #ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #server
    ssh.connect(server_ip, username="root", password=server_passwd)
    cmd="/root/IPERF_SIM/iperf_server_1Ues_udp.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
        raise Exception("Error in server for downlink traffic")
    ssh.close()
    #client
    ssh.connect(client_ip, username="root", password=client_passwd)
    cmd="/root/IPERF_SCRIPT/iperf_client_1_ue_udp.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
                raise Exception("Error in client for downlink traffic")
    ssh.close()
