*** Variables ***
#Login Credentials for EPC,UE and Board
${EPC}            172.27.22.71
${EPC_USER}       root
${EPC_PASS}       root123
${Board}          172.27.22.157
${BD_USER}        root
${BD_PASS}        root123
${UE}             172.27.22.201
${UE_USER}        root
${UE_PASS}        toor
${VS_IP}          172.27.22.156
${VS_PASS}        root123
${UE}             1
#Single Cell or CA for Board configurations
${CELL}           Single_Cell
#OAM configurations on Board
${OAM}            YES
#Mode FDD/TDD default FDD
${MODE}           FDD
#UE configurations
${UE_path}        /root/ue/config
${Config_path}    ../Config
${UE_File}        ue_64.cfg
${Traffic_Type}   "uplink"
#Logs path
${L2_LOG_PATH1}         /root/l2.log
${L2_LOG_PATH2}         /root/rsys/setup/trace/dbgLog*
${L2_LOG_PATH3}         /var/log/*
${L2_LOG_PATH4}         /root/ue/ue_console.log
${L2_LOG_PATH5}         /tmp/ue0.log
${TARGET_PATH}          ../Logs/

