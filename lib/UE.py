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
ue_prompt = ["# ", pexpect.EOF]

def UE_Bringup():
    fout = open('../logs/UE.log', 'wb')
    try:
        #logging into ue
        logger.info("let login into UE")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.UE_IP,
                                                        logfile=fout)
        child.expect('(?i)password:', timeout=30)
        child.sendline(config.UE_PASS)
        child.expect(ue_prompt,timeout=30)
        child.sendline("pkill -9 lteue-avx2*")
        child.expect(ue_prompt,timeout=30)
        child.sendline("service lte stop")
        child.expect(ue_prompt,timeout=30)
        child.sendline("service firewalld stop")
        child.expect(ue_prompt,timeout=30)
        child.sendline("service httpd start")
        child.expect(ue_prompt,timeout=30)
        child.sendline("cd /root/trx_sdr")
        child.expect(ue_prompt,timeout=30)
        child.sendline("./sdr_util upgrade ")
        child.expect(ue_prompt,timeout=30)
    except Exception as err:
        logger.error('Fail to Bringup UE : ' + str(err))

def Run_Scenario(s_file):
    fout = open('../logs/UE.log', 'wb')
    try:
    #logging into ue
        logger.info("let login into UE")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + ue_ip,
        logfile=fout)  
        child.expect('(?i)password:', timeout=25)
        child.sendline(ue_passwd)
        logger.debug('ue login successful')
        #Run scenario
        child.sendline('cd '+ config.UE_PATH)
        child.expect(ue_prompt,timeout=30)
        child.sendline('./lteue config/'+ s_file+ '> run_scenario.log 2>&1 &')
        child.expect(ue_prompt,timeout=30)
        child.sendline('tail -f run_scenario.log')
        child.expect("SIB found",timeout=50)
        logger.debug("Scenario started successfully with SIB Found")
    except Exception as err:
        logger.error('Fail to Run Scenario : ' + str(err))

def power_onoff_ue(msg,ue):
    fout = open('../logs/UE.log', 'wb')
    try:
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + ue_ip,
                                                logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(ue_passwd)
        child.expect(ue_prompt,timeout=30)
        for i in range(1,ue): 
            cmd= "/root/ue/doc/ws.js "+ config.UE_IP+":9002 '{\"message\": \""+msg+"\",\"ue_id\":"+i+"}'"
            child.sendline(cmd)
            child.expect(ue_prompt,timeout=30)
    except Exception as err:
        logger.error('Fail to Run Scenario : ' + str(err))

def UE_Teardown():
    fout = open('../logs/UE.log', 'wb')
    try:
        logger.info("let login into UE")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + ue_ip,
                                logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(ue_passwd)
        child.sendline('pkill -9 lteue-avx2')
        #collect logs
        child.expect(ue_prompt,timeout=30)
        child.sendline('rm -r /tmp/ue0.log')
        child.expect(ue_prompt,timeout=30)
    except Exception as err:
        logger.error('Error while UE Teardown: ' + str(err))


def Check_Ue_Status(ue,status):
    try:
        res=0
        mustend = time.time() + timeout
        while time.time() < mustend:
            if UE_Monitor(ue,state): 
                res=1
            time.sleep(period)
        if res == 0:
            raise Exception("Timeout :"+ ue + " UE Not " + status)
        ssh.close()
    except Exception as err:
        logger.error('Error in checking UE Status :' + str(err))
        ssh.close()

def Check_Traffic(tr_type,tr_proto,data,time_slot=99999):
    try:
        VS_Prereq()
        if tr_type == "uplink":
            send_traffic(config.VS_IP,config.VS_USER,config.VS_PASS,config.UE_IP,
                                config.UE_USER,config.UE_PASS,tr_proto,ue,data,time_slot)
        elif tr_type == "downlink":
            send_traffic(config.UE_IP,config.UE_USER,config.UE_PASS,config.VS_IP,
                                  config.VS_USER,config.VS_PASS,tr_proto,ue,data,time_slot)
    except Exception as err:
        logger.error('Error in Traffic exchange :' + str(err))

def UE_Monitor(ue,state):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config.UE_IP, username=config.UE_USER, password=config.UE_PASS)
    logger.info("inside UE_Monitor")

    cmd= "/root/ue/doc/ws.js "  + config.UE_IP+":9002 '{\"message\": \"ue_get\"}'"
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
        res=UE_Stats(obj,ue,state)
        logger.info("after UE_Stats")
        logger.info(res)
        return res
    else:
        raise RunTimeError("Error while connecting Nodejs server" + ssh_stderr.read())

def UE_Stats(obj,ue,status):
    logger.info("I am here to collect UE_Stats")
    n=0
    for i in obj:
        for k in obj[i]:
            for l in k:
                if l == "rrc_state":
                    if k[l] == status:
                        logger.info('equal')
                        n=n+1
    if n >= ue:
        return True
    else:
        return False


def remove_lines(fname,start,count):
    logger.info("removing lines")
    for line in fileinput.input(fname, inplace=1, backup='.orig'):
        if start <= fileinput.lineno() < start + count:
            pass
        else:
            print line[:-1]
    fileinput.close()

def send_traffic(server_ip,server_user,server_pass,client_ip,client_user,client_pass,tr_proto,ue,data,time_interval):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    #server
    ssh.connect(server_ip, username=server_user, password=server_pass)
    if tr_proto == "tcp":
        flag = "-w"
    elif tr_proto == "udp":
        flag = "-b"
    cmd = "iperf -s -t "+time_interval + " --" + tr_proto + " " + flag + data + " -i l &"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
                raise Exception("Error in server")
    ssh.close()
    
    #client
    ssh.connect(client_ip, username=client_user, password=client_pass)
    for i in range(1,ue):
        cmd = "iperf -c 10.20.40.%d/24 -t " + time_interval+" --" + tr_proto + " " + flag + data + "-i l &"% (i)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        if ssh_stderr != "":
            raise Exception("Error in client")
    ssh.close()
    time.sleep(time_interval)


def VS_Prereq():
    fout = open('../logs/VS.log', 'wb')
    try:
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + config.VS_IP,
            logfile=fout)
        child.expect('(?i)password:', timeout=25)
        child.sendline(config.VS_PASS)
        child.sendline('route add -net '+ config.UE_SUBNET +' gw '+ config.pgw)
        child.expect(ue_prompt,timeout=30)
        child.sendline("ip addr show | awk /'/inet.*brd//{print $NF; exit}//'")
        child.readline()
        interface = child.readline()
        child.sendline('ifconfig ' + interface.rstrip() + ' mtu 1390 up')
        child.expect(ue_prompt,timeout=30)
        child.sendline('pkill -9 iperf')
        child.expect(ue_prompt,timeout=30)
        child.sendline('pkill -9 iperf')
        child.expect(ue_prompt,timeout=30)
    except Exception as err:
        logger.error('Error in Video server prereqisites: ' + str(err))


