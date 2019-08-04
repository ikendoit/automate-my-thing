# No one should see this.

## Requirements:
	Open the realmofthemadgod in the right most ( small ) monitor 
	run terminal in the left most ( big ) monitor

## Run:
	`(MODE=LOGIN|FIGHT) (DEBUG=TRUE|FALSE) ./grab_screen.py`

## Code Smell:
	Keep in mind how the numpy+opencv capture screen and likes to do (x,y) => (y,x)
		But pyautogui uses the (x,y) pair
