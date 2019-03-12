#start automation 

#Remove before logs
rm -rf ../logs/*
rm -rf ../lib/*.pyc
rm -rf ../config/*.pyc
robot --outputdir  ../logs/ ../tests/01_SingleCeLL_OAM.robot
