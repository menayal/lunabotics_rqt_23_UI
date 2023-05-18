
# lunabotics_rqt_23_UI

This is the package that will hold all of the UI's components. 


# Install instructions

Clone this package into your src folder in your workspace:
	
 - Move into your src folder (if your workspace is named catkin_ws)
	 - `cd ~/catkin_ws/src/`
 - The src folder is where any and all packages you create or install are placed
 -	Install the package
	 -	HTTPS:
		 -	`git clone https://github.com/menayal/lunabotics_rqt_23_UI.git`
	 -	or SSH:
		 -	`git clone git@github.com:menayal/lunabotics_rqt_23_UI.git`
 -	Move back to your catkin_ws parent directory and run catkin_make
	 -	`cd ~/catkin_ws/`
	 -	`catkin_make`

The package is now installed


## View the UI

-  Make sure you have the associated robot code.
	- `~/catkin/ws/src`
	- Git clone this repo: https://github.com/GiovZa/wholeRobot     
	- `catkin_make`
- `roslaunch gen2bot allMotors.launch`
	- You will not get it running with no errors since you are not connected to the robot, but you can still run the code for development
-  `roslaunch lunabotics_rqt_23_UI viewUI.launch`


##  Directions on adding code

 - Make sure to branch away from main as soon as you install the package
	 - Make your branch name descriptive (aka what feature you are currently working on) and make sure to **add your name at the end of it**
	 - Commit and push code often
		 - Make your commit messages descriptive
 - Keep track of what helped you so people can use those resources in the future
 - Ask before merging
