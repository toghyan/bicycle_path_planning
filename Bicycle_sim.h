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
    Bicycle_sim();
    ~Bicycle_sim();
    void run_simulation();
    
    
private:
    vector<double> xr_vec, yr_vec, theta_vec, delta_vec, vel_vec, s_vec, xf_vec, yf_vec, time_vec;
    double xr, yr, theta, delta, vel, steering_rate, time_passed;
    int last_save, saves_num;
    static const double l = 2.5;
    static const double dt = 0.02;
    
    void initialize();
    void next_step();
    void save();
};

#endif // BICYCLE_SIM_H
