*** Variables ***
#Login Credentials for EPC,UE and Board
${EPC}            172.27.1.207
${EPC_USER}       labadmin
${EPC_PASS}       root123
${Board}          172.27.1.200
${BD_USER}        root
${BD_PASS}        ""
${UE}             172.27.22.201
${UE_USER}        root
${UE_PASS}        toor
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
