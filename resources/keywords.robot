*** Settings  ***********
Library           ../lib/UE.py
Library           ../lib/Epc.py
Library           ../lib/Enb.py
variables         ../config/config.py

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

Is EPC Reachable
    Open Connection And Log In    ${EPC_IP}    ${EPC_USER}    ${EPC_PASS}
    Execute Command And Verify Output
    Log out

Is UE Reachable
    Open Connection And Log In    ${UE_IP}    ${UE_USER}    ${UE_PASS}
    Execute Command And Verify Output
    Log out

Is ENB Reachable
    Open Connection And Log In    ${ENB_IP}   ${ENB_USER}    ${ENB_PASS}
    Execute Command And Verify Output
    Log out

VS Clean
    Open Connection And Log In    ${VS_IP}   ${VS_USER}    ${VS_PASS}
    Execute Command    kill -9 iperf
    Execute Command    kill -9 iperf
    Log out

EPC Node Bringup
    Clean_EPC
    EPC_Bringup

UE Node Bringup
    UE_Bringup

Power on UE
    [Arguments]    ${No_UE}
    power_onoff_ue    power_on    ${No_UE}

Power off UE
    [Arguments]    ${No_UE}
    power_onoff_ue    power_off    ${No_UE}

Check Setup Reachability
    Is EPC Reachable
    Is ENB Reachable
    Is UE Reachable

ENB Node Bringup with Single Cell and with OAM
#    Clean_ENB
    ENB_Bringup    Single_Cell    OAM

ENB Node Bringup with Single Cell and without OAM
    ENB_Bringup    0    1

ENB Node Bringup with CA and with OAM
    ENB_Bringup    1    2

ENB Node Bringup with CA and without OAM
    ENB_Bringup    0    2

Run scenario with   
    [Arguments]    ${scenario_file}
    Open Connection And Log In    ${UE_IP}    ${UE_USER}    ${UE_PASS}
    SSHLibrary.Put File    ${CFG_PATH}/${scenario_file}    ${UE_PATH}/${scenario_file}
    Run_scenario   ${scenario_file} 

Get l2Log
    Open Connection And Log In    ${ENB_IP}    ${ENB_USER}    ${ENB_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH1}    ${TARGET_PATH}
    Log out

Get dbgLog
    Open Connection And Log In    ${ENB_IP}    ${ENB_USER}    ${ENB_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH2}    ${TARGET_PATH}
    Log out

Get systemLog
    Open Connection And Log In    ${ENB_IP}    ${ENB_USER}    ${ENB_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH3}    ${TARGET_PATH}
    Log out

Get UE_consoleLog
    Open Connection And Log In    ${UE_IP}    ${UE_USER}    ${UE_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH4}    ${TARGET_PATH}
    Log out

Get UELog
    Open Connection And Log In    ${UE_IP}    ${UE_USER}    ${UE_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH5}    ${TARGET_PATH}
    Log out

Collect Logs
    Get l2Log
    Get dbgLog
    Get systemLog
    Get UELog

Teardown setup
    Collect Logs
    EPC_Teardown
    ENB_Teardown
    UE_Teardown

