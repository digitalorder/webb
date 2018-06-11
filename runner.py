import random
from user_input import MockUserInput, ConsoleOneCharInput
from playwords_set import PlaywordsSet
import sys


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


def play_round(playwords, user_input_generator):
    words = playwords.select_for_next_round()
    # print("filtered for this round: {}".format(filtered_playwords))
    if len(words) == 0:
        print("Good job, you've already remembered all the words for this session!")
        return True

    picked_number = random.randint(0, len(words) - 1)
    word = words[picked_number]
    print("{} / {}? ".format(word.german, word.native), end='')
    sys.stdout.flush()
    guessed = False
    failed_to_guess = False
    while not guessed:
        guess = get_guess(user_input_generator)

        if guess == "EOF":
            print(bcolors.FUCHSIA + "Quit. " + bcolors.ENDC)
            return True

        guess_result = playwords.check_guess(word, guess, failed_to_guess)
        if guess_result:
            print(bcolors.GREEN + "Correct. " + bcolors.ENDC, end='')
            sys.stdout.flush()
            guessed = True
        else:
            print(bcolors.RED + "{} is incorrect. ".format(guess) + bcolors.ENDC, end='')
            sys.stdout.flush()
            if not failed_to_guess:
                failed_to_guess = True

    if word.learned_in_session:
        print(bcolors.BOLD + "Now you remembered it!" + bcolors.ENDC)
    else:
        print("")

    return False


if __name__ == '__main__':
    print("Welcome to Words by Ebbinghaus!\nControls: 1 - der | 2 - die | 3 - das | q - exit\n")

    print("Loading game data...")
    playwords = PlaywordsSet("words.json", "player_data.json")
    # print("All words: {}".format(playwords))

    print("Configuring...")
    random.seed(0)

    print("Let's go!")
    user_input = MockUserInput('mock_commands.txt')  # ConsoleOneCharInput()
    user_abort = False
    while not user_abort:
        user_abort = play_round(playwords, user_input)

    print("Saving your progress...")
    playwords.save_progress()

    print("Bye!")
