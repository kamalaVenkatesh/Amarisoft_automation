*** Settings ***
Documentation     test1
Library           SSHLibrary
Library           OperatingSystem
Library           Process
Library           String
Resource          ../resources/keywords.robot
Resource          ../resources/variables.robot
#Test Setup        automation setup
#Test Teardown     Teardown setup

*** Test Cases ***
#Check Setup Reachability
#    Is EPC Reachable
#    Is ENB Reachable
#    Is UE Reachable

#Setup Bringup
#    EPC Node Bringup
#    UE Node Bringup

UE Attach Detach Scenario
#    [Arguments]    ${OAM}    ${Mode}    ${Cell}    ${File}    ${NO_UE}    ${Tr_Type}    ${Tr_Proto}
    ENB_Bringup    OAM    1
#    Copy Scenario File    "ue_attach_detach.cfg"
#    Run_scenario    ue_attach_detach.cfg    
#    Power on UE    1
#    Check_Ue_Status   1    connected
#    Check_Traffic    uplink    TCP    
#    Power off UE   1
#    Check_Ue_Status   1    disconnected 

#Teardown setup
#    Collect Logs
#    EPC_Teardown
#    ENB_Teardown
#    UE_Teardown
