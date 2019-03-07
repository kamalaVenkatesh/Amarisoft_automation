*** Settings ***
Documentation     Check EPC Node reachability
Library           SSHLibrary
Library           OperatingSystem
Library           Process
Library           String
Resource          Keywords.robot
Resource          variables.robot
#Test Setup        automation setup
#Test Teardown     Teardown setup

*** Test Cases ***
Run Scenarios
    ${contents}=    OperatingSystem.Get File    data.txt
    @{lines}=    String.Split to lines    ${contents}
    :FOR    ${line}    IN    @{lines}
            Log    ${line}    
    Log "done"

#64 UE Attach Detach Scenario
#    Copy Scenario File    "64_ue_attach_detach.cfg"
#    Run_scenario    64_ue_attach_detach.cfg    
#    Check_Ue_Status    "connected"
#    Check_Traffic    
#    Check_Ue_Status    "disconnected"   



*** Keywords ***
automation setup
   Check Setup Reachability
   Setup Bringup

Check Setup Reachability
    Is EPC Reachable
    Is ENB Reachable
    IS UE  Reachable

Setup Bringup
    EPC Node Bringup
    ENB Bringup
    Amarisoft UE Node Bringup

Teardown setup
    Collect Logs
    Clean_EPC
    Clean_ENB
    clean_UE
    


