# Handler to parse the database

These classes doesn't represent entities on database but are used to extract better the information about round


## LiskAccount

An account that vote and has an amount of lisk. It expose the method vote that acquire a Vote object and set if is voting or not.


## Segment

Considering it as a cluster of blocks, it process the votes from the blocks. It also allows to get the amount for account but is now deprecated for a big query



