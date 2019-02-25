*** Settings  ***********
Library    ../Lib/Enb.py

*** Keywords ***
Open Connection And Log In
    [Arguments]    ${arg1}    ${arg2}    ${arg3}   
    Open Connection    ${arg1} 
    Login    ${arg2}    ${arg3}

Execute Command And Verify Output
    [Documentation]    Execute Command can be used to run commands on the remote machine.
    ...    The keyword returns the standard output by default.
    ${output}=    Execute Command    echo Hello SSHLibrary!
    Should Be Equal    ${output}    Hello SSHLibrary!

Log out
    Close Connection

wait for sometime
    [Arguments]    ${sec}
    sleep    ${sec}


OAM Configurations
    ${IP}=    Execute Command    grep -Po '(?<=LTE_SIGLINK_SERVER_LIST_IP=).*' /root/rysy/config/configFile
    Log    ${IP}
    Run Keyword Unless    '${IP}'=='${EPC}'    Execute Command    sed -i 's/${IP}/${EPC}/g' /root/rysy/config/configfile
    Execute Command    sync
    Execute Command    reboot
    sleep    60
    Open Connection And Log In    ${Board}    ${BD_USER}    ${BD_PASS}
    Execute Command    ./root/rsys/script/install.sh
    Execute Command    ./root/rsys/script/start_TeNB.sh
    Log out
    Open Connection And Log In    ${Board}    ${BD_USER}    ${BD_PASS}

Single Cell configurations
    Execute Command    tr69.addobject Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.
    Execute Command    tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1
    Execute Command    tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101
    Execute Command    tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.Enable 1
    Execute Command    tr69.set Device.Services.FAPService.1.FAPControl.LTE.AdminState 1

CA Configurations
    Exceute Command    tr69.addobject Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.
    Execute Command    tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1
    Execute Command    tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101
    Execute Command    tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.CellReservedForOperatorUse 1
    Execute Command    tr69.set Device.Services.FAPService.1.CellConfig.LTE.EPC.PLMNList.1.Enable 1
    Execute Command    tr69.addobject Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.
    Execute Command    tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.IsPrimary 1
    Execute Command    tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.PLMNID 00101
    Execute Command    tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.CellReservedForOperatorUse 1
    Execute Command    tr69.set Device.Services.FAPService.2.CellConfig.LTE.EPC.PLMNList.1.Enable 1
    Execute Command    tr69.set Device.Services.FAPService.1.FAPControl.LTE.AdminState 1

Restart cne service
    Execute Command    ./restart_cne.sh 1
