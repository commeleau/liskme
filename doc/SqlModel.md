# Modelisation of postgres database

This package is going to change a lot since query performance are not adeguate using modelisation.

Btw is nice to have a view on the important table of the blockchain.

We assume all information are trustworthly since handled by lisk client

## Block

The block is the main entity representing a group of transactions. Every 101 group it happens a Round.
We will calculate the status for each Round so every 101 blocks

## Transaction

Rapresent a single transaction with senderId and recipientId. A transaction can also rapresent a vote
and are used to calculate the amount of lisk owned by one account

## Vote

A vote is a list of account delegate with + or - defining the vote gived by one account. The vote is related to a transaction
so that is defined the block and the senderId.


in vote there is the main query function

### get_votes_for_delegate_before_block

This function aim to reduce the number of query called. Still in development environment is quite slow. Maybe some improvements can be done.

It collect all votes and for every vote the transaction relative and the outcome and income for the relative account.
Like this it won't be required to use any other query.
