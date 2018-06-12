/*
 * This file is the header for Bicycle_sim class.
  *
 * Author : Aliakbar Toghyan
 */
#ifndef BICYCLE_SIM_H
#define BICYCLE_SIM_H

#define _USE_MATH_DEFINES

#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <time.h>
#include <ncurses.h>
#include <iomanip>
#include <sstream>


using namespace std;

class Bicycle_sim
{
public:
	// constructor of the bicycle simulation class
    Bicycle_sim();
    // deconstructor 
    ~Bicycle_sim();
    // This method runs the main loop of the simulation
    void run_simulation();
    
    
private:
	// vector of variables for storage purposes They all have the same size
    vector<double> xr_vec;
    vector<double> yr_vec;
    vector<double> theta_vec;
    vector<double> delta_vec;
    vector<double> vel_vec;
    vector<double> s_vec;
    vector<double> xf_vec; 
    vector<double> yf_vec; 
    vector<double> time_vec;

    // values of variables at the current moment 
    double xr; 
    double yr;
    double theta;
    double delta;
    double vel;
    double steering_rate;
    double time_passed;

    // index of the vectors, where 's' was hit last
    int last_save;
    // number of log files. For naming the log file 
    int saves_num;

    // length of the bicycle
    static const double l = 2.5;
    // delta of time. Equal to frequency of 50 Hz.
    static const double dt = 0.02;

    // Initializes values and reads initial conditions from "initial.txt"
    void initialize();
    // Calculates the variables in the next step of the simulation
    void next_step();
    // saves the variables in the desired format
    void save();
};

#endif // BICYCLE_SIM_H
