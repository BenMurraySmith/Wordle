import wordle_functions

#user input
my_word = input("enter a 5 letter word: ")

#initialise letters
used_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
most_common_letters = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U']
top_13_letters = most_common_letters[:13]

#initialise evaluation dictionary
previous_dictionary={}
solved=False

#standardise user's word
correct_word=my_word.upper()
# grab list of words from external data files
list_of_words = wordle_functions.initialise

#user's word might not be in my collection - if so, choose different word
if correct_word in list_of_words:
    #make the first guess
    my_first_guess = wordle_functions.first_guess(most_common_letters)
    no_of_guesses=1
    
    print(my_first_guess)
    # if first guess is correct, my program is a genius
    if correct_word==my_first_guess:
        solved=True
    else:
        previous_guess = my_first_guess
        while previous_guess!=correct_word:
            #evaluate the guess. the evaluation dictionary will be empty for the first iteration
            previous_dictionary = wordle_functions.evaulate_guess(previous_guess, correct_word, previous_dictionary)
            #the previous guess along with the findings are used to make the next guess. 
            next_guess = wordle_functions.next_guess(previous_guess, previous_dictionary)
            no_of_guesses+=1

            #repeat logic for the next guess
            print(next_guess)
            if next_guess==correct_word:
                solved=True
            else:
                previous_dictionary = wordle_functions.evaulate_guess(next_guess, correct_word, previous_dictionary)
                
                next_guess = wordle_functions.next_guess(next_guess, previous_dictionary)
                no_of_guesses+=1
                
                print(next_guess)
            # close loop here
            previous_guess=next_guess

            if solved:
                break
    # Wordle gives you a maximum of 6 guesses. The program will continue past this point anyway
    if no_of_guesses > 6:
        print(f"Failed to solve puzzle :( ({no_of_guesses} guesses)")
    else:
        print(f"Puzzle solved in {no_of_guesses} guesses :)")
else:
    print("please choose a different word.")
