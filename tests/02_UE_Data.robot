** Settings ***
Documentation     test2
Library           SSHLibrary
Library           OperatingSystem
Library           Process
Library           String
Resource          Keywords.robot
Resource          variables.robot

*** Test Cases ***
64 ue attach detach
    Log done

Run Scenarios
    ${contents}=    OperatingSystem.Get File    data.txt
    @{lines}=    String.Split to lines    ${contents}
    :FOR    ${line}    IN    @{lines}
            Log    ${line}
    Log done

