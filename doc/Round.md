# Round.py

This package models the mongo entities providing a easy interface to the database


## Account
 
Represent a single account in order to reference all votes. It can be maybe removed for access improvement

## Vote 

The vote registered with reference to account and round. Moreover it has the kappa coefficient, the amount of the wallet of the relative account
 the weight (coefficient * amount), the percentage inside the round, and if he has voted
 
## Round

Information about the round as height, end, weight, date and (not yet implemented) the forged coins in the round.
