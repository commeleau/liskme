# Scheduling script

For each segment get:
- round height
- get all voters
for each voter:
    - add account in mongo if needed
    - calculate k
    - calculate vote weight
    - add vote in mongo
meanwhile calculate round weight and calculate percentage for each vote so go next segment


this is the main algorithm.

## Run

this is the run function that control the loop

## parse_segment

it creates a segment and use the api to get votes and save it in mongo
