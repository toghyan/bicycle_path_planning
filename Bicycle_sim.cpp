/*
 * This file contains the implementation of the Bicycle_sim class.
 *
 * Author : Aliakbar Toghyan
 */
#include "Bicycle_sim.h"

Bicycle_sim::Bicycle_sim()
{
    initialize();
}

Bicycle_sim::~Bicycle_sim()
{
    
}

void Bicycle_sim::initialize(){
    // reading initial conditions from initial.txt
    ifstream myfile("initial.txt");
    if (myfile.is_open()){
        
        // storing initial values
        myfile >> xr;
        xr_vec.push_back(xr);
        myfile.ignore();
        myfile >> yr;
        yr_vec.push_back(yr);
        myfile.ignore();
        myfile >> theta;
        theta_vec.push_back(theta);
        myfile.ignore();
        myfile >> delta;
        delta_vec.push_back(delta);
        
        myfile.close();
    } 
    else {
        throw("Could not open initial.txt");
    }
    // initializing variables 
    steering_rate = 0;
    s_vec.push_back(steering_rate);
    time_passed = 0;
    time_vec.push_back(time_passed);
    vel = 0;
    vel_vec.push_back(vel);
    last_save = 0;
    saves_num = 0;
}

void Bicycle_sim::run_simulation(){
	// Initiallizing the keyboard interactions
    initscr();
    cbreak();
    // this could be modified to display keyboard inputs on terminal
    noecho();
    scrollok(stdscr, TRUE);
    nodelay(stdscr, TRUE);
    // variable for while loop
    bool loop = TRUE;
    while (loop){
    	// using this to make sure the loop runs in real time
    	clock_t start = clock();
    	// detecting keyboard input
    	char input = getch();
    	switch(input){

    		case 'j':	if(vel > 0) vel -= 0.1;
    					break;

    		case 'k':	if(vel <= 11.9) vel += 0.1;
    					break;

    		case 'l':	if(steering_rate > - M_PI_4) steering_rate -= 0.1;
    					// this statement is because pi/4 is not divisible by 0.1
    					if(steering_rate < - M_PI_4) steering_rate = - M_PI_4;
    					break;

    		case 'h':	if(steering_rate < M_PI_4) steering_rate += 0.1;
    					// this statement is because pi/4 is not divisible by 0.1
    					if(steering_rate > M_PI_4) steering_rate = M_PI_4;
    					break;

    		case 's':	save();
    					break;

    		case 'q':	loop = FALSE;	// exits the while loop
    					break;

    		default:	break;
    	}
    	// doing the next iteration of the simulation
    	next_step();
    	// making sure the loopis running in real-time
    	double elapsedTime = 0;
    	while (elapsedTime < dt){
        	elapsedTime = (double)(clock() - start) / CLOCKS_PER_SEC;
    	}
    }
    // closing the window
    endwin();
}

void Bicycle_sim::next_step(){
    // incrementing time and storing time stamp
    time_passed += dt;
    time_vec.push_back(time_passed);
    // calculating variables and storing them
    xr += vel * cos(theta) * dt;
    xr_vec.push_back(xr);
    yr += vel * sin(theta) * dt;
    yr_vec.push_back(yr);
    theta += vel * tan(delta) * dt / l;
    theta_vec.push_back(theta);
    delta += steering_rate * dt;
    delta_vec.push_back(delta);
    vel_vec.push_back(vel);
    s_vec.push_back(steering_rate);
    xf_vec.push_back(xr + l * cos(theta));
    yf_vec.push_back(yr + l * sin(theta));
    
}

void Bicycle_sim::save(){
	// setting up the name of the text file 
    ostringstream ss;
    ss << setw(4) << setfill('0') << saves_num;
    string file_name = "sim_log" + ss.str() + ".txt";
    ofstream myFile; 
    // initialing the log file 
    myFile.open(file_name.c_str());

    int size = vel_vec.size();
    // less than 10 seconds from last save
    if(size - last_save < 501){
    	for(int it = last_save; it < size; it++){
    		myFile << time_vec[it] << ", " << xr_vec[it] << ", " << yr_vec[it] 
    		<< ", " << xf_vec[it] << ", " << yf_vec[it] << ", " << theta_vec[it]
    		<< ", " << delta_vec[it] << ", " << vel_vec[it] << ", " << s_vec[it] 
    		<< endl;
    	}
    } 
    // more than 10 seconds from last save
    else {
    	for(int it = size - 501; it < size; it++){
    		myFile << time_vec[it] << ", " << xr_vec[it] << ", " << yr_vec[it] 
    		<< ", " << xf_vec[it] << ", " << yf_vec[it] << ", " << theta_vec[it]
    		<< ", " << delta_vec[it] << ", " << vel_vec[it] << ", " << s_vec[it] 
    		<< endl;
    	}

    }
    // closing the file
    myFile.close();
    // updating save-related variables
    last_save = size;
	saves_num++;
}


