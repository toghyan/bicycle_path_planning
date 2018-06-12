This program is for simulating the dynamics of a simple bicycle models in ral-time. To implement 
this program I developed Bicycle_sim class that runs the simulation with related dynamics. The 
run_simulation method runs the main loop of the simulation, and it is called in the main.cpp file. 
Instances of Bicycle_sim are initialized using the initial conditions in the initial.txt file included 
in the package. The initial conditions can be changed to best fit the desired conditions. The variables 
are stored in a vectors and the values at the instant of current time are also stored for simplicity.
The simulation runs with a 50 Hz frequency. To calculate the next value of each variable, a rectangle 
(linear) approximation is used.

User input:

	‘j’ : decrements the velocity by 0.1 m/s (down to 0 m/s)

	‘k’ : increments the velocity by 0.1 m/s (up to 12m/s)

	‘l’ : decrements the steering angle rate by 0.1 rad/s (down to -PI/4)

	‘h’ : increments the steering angle rate by 0.1 rad/s (up to PI/4)

	‘s’ : save the outputs to file

	'q' : stops the simulation and exits the program

	The code can be modified to display the users inputs.

Saved file:

	saved files have the format of "log_simXXXX.txt", where "XXXX"
	represents the counter for the log files. It stores values
	from the last time 's' was pressed or the last 10 seconds, 
	whichever is smaller. Each line of the log files contains the 
	following information:

	timestamp in seconds
	x and y position of the rear tire in meters
	x and y position of the front tire in meters
	angle of the body with respect to horizon in radians
	steering angle in radians
	velocity of the bicylce in meters per second
	rate of change of the steering angle in radians per second

	These are comma seperated.

ncurses library:
	
	The program utilizes ncurses library to interact with the user 
	and get input commands. ncurses is a linux exclusive library, 
	and depending on the linux version, it might not be already 
	installed. To make sure ncurses is installed type the following 
	command in your Terminal:

	'sudo apt-get install libncurses5-dev libncursesw5-dev'


Building:

	The Makefile is included in the package. In order to build the 
	program, in your terminal, navigate to the directory where the 
	package is stored and type 'make'

Running: 

	To run the simulation, after building, type './output' in your 
	terminal