*** Settings ***
Documentation     Check EPC Node reachability
Library           SSHLibrary
Library           Operatingsystem
Library           ../Lib/Enb.py
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

Execute Scenarios
    Open Connection And Log In    ${UE}    ${UE_USER}    ${UE_PASS}
    Execute Command    service lte stop
    Execute Command     ./trx_sdr/sdr_util upgrade
    Put File    ../Config/ue_64.cfg    /root/ue/config/ue_new_64.cfg
    ${value}=    Execute Command    /root/ue/lteue /root/ue/config/ue_new_64.cfg
    Log    ${value}


