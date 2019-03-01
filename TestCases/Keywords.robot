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

Restart cne service
    Execute Command    ./restart_cne.sh 1

Get l2Log
    Open Connection And Log In    ${Board}    ${BD_USER}    ${BD_PASS}
    OperatingSystem.Get File    ${L2_LOG_PATH1}    ${TARGET_PATH}
    Log out

Get dbgLog
    Open Connection And Log In    ${Board}    ${BD_USER}    ${BD_PASS}
    OperatingSystem.Get File    ${L2_LOG_PATH2}    ${TARGET_PATH}
    Log out

Get systemLog
    Open Connection And Log In    ${Board}    ${BD_USER}    ${BD_PASS}
    OperatingSystem.Get File    ${L2_LOG_PATH3}    ${TARGET_PATH}
    Log out

Get UE_consoleLog
    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
    OperatingSystem.Get File    ${L2_LOG_PATH4}    ${TARGET_PATH}
    Log out

Get UELog
    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
    OperatingSystem.Get File    ${L2_LOG_PATH5}    ${TARGET_PATH}
    Log out

Collect Logs
    Get l2Log
    Get dbgLog
    Get systemLog
    Get UELog

