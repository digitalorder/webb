import json
import random
from word import Word
from longterm_data import LongtermData
from datetime import datetime
from playword import PlayWord
from user_input import MockUserInput, ConsoleOneCharInput
import sys


def load_words(f):
    plain_data = json.load(f)
    result = []
    for w in plain_data['words']:
        result.append(Word(w['german'], w['german_gender'], w['native'], w['id_num']))
    return result


def load_longterm_data(f):
    plain_data = json.load(f)
    result = list()
    for d in plain_data:
        try:
            result.append(LongtermData.from_json(d))
        except KeyError:
            continue
    return result


def save_longterm_data(f, words):
    json_repr = []
    for w in words:
        json_repr.append(w.json_repr())
    json_words = json.dumps(json_repr, indent=4, sort_keys=True)
    f.write(json_words)


def get_guess(user_input):
    guess = ""
    while guess == "":
        char = user_input.next_command()
        # print("got {}".format(char))
        if char == "1":
            return "masculine"
        elif char == "2":
            return "feminine"
        elif char == "3":
            return "neuter"
        elif char == "EOF":
            return "EOF"


class bcolors:
    FUCHSIA = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def play_round(words, user_input):
    picked_number = random.randint(0, len(words) - 1)
    word = words[picked_number]
    word.attempts += 1
    print("{} / {}? ".format(word.german, word.native), end='')
    sys.stdout.flush()
    guessed = False
    failed_to_guess = False
    while not guessed:
        guess = get_guess(user_input)
        if word.german_gender == guess:
            print(bcolors.GREEN + "Correct. " + bcolors.ENDC, end='')
            sys.stdout.flush()
            word.success_in_row += 1
            guessed = True
        elif guess == "EOF":
            print(bcolors.FUCHSIA + "Quit. " + bcolors.ENDC)
            return True
        else:
            print(bcolors.RED + "{} is incorrect. ".format(guess) + bcolors.ENDC, end='')
            sys.stdout.flush()
            word.success_in_row = 0
            if not failed_to_guess:
                word.failures_timestamps.append(datetime.now())
                failed_to_guess = True

    if word.success_in_row == 3:
        word.learned_in_session = True
        word.success_timestamps.append(datetime.now())
        print(bcolors.BOLD + "Now you remembered it!" + bcolors.ENDC)
    else:
        print("")

    return False

if __name__ == '__main__':
    print("Welcome to Words by Ebbinghaus!\nControls: 1 - der | 2 - die | 3 - das | q - exit\n")

    print("Loading game data...")
    with open("words.json", 'r') as f:
        words = load_words(f)

    try:
        with open("player_data.json", 'r') as f:
            longterm_data = load_longterm_data(f)
    except FileNotFoundError:
        longterm_data = []

    playwords = list()
    for w in words:
        word_longterm_data = [d for d in longterm_data if d.id_num == w.id_num]
        if len(word_longterm_data) == 0:
            word_longterm_data = [LongtermData(w.id_num)]
        playwords.append(PlayWord(w, word_longterm_data[0]))

    # print("All words: {}".format(playwords))

    print("Configuring...")
    random.seed(0)

    print("Let's go!")
    user_input = ConsoleOneCharInput()  # MockUserInput('mock_commands.txt')
    user_abort = False
    while not user_abort:
        # 1. word wasn't remembered in this session
        filtered_playwords = [w for w in playwords if not w.learned_in_session]
        # 2. learned less then an minute ago
        filtered_playwords = [w for w in filtered_playwords if w.last_learned() > 600]
        # print("filtered for this round: {}".format(filtered_playwords))

        if len(filtered_playwords) == 0:
            print("Good job, you've already remembered all the words for this session!")
            break

        user_abort = play_round(filtered_playwords, user_input)

    print("Saving your progress...")
    with open("player_data.json", 'w') as f:
        save_longterm_data(f, playwords)

    print("Bye!")
