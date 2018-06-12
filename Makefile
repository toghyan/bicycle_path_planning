output: main.o Bicycle_sim.o
	g++ main.o Bicycle_sim.o -o output -lncurses

main.o: main.cpp
	g++ -c main.cpp 

Bicycle_sim.o: Bicycle_sim.cpp Bicycle_sim.h
	g++ -c Bicycle_sim.cpp

clean:
	rm *.o