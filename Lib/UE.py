def Run_Scenario(scenario):
    global NO_UE
    prompt = ['\w+\@\w+.*?\#', '\w+\@\w+.*?\$', '\#', '\$', '#', pexpect.EOF]
    fout = open('../Logs/UE.log', 'wb')
    try:
    #logging into ue
        logger.info("let login into UE")
        child = pexpect.spawn('ssh -o StrictHostKeyChecking=no root@' + ue_ip,
        logfile=fout)  
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
        child.sendline('cd '+ ueconfig.UE_PATH)
        child.expect(prompt,timeout=30)
        child.sendline('./lteue config/'+ scenario+ '> run_scenario.log 2>&1 &')
        child.expect(prompt,timeout=30)
        child.sendline('tail -f run_scenario.log')
        child.expect("SIB found",timeout=50)
        logger.debug("Scenario started successfully with SIB Found")
    except Exception as err:
        logger.error('Fail to Run Scenario : ' + str(err))

def Check_Ue_Status(ue,status):
    try:
        res=0
        mustend = time.time() + timeout
        while time.time() < mustend:
            if UE_Monitor(ue,state): 
                res=1
            time.sleep(period)
        if res == 0:
            raise Exception("Timeout : UE Not " + status)
        ssh.close()
    except Exception as err:
        logger.error('Error in checking UE Status :' + str(err))
        ssh.close()

def Check_Traffic(tr_type,tr_proto):
    try:
        if tr_type == "uplink":
            check_uplink(tr_proto,ue)
        elif tr_type == "downlink":
            check_downlink(tr_proto,ue)
    except Exception as err:
        logger.error('Error in Traffic exchange :' + str(err))

def UE_Monitor(ue,state):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ueconfig.UE_IP, username=ueconfig.UE_USER, password=ueconfig.UE_PASS)
    logger.info("inside UE_Monitor")

    cmd= "/root/ue/doc/ws.js "  + ueconfig.UE_IP+":9002 '{\"message\": \"ue_get\"}'"
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
        for k in obj[i]:
            for l in k:
                if l == "rrc_state":
                    if k[l] == status:
                        logger.info('equal')
                        n=n+1
    return n


def remove_lines(fname,start,count):
    logger.info("removing lines")
    for line in fileinput.input(fname, inplace=1, backup='.orig'):
        if start <= fileinput.lineno() < start + count:
            pass
        else:
            print line[:-1]
    fileinput.close()

def check_uplink(tr_proto,ue):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    #server
    ssh.connect(ueconfig.VS_IP, username=ueconfig.VS_USER, password=ueconfig.VS_PASS)
    cmd="/root/IPERF_SIM/iperf_server_udp.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
                raise Exception("Error in server for downlink traffic")
    ssh.close()
    
    #client
    ssh.connect(ueconfig.UE_IP, username=ueconfig.UE_USER, password=ueconfig.UE_PASS)
    cmd="/root/IPERF_SCRIPT/iperf_client_udp_1.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
        raise Exception("Error in server for downlink traffic")
    ssh.close()

def check_downlink(tr_proto,ue):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    #server
    ssh.connect(ueconfig.UE_IP, username=ueconfig.UE_USER, password=ueconfig.UE_PASS)
    cmd="/root/IPERF_SIM/iperf_server_1Ues_udp.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
        raise Exception("Error in server for downlink traffic")
    ssh.close()
    
    #client
    ssh.connect(ueconfig.VS_IP, username=ueconfig.VS_USER, password=ueconfig.VS_PASS)
    cmd="/root/IPERF_SCRIPT/iperf_client_1_ue_udp.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if ssh_stderr != "":
                raise Exception("Error in client for downlink traffic")
    ssh.close()




