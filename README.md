# NEAT_Python
Simple implementation of the NEAT algorithm to a platform game made using pygame. 

* config.txt contains the NEAT details
* modelo1.py is the main python script
* resize.py is a script used to resize the images so they fit inside the game

The goal of the game is for each player to get to the coin without touching the spikey ball. 
The way I did this is by rewarding them two times and punishing them two times as well: 
* small reward when they get the cookie
* big reward when they get the coin
* small punish when they get hit by the ray
* big punish when they get hit by the ball

What I found is the most optimal way is to have the reward of the cookie and the punishment of the ball to have a positive sum. What I mean by this is that each player is encouraged to jump and hit the ball, but it is even more encouraged to jump and NOT hit the ball. Both actions are necessary to the process of getting to the coin.
