#include <stdio.h>
#include <time.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include "Bicycle_sim.h"

using namespace std;

int main(int argc, char **argv)
{
    Bicycle_sim sim;
    sim.run_simulation();
    return 0;
}
