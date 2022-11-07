import numpy as np
from typing import List, Tuple


def pref_list(gender_preference):
    if gender_preference == "Men":
        pref_genders = ["Male", "Nonbinary"]
    elif gender_preference == "Women":
        pref_genders = ["Female", "Nonbinary"]
    else:
        pref_genders = ["Male", "Female", "Nonbinary"]

    return pref_genders


def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    # pseudocode: https://drive.google.com/file/d/1ejGCXLGijnqLcUy2Cx8VuZWQmcaThisi/view

    # initialize list of unmatched people
    N = len(gender_id)
    unmatched = list(range(N))

    # matrix for whether proposer has considered match with acceptor
    proposed = [([0] * N) for x in range(N)]

    # initialize matches tuple list
    matches = []

    # while unmatched != []:
    for person1 in range(N):
        if unmatched == []:
            break
        for person in range(N):
            person1 = unmatched[0]

            # or person1 not in unmatched
            if person1 == person or proposed[person1][person] == 1: 
                continue               

            # update scores in matrix to be 0 if genders incompatible
            if gender_id[person1] not in pref_list(gender_pref[person]):
                scores[person1][person] = 0
                # has tried proposing
                proposed[person1][person] = 1
                continue

            # if person is free
            if scores[person1][person] != 0 and person in unmatched:
                matches.append((person1, person))
                unmatched.remove(person1)
                unmatched.remove(person)
                # has tried proposing
                proposed[person1][person] = 1
                break

            # else if person prefers m to current match m2
            if person not in unmatched:
                item = [a for a in matches if a[0] == person]
                if item != []:
                    m2 = item[0][1]
                    if scores[person][person1] > scores[person][m2]:
                        matches.remove(item[0])
                        matches.append((person1, person))
                        unmatched.append(m2)
                        unmatched.remove(person1)
                        # has tried proposing
                        proposed[person1][person] = 1
                continue

            else:
                # has tried proposing
                proposed[person1][person] = 1
                break


        # if successful, remove m from unmatched list, add match to matches
    print(matches)
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
