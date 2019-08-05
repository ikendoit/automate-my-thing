#!/usr/bin/env bash

type=$1
debug=FALSE

count=1;

while true; do

	if [ "$XDG_SESSION_DESKTOP" == "ubuntu" ]; then
		google-chrome https://www.realmofthemadgod.com
	else 
		open -a "Google Chrome" https://www.realmofthemadgod.com
	fi

	case $1 in
		'fight')
			DEBUG=$debug MODE=FIGHT ./grab_screen.py
			;;
		'login')
			DEBUG=$debug MODE=LOGIN ./grab_screen.py
			;;
		*)
			DEBUG=$debug MODE=LOGIN ./grab_screen.py
			;;
	esac

	if [ $? == "0" ]; then
		echo "finished, got the calendar, after $count tries"
		break;
	fi

	sleep 2
	((count=count+1))
done;
