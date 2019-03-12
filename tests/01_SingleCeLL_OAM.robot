*** Settings ***
Documentation     test1
Library           SSHLibrary
Library           OperatingSystem
Library           Process
Library           String
Resource          ../resources/keywords.robot
Resource          ../resources/variables.robot
#Test Setup        Check Setup Reachability
#Test Teardown     Teardown setup

*** Test Cases ***
Setup Bringup
#    EPC Node Bringup
#    UE Node Bringup
    ENB Node Bringup with Single Cell and with OAM

#UE Attach Detach Scenario
#    Run scenario with   "ue_attach_detach.cfg"    1    
#    Power on UE    
#    Check_Ue_Status    "connected"    
#    Power off UE   
#    Check_Ue_Status    "disconnected"


