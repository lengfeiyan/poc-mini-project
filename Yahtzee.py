"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_all_combinations(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                if new_sequence.count(item) == outcomes.count(item):
                    continue
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = {}
    for dummy_score in hand:
        if scores.has_key(dummy_score):
            scores[dummy_score] = scores[dummy_score] + 1
        else:
            scores[dummy_score] = 1
    max_value = 0
    for dummy_key in scores.keys():
        if dummy_key * scores[dummy_key] > max_value:
            max_value = dummy_key * scores[dummy_key]
    return max_value


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [dummy_i for dummy_i in range(1,num_die_sides+1)]
    all_seq = gen_all_sequences(outcomes,num_free_dice)
    total_score = 0.0
    count = 0.0
    for dummy_seq in all_seq:
        hand = list(dummy_seq)
        for dummy_score in list(held_dice):
            hand.append(dummy_score)
        total_score += score(hand)
        count += 1
    
    return total_score / count


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    length = len(hand)
    all_hold = set([()])
    for dummy_i in range(length):
        current_hold = gen_all_combinations(hand,dummy_i+1)
        for dummy_hold in current_hold:
            all_hold.add(tuple(sorted(dummy_hold)))
    
    return all_hold



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_hold = gen_all_holds(hand)
    max_value = 0.0
    max_value_hold = ()
    for dummy_hold in all_hold:
        value = expected_value(dummy_hold, num_die_sides, len(hand) - len(dummy_hold))
        if value > max_value:
            max_value = value
            max_value_hold = dummy_hold
    return (max_value, max_value_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    #num_die_sides = 6
    #hand = (1, 1, 1, 5, 6)
    #hand_score, hold = strategy(hand, num_die_sides)
    #print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    print expected_value((2, 2), 6, 2)
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



