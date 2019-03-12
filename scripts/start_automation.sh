#start automation 

#Remove before logs
rm -rf ../Logs/*
rm -rf ../lib/*.pyc
rm -rf ../config/*.pyc
robot --outputdir  ../Logs/ ../tests/01_SingleCeLL_OAM.robot
