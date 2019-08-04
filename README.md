# For Educational Purpose Only.

## First, let's procrastinate:
	https://www.youtube.com/watch?v=0jO-cFA09xU&feature=youtu.be

## Requirements:
	- (Ken's note) Open the realmofthemadgod in the right most ( small ) monitor 
	- (Ken's note) run terminal in the left most ( big ) monitor
	- Configure the config.py to fit screen size.
	- (On Mac) set `alias google-chrome="open -a 'Google Chrome'"

## Run:
	```
		For testing or running, configure "run.sh"
		then:	./run.sh

		For typical running, no debug 
			./grab_screen.py
	```

## Tips:
```
	detect mouse position on screen:
	python3:
		>> import pyautogui
		>> pyautogui.position()
```

## Code Smell:
	Keep in mind how the numpy+opencv capture screen and likes to do (x,y) => (y,x)
		But pyautogui uses the (x,y) pair

## Disclaimer
```
This software is for educational purpose, so that I can learn about opencv, numpy and pyautogui. If required, I will remove this from github on demand.
```
