#start automation 

#Remove before logs
rm -rf ../Logs/*
robot --outputdir  ../Logs/ ../tests/01_UE_Attach_Detach.robot
