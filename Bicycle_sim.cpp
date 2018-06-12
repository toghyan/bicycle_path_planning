#include "Bicycle_sim.h"

Bicycle_sim::Bicycle_sim()
{
    initialize();
}

Bicycle_sim::~Bicycle_sim()
{
    
}

void Bicycle_sim::initialize(){
    
    ifstream myfile("initial.txt");
    if (myfile.is_open()){
        
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
        throw("Could not open initial.txt file");
    }
    
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
    noecho();
    scrollok(stdscr, TRUE);
    nodelay(stdscr, TRUE);
    bool loop = TRUE;
    while (loop){
    	clock_t start = clock();
    	char input = getch();
    	switch(input){
    		case 'j':	if(vel > 0) vel -= 0.1;
    					break;

    		case 'k':	if(vel <= 11.9) vel += 0.1;
    					break;

    		case 'l':	if(steering_rate > - M_PI_4) steering_rate -= 0.1;
    					if(steering_rate < - M_PI_4) steering_rate = - M_PI_4;
    					break;

    		case 'h':	if(steering_rate < M_PI_4) steering_rate += 0.1;
    					if(steering_rate > M_PI_4) steering_rate = M_PI_4;
    					break;

    		case 's':	save();
    					break;

    		case 'q':	loop = FALSE;
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
    endwin();
}

void Bicycle_sim::next_step(){
    
    time_passed += dt;
    time_vec.push_back(time_passed);
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
    myFile.open(file_name.c_str());
    int size = vel_vec.size();
    if(size - last_save < 501){
    	for(int it = last_save; it < size; it++){
    		myFile << time_vec[it] << ", " << xr_vec[it] << ", " << yr_vec[it] 
    		<< ", " << xf_vec[it] << ", " << yf_vec[it] << ", " << theta_vec[it]
    		<< ", " << delta_vec[it] << ", " << vel_vec[it] << ", " << s_vec[it] 
    		<< endl;
    	}
    } 
    else {
    	for(int it = size - 501; it < size; it++){
    		myFile << time_vec[it] << ", " << xr_vec[it] << ", " << yr_vec[it] 
    		<< ", " << xf_vec[it] << ", " << yf_vec[it] << ", " << theta_vec[it]
    		<< ", " << delta_vec[it] << ", " << vel_vec[it] << ", " << s_vec[it] 
    		<< endl;
    	}

    }

    myFile.close();
    last_save = size;
	saves_num++;
}


