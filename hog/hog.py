"""CS 61A Presents The Game of Hog."""

from math import sqrt

from dice import four_sided, make_test_dice, six_sided
from ucb import interact, main, trace

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, "num_rolls must be an integer."
    assert num_rolls > 0, "Must roll at least once."
    # BEGIN PROBLEM 1
    outcomes = [dice() for _ in range(num_rolls)]
    return sum(outcomes) if (1 not in outcomes) else 1
    # END PROBLEM 1


def oink_points(player_score, opponent_score):
    """Return the points scored by player due to Oink Points.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """
    # BEGIN PROBLEM 2
    tens = (opponent_score // 10) % 10
    ones = opponent_score % 10
    return max(1, 2 * tens - ones)
    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice,
    which may be 0 in the case of a player using Oink Points.
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    goal:            The goal score of the game.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, "num_rolls must be an integer."
    assert num_rolls >= 0, "Cannot roll a negative number of dice in take_turn."
    assert num_rolls <= 10, "Cannot roll more than 10 dice."
    assert max(player_score, opponent_score) < goal, "The game should be over."
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return oink_points(player_score, opponent_score)
    return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def is_prime(n):
    if n == 2:
        return True
    elif n % 2 == 0:
        return False
    i = 3
    while i <= sqrt(n):
        if n % i == 0:
            return False
        i += 2
    return True


def pigs_on_prime(player_score, opponent_score):
    """Return the points scored by the current player due to Pigs on Prime.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """
    # BEGIN PROBLEM 4
    additional_points = 0
    if is_prime(player_score):
        while True:
            additional_points += 1
            if is_prime(player_score + additional_points):
                break
    return additional_points
    # END PROBLEM 4


def next_player(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> next_player(0)
    1
    >>> next_player(1)
    0
    """
    return 1 - who


def silence(score0, score1, leader=None):
    """Announce noehing (see Phase 2)."""
    return leader, None


def play(
    strategy0,
    strategy1,
    score0=0,
    score1=0,
    dice=six_sided,
    goal=GOAL_SCORE,
    say=silence,
):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call every turn.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    leader = None  # To be used in problem 7
    # BEGIN PROBLEM 5
    while True:
        if who == 0:
            score0 += take_turn(strategy0(score0, score1), score0, score1, dice, goal)
            score0 += pigs_on_prime(score0, score1)
        else:
            score1 += take_turn(strategy1(score1, score0), score1, score0, dice, goal)
            score1 += pigs_on_prime(score1, score0)
        who = next_player(who)
        # END PROBLEM 5
        # (note that the indentation for the problem 7 prompt (***YOUR CODE HERE***) might be misleading)
        # BEGIN PROBLEM 7
        leader, message = say(score0, score1, leader)
        if message:
            print(message)
        if score0 >= goal or score1 >= goal:
            break
    # END PROBLEM 7
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1, player=None):
    """A commentary function that announces the score for each player."""
    message = f"Player 0 now has {score0} and now Player 1 has {score1}"
    return player, message


def announce_lead_changes(score0, score1, last_leader=None):
    """A commentary function that announces when the leader has changed.

    >>> leader, message = announce_lead_changes(5, 0)
    >>> print(message)
    Player 0 takes the lead by 5
    >>> leader, message = announce_lead_changes(5, 12, leader)
    >>> print(message)
    Player 1 takes the lead by 7
    >>> leader, message = announce_lead_changes(8, 12, leader)
    >>> print(leader, message)
    1 None
    >>> leader, message = announce_lead_changes(8, 13, leader)
    >>> leader, message = announce_lead_changes(15, 13, leader)
    >>> print(message)
    Player 0 takes the lead by 2
    """
    # BEGIN PROBLEM 6
    score_diff = abs(score0 - score1)
    if score0 > score1 and (last_leader == 1 or last_leader is None):
        leader, message = 0, f"Player 0 takes the lead by {score_diff}"
    elif score1 > score0 and (last_leader == 0 or last_leader is None):
        leader, message = 1, f"Player 1 takes the lead by {score_diff}"
    else:
        leader, message = None if score0 == score1 else last_leader, None

    return leader, message
    # END PROBLEM 6


def both(f, g):
    """A commentary function that says what f says, then what g says.

    >>> say_both = both(say_scores, announce_lead_changes)
    >>> player, message = say_both(10, 0)
    >>> print(message)
    Player 0 now has 10 and now Player 1 has 0
    Player 0 takes the lead by 10
    >>> player, message = say_both(10, 8, player)
    >>> print(message)
    Player 0 now has 10 and now Player 1 has 8
    >>> player, message = say_both(10, 17, player)
    >>> print(message)
    Player 0 now has 10 and now Player 1 has 17
    Player 1 takes the lead by 7
    """

    def say(score0, score1, player=None):
        f_player, f_message = f(score0, score1, player)
        g_player, g_message = g(score0, score1, player)
        if f_message and g_message:
            return g_player, f_message + "\n" + g_message
        else:
            return g_player, f_message or g_message

    return say


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """

    def strategy(score, opponent_score):
        return n

    return strategy


def make_averaged(original_function, total_samples=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TOTAL_SAMPLES times.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 1000)
    >>> averaged_dice(1, dice)
    3.0
    """
    # BEGIN PROBLEM 8
    def averaged(*args):
        total = 0
        for _ in range(total_samples):
            total += original_function(*args)
        return total / total_samples

    return averaged
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, total_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TOTAL_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    best_turn_avg_score, best_dice_n = -1, 0
    averaged_dice = make_averaged(roll_dice, total_samples)
    for num_rolls in range(1, 10 + 1):
        if (turn_avg_score := averaged_dice(num_rolls, dice)) > best_turn_avg_score:
            best_dice_n, best_turn_avg_score = num_rolls, turn_avg_score
    return best_dice_n
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print("Max scoring num rolls for six-sided dice:", six_sided_max)
    print("always_roll(6) win rate:", average_win_rate(always_roll(6)))

    print("always_roll(8) win rate:", average_win_rate(always_roll(8)))
    print("oink_points_strategy win rate:", average_win_rate(oink_points_strategy))
    print("pigs_on_prime_strategy win rate:", average_win_rate(pigs_on_prime_strategy))
    print("final_strategy win rate:", average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def oink_points_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice if that gives at least THRESHOLD points, and
    returns NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    return 0 if oink_points(score, opponent_score) >= threshold else num_rolls
    # END PROBLEM 10


def pigs_on_prime_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice when this would result in Pigs on Prime taking
    effect. It also returns 0 dice if it gives at least THRESHOLD points.
    Otherwise, it returns NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    return (
        0
        if pigs_on_prime(oink_points(score, opponent_score) + score, opponent_score)
        or oink_points_strategy(score, opponent_score, threshold, num_rolls) == 0
        else num_rolls
    )
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    This strategy slightly optimizes the default `oink_points_strategy` by
    reducing `threshold` toward endgame.
    """
    # BEGIN PROBLEM 12
    threshold = min(10, 100 - score)
    num_rolls = 5
    return oink_points_strategy(score, opponent_score, threshold, num_rolls)
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument(
        "--run_experiments", "-r", action="store_true", help="Runs strategy experiments"
    )

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
