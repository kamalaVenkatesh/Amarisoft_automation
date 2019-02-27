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

Execute_scenarios
   ${result}=    Run Process    /root/ue/lteue    ${UE_Path}/${UE_File}    
   Should Not Contain    ${result.stdout}    FAIL
   ${result}=    Wait For Process    First
   Should Be Equal As Integers    ${result.rc}    0
