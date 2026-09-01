import random
from itertools import combinations
import os

def __all_team_in_selection(selections, team):
    """
    Ensure that the entire team is a part of any selection of pairings.

    :param selections: list of pairs
        - list of pairings (number of len(team)/2, rounded) to test for inclusion of all participants
    :param team: list
        - list of participants to take part in the random coffees
    :return: boolean
        - True if all participants are included in the selection; False otherwise
    """
    personnel = []
    for s in selections:
        personnel.append(s[0])
        personnel.append(s[1])

    for person in team:
        if person not in personnel:
            return False

    return True

def __selection_in_previous(selections, pairs_dict, prev_week):
    """
    Compares the current pairing selection against:
        - all previous weeks (pairs_dict)
        - the most previous week, as all possible combinations are reset (prev_week)

    :param selections: list of pairs
        - list of pairings (number of len(team)/2, rounded) to test for inclusion of all participants
    :param pairs_dict: dictionary
        - keys are dates for weeks with coffees, values are the pairings for that week
    :param prev_week: list of pairings
        - list of pairings from the previous week to ensure that no duplicates happen between weeks
    :return: boolean
        - check if pairing is present in one of the previous weeks (pairs_dict), or in the most previous week after all
        possible combinations have been used up (prev_week)
    """
    if len(prev_week) != 0:
        for pair in selections:
            if pair in prev_week:
                return True
    else:
        combined = [item for vals in pairs_dict.values() for item in vals]
        for pair in selections:
            if pair in combined:
                return True

    return False


def check_selection_valid(selections, team, pairs_dict, prev_week):
    """
    Check the presently selected pairs to ensure that:
        1. all members of the participants are listed in each selection
        2. the selections have not been used previously in preceding weeks

    :param selections: list of pairs
        - list of pairings (number of len(team)/2, rounded) to test for inclusion of all participants
    :param team: list
        - list of participants to take part in the random coffees
    :param pairs_dict: dictionary
        - keys are dates for weeks with coffees, values are the pairings for that week
    :param prev_week: list of pairings
        - list of pairings from the previous week to ensure that no duplicates happen between weeks
    :return: boolean
        - True if the selection of pairs is valid/approved; False otherwise
    """

    if __all_team_in_selection(selections, team) and \
        not __selection_in_previous(selections, pairs_dict, prev_week):
            return True

    return False



if __name__ == "__main__":
    from itertools import combinations as combs
    import datetime

    fn = './inputs/coffee participants.txt'
    part = {}
    with open(fn, 'r') as fid:
        ch4ds = [line for nnn, line in enumerate(fid.read().split('\n'))]

    if len(ch4ds) % 2 != 0:  # odd length
        ch4ds.append('Your choice! Contact whomever you want :D!')

    # determine start and end date
    start = input('What is the start date for the random coffees? (MM/DD/YYYY)\n')
    if start == '':
        start = '09/07/2026'

    start = datetime.datetime.strptime(start, '%m/%d/%Y')
    end_date = input('What is the end date for the random coffees? (MM/DD/YYYY)\n')
    if end_date == '':
        end_date = '01/01/2027'
    end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y')

    # create all possible pairs
    all_possible_pairs = [sorted(pair) for pair in combinations(ch4ds, 2)]

    # calculate number of pairings
    pairings_per_week = int(len(ch4ds) / 2)

    longterm_pairs = {}
    shortterm_pairs = {}
    previous_week = []
    current = start

    while current < end_date:
        a = 0
        # create selection
        found_selection = False
        while not found_selection:
            selection_idx = random.sample(range(len(all_possible_pairs)), pairings_per_week)
            valid_selection = []
            for idx in selection_idx:
                valid_selection.append(all_possible_pairs[idx])
            found_selection = check_selection_valid(valid_selection, ch4ds,
                                                    shortterm_pairs, previous_week)
            # loop is stuck! Restart!!
            if a > 0 and a % 1e5 == 0:
                print('** loop stuck: restarting... **')
                current = min(shortterm_pairs.keys())
                all_possible_pairs = [sorted(pair) for pair in combinations(ch4ds, 2)]
                shortterm_pairs = {}
                break
            a+=1

        if found_selection:
            shortterm_pairs[current] = valid_selection
            # update user
            print(f'Completed Week: {current}')
            # update time
            current += datetime.timedelta(days=7)

            for selection in valid_selection:
                all_possible_pairs.remove(selection)

            if len(all_possible_pairs) == 0:
                print('\n*** ALL POSSIBLE PAIRS COMPLETE: RESTARTING MATCHUPS ***\n')
                all_possible_pairs = [sorted(pair) for pair in combinations(ch4ds, 2)]
                previous_week = valid_selection
                longterm_pairs.update(shortterm_pairs)
                shortterm_pairs = {}
            elif len(shortterm_pairs.keys()) > 0:
                previous_week = []

            if len(shortterm_pairs.keys()) > 0:
                longterm_pairs.update(shortterm_pairs)

    # write the file output
    if not os.path.exists('./outputs/'):
        os.makedirs('./outputs/')

    fileout = f'./outputs/{start.strftime("%Y%m%d")}-{end_date.strftime("%Y%m%d")}-random-coffee-schedule.txt'
    with open(fileout, 'w') as fout:
        for date in longterm_pairs.keys():
            fout.write(f"Coffee dates for week of {date.strftime('%m/%d/%Y')}:\n")
            for pair in longterm_pairs[date]:
                fout.write(f"{pair[0]} <---> {pair[1]}\n")
            fout.write('\n\n')

    print(f'\nSchedule txt file created: \n\t- {fileout}')