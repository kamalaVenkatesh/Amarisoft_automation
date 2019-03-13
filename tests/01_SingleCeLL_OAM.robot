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
    UE Node Bringup
#    ENB Node Bringup with Single Cell and with OAM

1 UE Attach Detach without any interval
    UE Attach Detach Scenario    file=1_ue_attach_deatch.cfg    N_ue=1    	

32 UE Attach Detach with interval 10s
    UE Attach Detach Scenario    file=1_ue_attach_deatch.cfg    N_ue=1    Interval=10

64 UE Attach Detach with interval 30s
    UE Attach Detach Scenario    file=1_ue_attach_deatch.cfg    N_ue=1    Interval=30

1 UE Attach Detach with uplink udp data
    UE Attach Detach and Data Scenario    file=1_ue_attach_deatch.cfg    N_ue=1    type=uplink    proto=udp    data=512k

1 UE Attach Detach with uplink tcp data
    UE Attach Detach and Data Scenario    file=1_ue_attach_deatch.cfg    N_ue=1    type=uplink    proto=tcp    data=512k

1 UE Attach Detach with downlink udp data
    UE Attach Detach and Data Scenario    file=1_ue_attach_deatch.cfg    N_ue=1    type=downlink    proto=udp    data=512k

1 UE Attach Detach with uplink tcp data
    UE Attach Detach and Data Scenario    file=1_ue_attach_deatch.cfg    N_ue=1    type=downlink    proto=tcp    data=512k



