import paramiko 
import fileinput
import os
import json
import sys
import time
import pexpect
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
sys.path.append('../Config/')
import epcconfig
import enbconfig
import ueconfig

class RunTimeError(Exception):
        ROBOT_EXIT_ON_FAILURE = True

def EPC_Configurations():
    prompt = ['#', pexpect.EOF]
    fout = open('../Logs/EPC.log', 'wb')
    try:
    #logging into EPC
        logger.info("login into EPC")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + epcconfig.EPC_IP,
                        logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(epcconfig.EPC_PASS)
        logger.debug('login successful')
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


def Bringup_Board():
    prompt = ['# ', pexpect.EOF]
    fout = open('../Logs/Board.log', 'wb')
    try:
        #logging into board
        logger.info("let login into board")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enbconfig.ENB_IP,
                logfile=fout)  # Creates a child obj for spawning ssh to board
        child.expect('(?i)password:', timeout=25)
        child.sendline(enbconfig.ENB_PASS)
        child.expect(prompt, timeout=20)
        logger.debug('login successful')
        child.sendline('rm -r rsys')
        child.expect(prompt, timeout=20)
        logger.info('deleted existing binaries on board')
        #copying binaries to the board
        cmd = "scp -r " + enbconfig.COPY_RSYS_PATH + " /root/"
        child.sendline(cmd)
        child.expect('(?i)password:',timeout=30)
        child.sendline(epcconfig.EPC_PASS)
        child.expect(prompt, timeout=20)
        logger.info('copied rsys')
        child.sendline('umount /mnt/firmware')
        child.expect(prompt, timeout=20)
        child.sendline('mount -t vfat /dev/mmcblk0p1 /mnt/firmware/')
        child.expect(prompt, timeout=20)
        child.sendline('cp -f /root/rsys/bin/mdm2_00.mbn /mnt/firmware')
        child.expect(prompt, timeout=20)
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
        child.expect(prompt, timeout=20)
        #Bringup Board
        child.sendline('cd ' + enbconfig.SCRIPT_PATH)
        child.expect(prompt, timeout=20)
        child.sendline('./install.sh')
        child.expect(prompt, timeout=20)
        child.sendline('./start_TeNB.sh > TeNB_console.log 2>&1 &')
        child.expect(prompt, timeout=20)
        time.sleep(40)
        child.sendline('tail -f TeNB_console.log')
        child.expect("address", timeout=50)
        logger.debug("EPC To ENB Connection is successfull")
        time.sleep(10)
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
    prompt = ['# ', pexpect.EOF]
    fout = open('../Logs/Board.log', 'a')
    logger.info("Inside OAM Configurations")
    try:
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + enbconfig.ENB_IP,
                                logfile=fout)  # Creates a child obj for spawning ssh to board
        child.expect('(?i)password:', timeout=25)
        child.sendline(enbconfig.ENB_PASS)
        child.expect('# ', timeout=30)
        logger.debug('login successful')
        #ssh = paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(enbconfig.ENB_IP, username=enbconfig.ENB_USER, password=enbconfig.ENB_PASS)
        cmd = "grep 'LTE_SIGLINK_SERVER_LIST' "+ enbconfig.CONFIG_FILE + " | awk '{print $2}'"
        logger.info(cmd)
        #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        child.sendline(cmd)
        #child.expect('# ', timeout=30)
        #current_ip = ssh_stdout.read()
        child.readline()
        current_ip = child.readline()
        logger.info(current_ip)
        #child.expect('# ', timeout=30)
        logger.info('Inside OAM')
        logger.info(current_ip)
        if current_ip != epcconfig.EPC_IP:
            cmd = "sed -i 's/"+ current_ip.rstrip() +"/\""+ epcconfig.EPC_IP+"\"/g' " + enbconfig.CONFIG_FILE
            logger.info(cmd)
            #ssh.exec_command(cmd)
            child.sendline(cmd)
            child.expect('# ', timeout=30)
            #add OAM enable changes in files
            #ssh.exec_command('sync')
            child.sendline('sync')
            child.expect('# ', timeout=30)
            #time.sleep(5)
            child.sendline('reboot')
            #ssh.exec_command('reboot')
            time.sleep(30)
            #try login again
            #ssh.connect(enbconfig.ENB_IP, username=enbconfig.ENB_USER, password=enbconfig.ENB_PASS)
            #ssh.close()
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
        cmd = "grep 'LTE_SIGLINK_SERVER_LIST' "+ enbconfig.CONFIG_FILE + " | awk '{print $2}'"
        logger.info(cmd)
        child.sendline(cmd)
        IP = child.readline()
        logger.info(IP)
        logger.info('got ahh')
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
        
def UE_Status(*args):
    logger.info("In UE status")
    res=wait_until(UE_Monitor,timeout=5,period=5,ssh=args[0],ue=args[1],ue_ip=args[2],state=args[3])
    logger.info("returning from uE status")
    logger.info(res)
    return res

def Run_Scenario(ue_ip,ue_passwd):
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
        #pkill the already running scenario if exist
        #child.sendline("ps -eaf | grep lteue-avx2 | head -n 1 | awk \'{print $2}\'"
        #res = child.expect('^[0-9]+$', timeout=2)
        #if res == 0:
        #    procees_id = child.read()
        #    child.sendline('pkill -9' + process_id)
        #Run scenario
        child.sendline("/root/ue/lteue /root/ue/config/64_ue.cfg")
        res=child.expect('(?i)SIB found',timeout=30)
        logger.info(res)
        logger.info("Scenario started successfully")
    except Exception as err:
        logger.error('Fail to Run Scenario : ' + str(err))

def Check_Ue_Status(ue_ip,ue_passwd,ue,status):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ue_ip, username="root", password=ue_passwd)
        res= UE_Status(ssh,ue,ue_ip,status)
        if res == False:
            raise Exception("Timeout : UE Not " + status)
        ssh.close()
    except Exception as err:
        logger.error('Error in checking UE Status :' + str(err))
        ssh.close()

def Check_Traffic(ue_ip,ue_passwd,vs_ip,vs_passwd,tr_type,ue):
    try:
        if tr_type == "uplink":
            check_uplink(vs_ip,vs_passwd,ue_ip,ue_passwd,ue)
        elif tr_type == "downlink":
            check_downlink(vs_ip,vs_passwd,ue_ip,ue_passwd,ue)
    except Exception as err:
        logger.error('Error in Traffic exchange :' + str(err))

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
        
        #get the status
        res=UE_Stats(obj,state)
        logger.info("after UE_Stats")
        logger.info(res)
        
        if res == ue: return ue
        return 0
    else:
        raise RunTimeError("Error while connecting Nodejs server" + ssh_stderr.read())

def UE_Stats(obj,status):
    logger.info("I am here to collect UE_Stats")
    n=0
    for i in obj:
        logger.info('i')
        for k in obj[i]:
            logger.info('k')
            for l in k:
                logger.info('l')
                if l == "rrc_state":
                    if k[l] == status:
                        logger.info('equal')
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
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    #server
    ssh.connect(server_ip, username="root", password=server_passwd)
    cmd="/root/IPERF_SIM/iperf_server_udp.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
                raise Exception("Error in server for downlink traffic")
    ssh.close()
    
    #client
    ssh.connect(client_ip, username="root", password=client_passwd)
    cmd="/root/IPERF_SCRIPT/iperf_client_udp_1.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
        raise Exception("Error in server for downlink traffic")
    ssh.close()

def check_downlink(server_ip,server_passwd,client_ip,client_passwd,ue):
    ssh = paramiko.SSHClient()
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
