#start automation 

#Remove before logs
rm -rf ../logs/*
rm -rf ../lib/*.pyc
rm -rf ../config/*.pyc
robot --outputdir  ../logs/ -t "Setup Bringup" ../tests/01_SingleCeLL_OAM.robot
robot --outputdir  ../logs/ -t "1 UE Attach Detach without any interval" ../tests/01_SingleCeLL_OAM.robot
