import random
import numpy as np
from pprint import pprint

# Updates beliefs according to Bayes' theorem
# Hypothesis: The door is at the given loc. Event: The door is reported to be at the given loc.
# P(H | E) = (P(E | H) * P(H)) / (P(H) * P(E | H) + P(-H) * P(E | -H))
# Initially: P(H) = 1 / room_l, P(-H) = 1 - P(H), P(E | H) = 1, P(E | -H) = 0
# Takes a dict representing P(H) for each location (beliefs), a float representing the trust in
# the user (trust), the int location of the agent (y), the int length of the room (room_l),
# and a string representing the user's input (check) yes or no
# Returns a modified version of the beliefs dict
def update_beliefs(beliefs, trust, y, room_l, check):
    for loc, prob in beliefs.items():
        if (loc != y):
            if (check == "yes"):
                if (prob == 0):
                    beliefs[loc] = 0
                else:
                    beliefs[loc] = 1 - (trust * prob) / (prob * trust + (1 - prob) * (1 - trust))
            elif (check == "no"):
                beliefs[loc] = (trust * prob) / (prob * trust + (1 - prob) * (1 - trust))
            else:
                print("Something went wrong (line 95")
                quit()
        elif (trust != 1):
            if (check == "yes"):
                if (prob == 0):
                    beliefs[loc] = 0
                else: 
                    if (prob == 0):
                        beliefs[loc] = 0
                    else: 
                        beliefs[loc] = 1 - (trust * prob) / (prob * trust + (1 - prob) * (1 - trust))
            elif check == "no":
                beliefs[loc] = (trust * prob) / (prob * trust + (1 - prob) * (1 - trust))
        # Normalize beliefs
        total = np.prod(sum(beliefs.values()))
        for loc in beliefs:
            beliefs[loc] = beliefs[loc] / total
    return beliefs

# Moves the agent one space up or down depending on its beliefs about where the door is located. The agent
# cannot move above the coordinate 1 or below the coordinate room_l
# Takes the ints room_l (the length of the room), y (the location of the agent), door (the location of the door),
# and the dict beliefs (each location in the room paired with the agent's belief about where the door is)
def agent_move(room_l, y, door, beliefs):
    max_belief = max(beliefs.values()) # Find the maximum belief value
    max_locations = [loc for loc, belief in beliefs.items() if belief == max_belief] # Find all locations with the maximum belief value
    if (y < max(max_locations)): # If the agent's current location is below the location(s) with the highest belief
        y += 1 # Move the agent up
    elif (y > min(max_locations)): # If the agent's current location is above the location(s) with the highest belief
        y -= 1 # Move the agent down
    if (y < 1): # Check if the agent is above the lowest coordinate
        y = 1 # If so, set the agent's location to the lowest coordinate
    elif (y > room_l): # Check if the agent is below the highest coordinate
        y = room_l # If so, set the agent's location to the highest coordinate
    return y


# Prints the simulated room marking the location of the agent (A), the door (D), 
# and the agent's beliefs about where the door is located in the room.
# Takes the room width, length, agent location, door location, and current belief
def print_room(room_l, y, door, beliefs):
    for i in range(1, room_l + 1):
        prob = beliefs.get(i)
        loc = " | " + str(prob) + " | "
        if i == y: 
            loc = loc + "A"
        if i == door: 
            loc = loc + "D" 
        print(loc)

def main():
    # Asks the user for the dimensions of the room and establishes initial trust in the user at 100%
    room_l = int(input("Enter the length of the room: "))
    door = int(input("Enter the location of the door: "))
    trust = 1

    # Randomly assign initial coordinates to the agent and tells the user what they are
    y = random.randint(1, room_l)
    print("Agent coordinates: ", y)
    print("Door coordinates: ", door)

    # Create initial belief about the door's location, where the probability of each coordinate is 1 / room_l
    # Each entry in the dict refers to a possible state the door could be in, and pairs that state with its probability
    beliefs = {}
    for i in range(1, room_l + 1):
        beliefs[i] = (1 / room_l)

    # Prompt the user after each of the agents' moves    
    while True:
        y = agent_move(room_l, y, door, beliefs)
        print_room(room_l, y, door, beliefs)
        check = str(input("Is the agent at the door? (yes/no) "))
        # The agent is certain the door is there
        if (beliefs.get(y) > 0.98):
            if (y == door):
                # The door is there
                print("The agent escaped!")
                quit()
            elif (check == "yes"):
                # The door is not there and the user said it was
                print("The agent knows you lied")
                if (trust >= 0.05):
                    trust = trust - 0.05
                else:
                    trust = 0.05
                beliefs[y] = 0
            elif check == "no":
                # The door is not there and the user said it wasn't
                print("You tricked the agent!")
                quit()
            else:
                print("Something went wrong (line 95)")
                quit()
        # The agent trusts the user completely
        elif (trust == 1):
            if (check == "yes"):
                if (y == door):
                    # The door is there
                    print("The agent escaped!")
                    quit()
                else:
                    # The door is not there and the user said it was
                    print("The agent knows you lied")
                    if (trust >= 0.05):
                        trust = trust - 0.05
                    else:
                        trust = 0.05
                    beliefs[y] = 0
            elif (check == "no"):
                beliefs[y] = 0
            else:
                print("Something went wrong (line 95)")
                quit()
        beliefs = update_beliefs(beliefs, trust, y, room_l, check)

if __name__ == '__main__':
    main()