Simple replication of the hallway problem using Bayes' theorem with a twist

The user decides the length of the hallway, and responds to prompts from the agent about the actions the agent has taken. 
Responses to prompts from the agent will only be as reliable as the user decides, so the transition probability of the move action is hidden from 
the agent, and only the user knows if they are making true or false statements. 

The agent knows:
- The length of the hallway
- The transition probability of the move action
- Its own location in the hallway

The agent doesn't know:
- The location of the door
- The transition probability of the check action (because the user decides the result of the agent's actions)

The agent can take the move action, which will move it one space to the left or right, but only the user will know the agent's actual location.
The agent can also check if there is a door in its current space, which will prompt the user to respond with "yes" or "no". Whether or not the
user's response is true is up to them, so the probability of the check action succeeding is an unknown variable. 

This version has unused elements intended for a 2d room problem instead of a 1d hallway.

The first time the user inputs an answer to the check function, the agent will trust them completely. If the answer is "no", then the beliefs
about the door will update accordingly. If the answer is "yes" and is true, the game ends, but if it tries to go through a door and fails, the 
trust probability will change.