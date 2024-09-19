import wordle_functions

my_word = input("enter a 5 letter word: ")

used_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
most_common_letters = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U']
top_12_letters = most_common_letters[:13]
previous_dictionary={}
solved=False

correct_word=my_word.upper()
list_of_words = wordle_functions.initialise

if correct_word in list_of_words:
    my_first_guess = wordle_functions.first_guess(most_common_letters)
    no_of_guesses=1
    
    print(my_first_guess)
    if correct_word==my_first_guess:
        solved=True
    else:
        previous_guess = my_first_guess
        while previous_guess!=correct_word:
            previous_dictionary = wordle_functions.evaulate_guess(previous_guess, correct_word, previous_dictionary)
            
            next_guess = wordle_functions.next_guess(previous_guess, previous_dictionary)
            no_of_guesses+=1
            
            print(next_guess)
            if next_guess==correct_word:
                solved=True
            else:
                previous_dictionary = wordle_functions.evaulate_guess(next_guess, correct_word, previous_dictionary)
                
                next_guess = wordle_functions.next_guess(next_guess, previous_dictionary)
                no_of_guesses+=1
                
                print(next_guess)
            
            previous_guess=next_guess

            if solved:
                break

    if no_of_guesses > 6:
        print(f"Failed to solve puzzle :( ({no_of_guesses} guesses)")
    else:
        print(f"Puzzle solved in {no_of_guesses} guesses :)")
else:
    print("please choose a different word.")
