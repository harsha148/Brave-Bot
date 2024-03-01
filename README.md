# Brave-Bot
You are the space roomba on a deep space salvage vessel, and your best friend is the captain. Its just the two of you
out here, against the world / the innite void of space. Unfortunately your ship has been boarded by aliens. The
captain is hiding under the oor panels, but its up to you to get to them and teleport you both to safety- avoiding
the aliens as you do.
For this task we have introduced five different bots which use different algorithms to succeed the task.

We have written different commands for running the bots individually or together and generating graphs to compare across 
different metrics.
All the metrics we have generated are simulated using a ship dimension 30*30, the number of aliens over the range (0,200), unless specified. 

Unzip the project, open terminal in the /Brave-Bot/Brave-Bot folder
The command for running the bots individually:
BOT 1 :  python3 main.py bot1 --ship_size=30 --k_min=0 --k_max=200 --k_step=1
BOT 2 :  python3 main.py bot2 --ship_size=30 --k_min=0 --k_max=200 --k_step=1
BOT 3 :  python3 main.py bot3 --ship_size=30 --k_min=0 --k_max=200 --k_step=1
BOT 4 :  python3 main.py bot4 --ship_size=30 --k_min=0 --k_max=200 --k_step=1
BOT 5 :  python3 main.py bot5 --ship_size=30 --k_min=0 --k_max=200 --k_step=1
Comparing the bots:
Compare BOT 1, BOT 2, BOT 3: python3 main.py bot123 --ship_size=30 --k_min=0 --k_max=200 --k_step=1
Compare BOT 1, BOT 2, BOT 3, BOT 4: python3 main.py all_bots --ship_size=30 --k_min=0 --k_max=200 --k_step=1
Compare BOT 1, BOT 2, BOT 3, BOT 5 with a time constraint: python3 main.py time_constraint --ship_size=30 --k_min=0 --k_max=200 --k_step=1 --time_constraint=0.0005

Description of the arguments:
ship_size: The dimension of the ship layout
k_min: The minimum value of K(number of aliens) in the range of K
k_max: The maximum value of K(number of aliens) in the range of K
k_step: The step size of values of K
time_constraint: The time constraint for the bot step
