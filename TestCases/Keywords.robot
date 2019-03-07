*** Settings  ***********
Library           ../Lib/UE.py
Library           ../Lib/Epc.py
Library           ../Lib/Enb.py

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

EPC Node Bringup
    Clean_EPC
    EPC_Bringup

ENB Bringup
    Clean_ENB
    ENB_Bringup

Amarisoft UE Node Bringup
    Open Connection And Log In    ${UE_IP}    ${UE_USER}    ${UE_PASS}
    Execute Command    service lte stop
    Execute Command     ./trx_sdr/sdr_util upgrade

Copy Scenario File
    [Arguments]    ${scenario_file}
    Open Connection And Log In    ${UE_IP}    ${UE_USER}    ${UE_PASS}
    SSHLibrary.Put File    ${Config_path}/${scenario_file}    ${UE_PATH}/${scenario_file}

Get l2Log
    Open Connection And Log In    ${Board}    ${BD_USER}    ${BD_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH1}    ${TARGET_PATH}
    Log out

Get dbgLog
    Open Connection And Log In    ${Board}    ${BD_USER}    ${BD_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH2}    ${TARGET_PATH}
    Log out

Get systemLog
    Open Connection And Log In    ${Board}    ${BD_USER}    ${BD_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH3}    ${TARGET_PATH}
    Log out

Get UE_consoleLog
    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH4}    ${TARGET_PATH}
    Log out

Get UELog
    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
    SSHLibrary.Get File    ${L2_LOG_PATH5}    ${TARGET_PATH}
    Log out

Collect Logs
    Get l2Log
    Get dbgLog
    Get systemLog
    Get UELog

