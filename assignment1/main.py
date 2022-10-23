#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # initialize score
    score = 0

    # gender preferences - will return 0 if not in either preference
    if user2.gender in user1.preferences:
        score += 0.1
    if user1.gender in user2.preferences:
        score += 0.1

    # check corresponding responses
    q_total_num = len(user1.responses)
    q_index = 0
    answer_match = 0
    for answer in user2.responses:
        if answer == user1.responses[q_index]:
            answer_match += 1
    
    # add percentage of matching question answers - will be 1 if all match
    question_weight = answer_match / q_total_num
    score += question_weight

    # extra weight if more than half of question answers match
    # none of test data had more than 10 questions match rip
    if answer_match > q_total_num * 0.5:
        score = score * (1 + question_weight)

    # scuffed normalizing - cap scores at 1
    if score > 1:
        score = 1

    return score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
