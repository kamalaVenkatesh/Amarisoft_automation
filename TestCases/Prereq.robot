*** Settings ***
Documentation     Check EPC Node reachability
Library           SSHLibrary
Library           OperatingSystem
Library           ../Lib/Enb.py
Library           Process
Resource          Keywords.robot
Resource          variables.robot

*** Test Cases ***
#Check EPC Reachability
#    Open Connection And Log In    ${EPC}    ${EPC_USER}    ${EPC_PASS}
#    Execute Command And Verify Output
#    Log out

#Check UE Reachability
#    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
#    Execute Command And Verify Output
#    Log out

#Check Board Reachability
#    Open Connection And Log In    ${EPC}    ${EPC_USER}    ${EPC_PASS}
#    Check_Board_reachability    ${Board}   ${BD_PASS}
#    Log out

#EPC Configurations
#    Open Connection And Log In    ${EPC}    ${EPC_USER}    ${EPC_PASS}
#    Restart cne service
#    Log out

#Board Configurations
#    Enb_Configurations    ${Board}   ${BD_PASS}    ${OAM}    ${CELL}

UE Configurations
    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
    Execute Command    service lte stop
    Execute Command     ./trx_sdr/sdr_util upgrade
    Put File    ${Config_path}/${UE_File}    ${UE_path}/${UE_File}

Run Scenario 
    Execute_scenario    ${UE}    ${UE_PASS}   

UE Connected 
    Check_UE_Status    ${UE}     ${UE_PASS}    ${UE}    "connected"

Send Traffic
    Check_traffic    ${UE}    ${UE_PASS}   ${VS_IP}    ${VS_PASS}    ${Traffic_Type}    ${UE}

UE Disconnected
    Check_UE_Status    ${UE}     ${UE_PASS}    ${UE}    "disconnected"

Collect Logs
    Collect Logs    
    


