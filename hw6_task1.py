import numpy as np
import random

# I'm representing the maze like this so it looks the same superficially
# I'm manually converting the coordinates when I transfer them into the table in the pdf
ogpolicy = [
    ["W", "S", "E", "GP"],
    ["N", "rock", "W", "GN"],
    ["E", "N", "W", "W"]
]

Left = {"N": "W", "W": "S", "S": "E", "E": "N"}
Right = {"N": "E", "E": "S", "S": "W", "W": "N"}
Back = {"N": "S", "S": "N", "E": "W", "W": "E"}


discount = 0.8

def reward(state):
    if state == "GP":
        return 1
    elif state == "GN":
        return -1
    else:
        return -0.04


# calculate the actual direction to go from the probability
def move_prob(instruction):
    r = random.random()

    # use the probability to find the relative direction, then the orientation to find the cardinal direction
    if r < 0.6:
        return instruction
    elif r < 0.8:
        return Left[instruction]
    elif r < 0.9:
        return Right[instruction]
    else:
        return Back[instruction]


# use the cardinal direction the agent should go and adjust position accordingly
def next_spot(position, direction):
    row, col = position

    if direction == "N":
        return (row - 1, col)
    if direction == "E":
        return (row, col + 1)
    if direction == "S":
        return (row + 1, col)
    if direction == "W":
        return (row, col - 1)
    

def validate(postition):
    row, col = postition

    # the agent can't phase through walls
    if row < 0 or row >= len(ogpolicy):
        return False
    if col < 0 or col >= len(ogpolicy[0]):
        return False
    
    # the agent also can't phase through the rock
    if ogpolicy[row][col] == "rock":
        return False
    
    return True


def stepitup(position):
    row, col = position

    # grab the direction the agent is supposed to go for this square
    intention = ogpolicy[row][col]

    if intention == "GP":
        return position, reward(position)
    elif intention == "GN":
        return position, reward(position)

    # calc the actual direction it will go
    actual = move_prob(intention)

    # find that new square
    proposed = next_spot(position, actual)

    # check to make sure it is a valid square
    if validate(proposed):
        new_position = proposed
    else:
        new_position = position

    prize = reward(new_position)

    return new_position, prize


def terminal(position):
    row, col = position
    return ogpolicy[row][col] in ("GP", "GN")


# In this case, (1, 1) is represented by (2, 0)
start_squares = [(0, 0), (0, 1), (0,2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3)]
utilities = []


for pos in start_squares:

    print(f"starting square {pos}")

    cumulative_reward = 0

    for i in range(10):
    
        while True:
            # run the trial and update the ersults
            pos, r = stepitup(pos)
            cumulative_reward += r
    
            # test for reaching the end, update the late reward since the earlier one doesn't seem to work
            if terminal(pos):
                if reward(pos) == 1:
                    cumulative_reward += 1
                else:
                    cumulative_reward += -1
                break
        
    final_reward = cumulative_reward/10
    utilities.append(final_reward)
    print(f"utility {round(final_reward, 4)}")
