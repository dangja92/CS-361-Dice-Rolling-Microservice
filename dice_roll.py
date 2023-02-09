from random import randint, seed
from datetime import datetime

# create dictionary to look up the upper value of each die based on its index position
# eg. 0 : d4, 1 : d6, 2 : d8, 3 : d10, etc...
dice_upperval = {
    0 : 4,
    1 : 6,
    2 : 8,
    3 : 10,
    4 : 12,
    5 : 20,
    6 : 100,
}

def dice_roll(dice_array):
    '''
    
    dice_array : [List][int] - the number of dice for each position (d4, d6, d8, d10, d12, d20, d100)
    return: [List][List][int] - an array of int arrays for each randomized die roll, for any number of dice 
    within dice_array > 0
    '''
    seed(datetime.now().timestamp())
    
    final_dice_array = []
    for index, num_dice in enumerate(dice_array):
        
        curr_dice_array = []    # this holds the roll result for a particular die (eg. d20)
        
        # if die == 0, no roll is needed, append an empty array for that index position to final_dice_array, and continue
        if num_dice == 0:
            final_dice_array.append(curr_dice_array)
            continue
        
        for roll in range(num_dice):
            curr_dice_array.append(randint(1, dice_upperval[index]))
            
        final_dice_array.append(curr_dice_array)
    
    return final_dice_array

