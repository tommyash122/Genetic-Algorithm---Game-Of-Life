# Genetic-Algorithm---Game-Of-Life

## About
The algorithm is a genetic algorithm that interfaces with the legality of John Conway's Game of Life and finds different
forms of beings called Methuselah according to the one given to them by Conway's Game.       

Game of life - A genetic algorithm that work with the Roulette wheel  selection and select an individual to insert to the running process thus creating a stable, strong and diverse environment of population.
( Tkinter , Python )

Link to a video that comprehensively explains the code and all its functions and components:    
https://youtu.be/7BiEzkHaChk    

**Check out the [algorithm's behavior](#Data-and-conclusions) that 6000 generations run shows.**

## System requirements 
Python 3.4 and above installed.

screen shot of stage 170 generation 19/20:
![3](https://user-images.githubusercontent.com/84855441/203360903-d79a0b62-05f4-45f4-a823-e3097e036eb7.PNG)

## Explanation
We will provide an explanation of how the algorithm works and the elements included in it:
When running the algo, a window opens showing a black image and a random distribution of some cells in the form of green squares (initial color), this is the initial configuration of our metoshal.   

#### window's definition:
Our window contains a two-dimensional matrix of a size determined by the user and inside it will be cells.    

#### cell's definition:
A black cell will be marked as DEATH cell.    
A non-black colored cell will be marked as a LIFE cell.    
A dead cell has no special function and is simply dead until it is resurrected.    
A living cell has a role, a living cell functions as a cell supported by all 8 of its direct neighbors in a 3x3 matrix around which we will call M.    
If there are 4 or more living cells in M ​​or 1 or less living cells, our cell will die.
Otherwise, if M has between 2 and 3 live cells, this is a different situation.
If there are 2 live cells in M ​​and our cell is alive then it will remain alive and if it is dead then it will remain dead.
If there are 3 living cells in M ​​and our cell is alive then it will stay alive and if it dies then it will become alive (be born).
In accordance with this rules, each cell scans the matrix of its neighbors M and checks the conditions regarding it and according to them in each generation moves to its appropriate state.

![aaaa](https://user-images.githubusercontent.com/84855441/203363555-f789b635-38c2-4d6a-a10b-875155a78be2.PNG)    


#### stage definition:
Our algo run is divided into generations and stages, a stage is a number of generations that we need to run our current configuration to store enough data to be used for details that we would like to insert into our window.
At each stage we set 20 generations to run (can be changed by the user) and with each generation that passes we scan the window and look for as many eligible individuals as possible that have evolved, as soon as such a individual is identified we will save it in a set of data, we will code it with a string of 0 and 1 when 0 is dead and 1 live.
At the end of running the defined number of generations, we accumulated a number of people of individuals eligible for insertion into the next stage, individuals were selected from among them using the roulette wheel selection roulette method and we will insert it in a random position in the window that will mix with the given state of this matching.    
At each stage transition we will change the color of the cells.

#### generation definition:
In each generation, the entire window will be scanned, we will look for additional details in the conditions of an organism, which will be detailed later, and at the end of the generation, the window will be updated according to the stage, any suitable ones died and any suitable ones were born, and so on.    

#### individual definition:
For the object "individual" I chose to call it an organism.
Our organism is defined to be in its initial state a group of at least 20 living cells spread over an area of ​​a 7x7 matrix 'M'. Going through each and every cell, this matrix 'M' will be scanned and if it finds an organism that meets the conditions, we will keep it and during the transition over the next 100 cells, we will not try to extract another organism because if we scan in cells too close to each other, we are approximately two very overlapping organisms in which almost all the cells are identical.
Any organism that meets the condition will be encoded into a 49 character string of 0's and 1's where 0 is dead and 1 is alive.    

#### fitness of an organism definition:
Definition of fitness as a measure of the dispersion ratio of the adaptation within the organism to the appropriate amount.
The qualification value will be a value between 0 and 1 where 0 is not qualified and 1 is maximally qualified.
From the basic assumption that an organism should contain at least 20 live cells in a 7x7 area, that is, out of 49 possible options based on the legal definitions of the game of life, it can be concluded that high densities or low densities does not bring with it a high chance of giving birth to new live cells.
From here I assumed that a balanced density is the key, the string of our organism will be checked once we omit the 0 (dead) cells and check how suitable we are living next to each other.    
The more places with single live cells there are in our string after subtracting the zeros, the higher our fitness level will be.    
We will divide the number of places containing 1 in our string by the total number of living cells and we will get the desired degree of fitness.    

#### Total windows fitness definition:
The fitness of the whole window is determined according to how many live cells there are in total in each generation.


## Data and conclusions

Below is a graph of the fitness values ​​throughout the running of the algorithm for a length of 6000 generations.
It can be seen in this graph that there are many points of increase and decrease, but throughout the entire period of operation there was at least one living cell.
The graph is a graph of the generation as a function of the total number of living cells in that generation, it can be seen that there is an upward trend shown as a red linear line crossing the graph along its length.

![image](https://user-images.githubusercontent.com/84855441/203370335-8abc39bd-7e88-4439-bca3-779b3750a583.png)    

A bit of numerical data for the above experiment is now presented:    
MIN VALUE = 6    
MAX VALUE = 284    
MEDIAN = 150    
AVERAGE = 141.774    
The maximum value is obtained in the 4328th generation, The minimum can be proven to be preserved for 364 generations approximately from generation ~183 to ~490 and from there it climbs back up.    
As I mentioned earlier, the competence index rises and falls sharply throughout the entire period of the experiment, but the most noticeable increase occurs from generation ~490 approximately to approximately ~1038, which is an increase from an array of 12 living cells to a value of 267 living cells in approximately ~550 generations, a 22.25-fold increase in the amount of cells Life.    
The reason for that is, according to looking at the graph, it is possible to learn about the period of these generations when there were very few organisms scattered throughout the window area, during the routine scan in order to search for organisms that meet the conditions, every time we come across an organism we will save it.    
In a step stage, we will insert the one that was chosen in a random position in the window until we insert it in a precise position that will result in a good match with the other individuals that already exist in the window, accordingly, it will lead to the proliferation of the cells and organisms in general in the window,
#### thus creating a strong and stable diverse population that in each generation will give birth to a sufficient amount of cells that will maintain its stability over time.    

 # Final conclusion: 
 # Genetic Algorithms are freakin awesome
![2002718273chemistry-atom-proton-electron-animation-17](https://user-images.githubusercontent.com/84855441/203532946-518079d6-7c3f-4cac-ba6e-00552689bdbd.gif)





