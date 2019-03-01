*** Settings ***
Documentation     Check EPC Node reachability
Library           SSHLibrary
Library           OperatingSystem
Library           ../Lib/Enb.py
Library           Process
Resource          Keywords.robot
Resource          variables.robot
Test Teardown  run keyword if test failed  Collect Logs

*** Test Cases ***
Check EPC Reachability
    Open Connection And Log In    ${EPC}    ${EPC_USER}    ${EPC_PASS}
    Execute Command And Verify Output
    Log out

Check UE Reachability
    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
    Execute Command And Verify Output
    Log out

Check Board Reachability
    Open Connection And Log In    ${Board}   ${BD_USER}    ${BD_PASS}
    Execute Command And Verify Output
    Log out

EPC Configurations
    EPC_Configurations    ${EPC}    ${EPC_PASS}

Board Configurations
    Bringup_Board   ${Board}   ${BD_PASS}     ${OAM}    ${CELL}

#UE Configurations
#    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
#    Execute Command    service lte stop
#    Execute Command     ./trx_sdr/sdr_util upgrade
#    Put File    ${Config_path}/${UE_File}    ${UE_path}/${UE_File}
#
#Run Scenario 
#    ${output}=    Execute_scenario    ${UE}    ${UE_PASS}   
#    Should Be Equal    ${output}  "True"  

#UE Connected 
#    Check_Ue_Status    ${UE}     ${UE_PASS}    ${UE}    ${ATTACH}

#Send Traffic
#    Check_Traffic    ${UE}    ${UE_PASS}   ${VS_IP}    ${VS_PASS}    ${Traffic_Type}    ${UE}

#UE Disconnected
#    Check_UE_Status    ${UE}     ${UE_PASS}    ${UE}    ${DETACH}

#Collect Logs
#    Collect Logs    
    


