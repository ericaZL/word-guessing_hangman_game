import random

# create_word_list(src) produces a list of all the
#    words in the file called src
# effects: reads the file src, which has the following format:
# - the first line which is a header to be ignored
# - the remaining lines each contain a single word and newline
#
# create_word_list: Str -> (listof Str)
# requires: src is a nonempty file containing common words.

def create_word_list(src):
    w_file = open(src, 'r')
    w_file.readline()
    all_words = w_file.readlines()
    w_file.close()
    w_lst = list(map(str.strip, all_words))
    return w_lst


# replace_all(secret, guess, cur) produces a string
#   like cur, except that all '-' in cur
#   corresponding to occurrences of guess in 
#   secret are replaced in cur with guess
# replace_all: Str Str Str -> Str
# requires: len(guess)=1 and guess.isalpha() is True
#           len(secret) = len(current)
#           current contains '-' or letters matching secret
# Examples:
# replace_all("secret", "e", "------") => "-e--e-"
# replace_all("secret", "s", "-e--e-") => "se--e-"
# replace_all("secret", "q", "s----t") => "s----t"

def replace_all(secret, guess, cur):
    occ = secret.count(guess)
    pos = 0
    l = len(secret)
    for i in range(l):
        if secret[i] == guess:
            cur = cur[:i] + guess + cur[i+1:]
    return cur

        
# check_guess(missed, coded) produces the string entered
#   by the user if it is not in misses or coded and is
#   an alphabetic string of length 1, otherwise continues 
#   reading input from the keyboard.
# effects: reads input from the user 
# Example:
# If the user calls check_guess("an", "a---n"), the function
#   continues until the user enters a single alphabetic character
#   other than a or n.

def check_guess(misses, coded):
    excluded = misses + coded
    acceptable = False
    while not acceptable:
        guess = input('Enter a letter: ').lower()
        if len(guess) != 1 or not (guess.isalpha()):
            print('You need to enter a single letter. Try again.')
            print('Current coded word: {0}'.format(coded))
            print('Not present: {0}'.format(misses))
        elif guess in excluded:
            print("You've already guessed {0}. Try again.".format(guess))
            print('Current coded word: {0}'.format(coded))
            print('Not present: {0}'.format(misses))
        else:
            acceptable = True
    return guess
            
        

# play_hangman() plays multiple games of hangman, reading in a list of 
#   words as a reference. The user may play multiple games of hangman
#   from this reference list, until they specify an impossible game 
#   (no suitable words in reference, or num_misses < 0). 
#   For each game, the user specifies the requirements of the game
#   (word length and maximum misses). A secret word is chosen, and the
#   player tries to guess the word before making too many mistakes. 
# Effects: reads the file "4000-most-common-english-words-csv.txt"
# play_hangman: None -> None

# Example run of play_hangman() with 3 games:
#Enter minimum word length: 5
#Enter maximum word length: 10
#Enter maximum number of misses allowed: 7
#Secret word generated ... Start guessing
#Current coded word: -----
#Enter a letter: e
#Current coded word: -----
#Not present: e
#Enter a letter: i
#Current coded word: -----
#Not present: ei
#Enter a letter: o
#Current coded word: -----
#Not present: eio
#Enter a letter: a
#Current coded word: --a--
#Not present: eio
#Enter a letter: u
#Current coded word: --a--
#Not present: eiou
#Enter a letter: t
#Current coded word: -ta--
#Not present: eiou
#Enter a letter: n
#Current coded word: -tan-
#Not present: eiou
#Enter a letter: s
#Current coded word: stan-
#Not present: eiou
#Enter a letter: d
#Congratulations! You guessed the word stand in 9 guesses
#Do you want to play again? [yn]: y
#Enter minimum word length: 10
#Enter maximum word length: 20
#Enter maximum number of misses allowed: 4
#Secret word generated ... Start guessing
#Current coded word: ----------
#Enter a letter: a
#Current coded word: a---------
#Enter a letter: e
#Current coded word: a-------e-
#Enter a letter: i
#Current coded word: a--i-i--e-
#Enter a letter: n
#Current coded word: a--ini--e-
#Enter a letter: t
#Current coded word: a--ini-te-
#Enter a letter: a
#You've already guessed a. Try again
#Current coded word: a--ini-te-
#Not present: 
#Enter a letter: huh?
#You need to enter a single letter. Try again.
#Current coded word: a--ini-te-
#Not present: 
#Enter a letter: s
#Current coded word: a--iniste-
#Enter a letter: r
#Current coded word: a--inister
#Enter a letter: p
#Current coded word: a--inister
#Not present: p
#Enter a letter: c
#Current coded word: a--inister
#Not present: pc
#Enter a letter: m
#Current coded word: a-minister
#Not present: pc
#Enter a letter: d
#Congratulations! You guessed the word administer in 11 guesses
#Do you want to play again? [yn]: y
#Enter minimum word length: 2
#Enter maximum word length: 2
#Enter maximum number of misses allowed: 1
#Secret word generated ... Start guessing
#Current coded word: --
#Enter a letter: i
#Sorry! You ran out of guesses. The word was we
#Do you want to play again? [yn]: n

def play_hangman():
    w_list = create_word_list("4000-most-common-english-words-csv.txt")

    # Continue playing until user doesn't want to play
    # anymore, or the conditions for the game make it impossible
    # to play (e.g. no misses allowed or no suitable words)
    while True:
        min_length = int(input("Enter minimum word length: "))
        max_length = int(input("Enter maximum word length: "))
        max_misses = int(input("Enter maximum number of misses allowed: "))
        
        # select possible words from w_list which are an 
        # acceptable length - the result should be called words
        words = list(filter(lambda s: min_length <= len(s) <= max_length, w_list))
        
        # terminate if game can't be played
        if words == [] or max_misses < 0:
            print("Can't play that game!")
            return
        
        # generate a secret word from the words list
        # Note the use of the randint function - cool!
        this_one = random.randint(0,len(words))
        secret = words[this_one].lower()
        
        # initialize the game variables (coded, num_guesses, misses)
        print("Secret word generated ... Start guessing")
        coded = '-' * len(secret)
        num_guesses = 0
        misses = ""
        
        # Keep playing until this match is finished 
        # successfully or unsuccessfully
        while len(misses) < max_misses and (coded != secret):
            num_guesses += 1
            print("Current coded word: {0}".format(coded))
            if misses!="":
                print("Not present: {0}".format(misses))
            your_guess = check_guess(misses,coded)
            if your_guess in secret:
                coded = replace_all(secret, your_guess, coded)
            else:
                misses += your_guess
        if coded == secret:
            print('Congratulations! You guessed the word {0} in {1} guesses'.\
                  format(secret,num_guesses))
        else:
            print('Sorry! You ran out of guesses. The word was {0}'.\
                  format(secret))
        again = input("Do you want to play again? [yn]: ")
        if again=='n':
            return
        
            
play_hangman()
