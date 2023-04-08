#!/bin/bash
# Script to install mysql on linux
# By: Shoaib wani
# version: 0.01

# different colos
function prRed() {
	echo -ne "\033[91m"$1"\033[00m"
}

function prGreen() {
	echo -ne "\033[92m"$1"\033[00m"
}

function prYellow() {
	echo -ne "\033[93m"$1"\033[00m"
}

function prBlue() {
	echo -ne "\033[94m"$1"\033[00m"
}



prGreen '[+] Installing Mariadb-Client & Mariadb-Server\n'

# installing mariadb client&server
sudo apt instal mariadb-client mariadb-server > /dev/null 2>&1

if [[ $? -eq 0 ]]
then
	prGreen '[+] Installation Complete\n'
	prBlue '[+] Starting mysql\n'
	systemctl tart mysql > /dev/null 2>&1

	if [[ $? -eq 0 ]]
	then
		prGreen '[+] Started ...\n'
		prYellow '[-] Enjoy!\n'
	else
		prRed '[x] Error while starting Mysql\n'
		prYellow '[help] Try running : systemctl start mysql\n'
	fi
else
	prRed '[x] Couldnt Install mariadb\n'
	prYellow '* Try running : '
	prBlue 'sudo apt install mariadb-client mariadb-server\n'
	prYellow '* then run : '
	prBlue 'systemctl start mysql\n'
fi