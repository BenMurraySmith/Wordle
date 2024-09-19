import os
import pandas as pd
import random
import collections

unused_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
most_common_letters = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']

def get_data():
    duplicate_five_letter_words=[]
    individual_letter_csv_path = "C:\\Users\\bmurraysmith\\OneDrive - SharkNinja\\Documents\\side_project\\Dictionary-in-csv"
    dictionary = os.listdir(individual_letter_csv_path)
    for i in range(0,24):
        if dictionary[i]=="Dictionary in csv - raw":
            continue
        else:
            words = os.path.join(individual_letter_csv_path, dictionary[i])
            df = pd.read_csv(words, encoding="latin1", dtype=str)
            df = df.dropna(axis=0, how='all')
            values = df[df.columns[0]].tolist()
            for word in values:
                if len(word)==5 and word not in duplicate_five_letter_words and 'x96' not in word and "-" not in word and "'" not in word:
                    duplicate_five_letter_words.append(word.upper())
    five_letter_words=[]
    for word in duplicate_five_letter_words:
        if word not in five_letter_words:
            five_letter_words.append(word)
    return five_letter_words
print("Initializing...")
initialise = get_data()

# input a list of all possible letters
def first_guess(letters):
    # we want to eliminate as many letters as possible
    # first guess should be a combination of no duplicate letters and the most common letters in the english alphabet

    # returns a list of words with unique letters
    all_words = initialise
    unique_words = []
    for word in all_words:
        unique_letters = []
        for letter in word:
            if letter not in unique_letters:
                unique_letters.append(letter)
        if len(unique_letters)==5:
            unique_words.append(word)
 
    
    best_first_guesses =[]
    for word in unique_words:
        count=0
        for letter1 in word:
            for letter2 in letters:
                if letter1==letter2:
                    count+=1
        if count == 5:
            best_first_guesses.append(word)

    random_index = random.randint(0, len(best_first_guesses) - 1)
    my_first_guess = best_first_guesses[random_index]

    return my_first_guess
# print(first_guess(['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']))

# returns information on your previous guess
# import collections
def evaulate_guess(guess, correct_word, previous_dictionary):
    guess=guess.upper()
    correct_word=correct_word.upper()
    info={}
    counting_index=0
    for letter1 in guess:
        indexes = [0,1,2,3,4]
        for letter2 in correct_word:
            # if a letter from the guess exists in the correct word, is it in the correct position?
            if letter1==letter2:
                # print(f"Letter '{letter1}' found")
                guess_index = counting_index
                correct_word_index = correct_word.index(letter2)
                # if a letter in the guess is in the correct position, save this position and letter to be used in the next guess
                if guess_index==correct_word_index:
                    info[letter1]= guess_index
                else:
                    # if letter exists but is not in the right position, remove index and return a list of possible indexes.
                    indexes.remove(guess_index)
                    info[letter1]= indexes
                break
        counting_index+=1

    # clean up list indexes
    import collections
    correct_guesses=[]
    for letter in info:
        index = info[letter]
        if isinstance(index, int):
            correct_guesses.append(index)
    for correct_index in correct_guesses:
        for letter in info:
            possible_indexes = info[letter]

            if isinstance(possible_indexes, list) and correct_index in possible_indexes:
                possible_indexes.remove(correct_index)
    
    for letter in info:
        index=info[letter]
        if isinstance(index, list) and len(index)==1:
            info[letter]=index[0]
    

    # we want to keep track of all previous words and indexes, so every time we call evaluate guess, we append the output to a list where we can filter the most recent dictionary using previous ones
    
    #------------------------------------------------------------------------------------
    # improvements on extra filter steps:

    prev_info=previous_dictionary
    curr_info = info
    for letter1 in prev_info:
        for letter2 in curr_info:
            if letter1==letter2 and isinstance(prev_info[letter1], list) and isinstance(curr_info[letter2], list):
                list1 = prev_info[letter1]
                list2 = curr_info[letter2]
                updated_info = list1+list2
                count_nums = collections.Counter(updated_info).items()
                for x in count_nums:
                    num, count = x
                    if count < 2 and num in list2:
                        list2.remove(num)
                unique_list=[]
                for y in list2:
                    if y not in unique_list:
                        unique_list.append(y)

                curr_info[letter2] = unique_list



    # improvements end here
    #--------------------------------------------------------------------------------
        
    return curr_info
# guess, correct_word, previous dictionary
# print(evaulate_guess("ALOFT", "BOAST", {'O': [0, 1, 2], 'T': 4}))



# next guess assumes the evaluation is non-empty
def next_guess(previous_guess, evaluation):
    previous_guess=previous_guess.upper()
    # if zero letters are present in guess:
    if not evaluation: 
        for letter in previous_guess:
            unused_letters.remove(letter)
            most_common_letters.remove(letter)
        return first_guess(unused_letters)
    else:
        # remove unwanted letters from unused_letters list
        correct_letters = []
        for letter_found in evaluation:
            correct_letters.append(letter_found)
        previous_guess_composition = [letter for letter in previous_guess]
        for letter in previous_guess_composition:
            if letter not in correct_letters:
                try:
                    unused_letters.remove(letter)
                    most_common_letters.remove(letter)
                except ValueError:
                    continue
                    # print("letter already removed.")
            
        unsure_indexes = {}
        definite_indexes = {}
        # pull apart the evaluation:
        for letter_found in evaluation:
            index = evaluation[letter_found]
            
            # if the index of the letter is an integer, then its position is correct - lock in the letter and index.
            if isinstance(index, int):
                definite_indexes[letter_found]=index
            else:
                unsure_indexes[letter_found]= index
        

        
        # put evaulation into a dictionary:
        evaluation_dict = evaluation

        # now we have sorted through the information, how can we use it to make the next guess?

        # FILTERING PROCESS


        # using the dictionary and previous guess, narrow down the list of all available words 
        all_words = initialise

        # step 1: filter list by what letters are found in evaluation

        # filter by getting rid of all words that dont have any of the letters found in the evalation function
        filter1_list = []
        for word in all_words:
            letter_count=0
            for letter in evaluation_dict:
                if letter in word:
                    letter_count+=1
            if letter_count==len(evaluation_dict) and word not in filter1_list:
                filter1_list.append(word)


        # step 2: eliminate words based on indexes

        # how do we choose which word to play based on the possible words in our most up-to-date list? - use the indexes!!
        # go through each letter, if the index is a list, then make sure to eliminate words with letters that don't match the index list
        # filter2_list=[]
        possible_indexes = [0,1,2,3,4]
        no_possible_letters = {}
        for letter in evaluation_dict:
            if isinstance(evaluation_dict[letter], list):
                for index in possible_indexes:
                    if index not in evaluation_dict[letter]:
                        no_possible_letters[letter] = index
        
        
        filter2_list=[]
        for word in filter1_list:
            outer_check=True
            counting_letters=0
            for index, letter in enumerate(word):
                letter_index=index
                if outer_check==False:
                        break
                else:
                    if letter in no_possible_letters:
                        # letter_index=word.index(letter)
                        for imp_letter in no_possible_letters:
                            if letter==imp_letter:
                                if letter_index==no_possible_letters[imp_letter]:
                                    outer_check=False
                                    break
                counting_letters+=1
                    
            if outer_check:
                filter2_list.append(word)

        




                    
        

        # step 3: remove words from list that contain letters not found in unused letters

        # remove all words in the filtered list with letters that are not in unused letters 
        # - these are dud letters and can be thrown away because we know they aren't in the correct word
        filter3_list=[]
        for word in filter2_list:
            count=0
            for letter in word:
                if letter in unused_letters:
                    count+=1
            if count==5:
                filter3_list.append(word)


        if not filter3_list:
            filter3_list=filter2_list



        # step 4: filter by definite letters ( letters where we know the location ) IF THERE ARE ANY
        
        # count how many definite letters we have


        # filter by known letters
        filter4_list=[]
        for word in filter3_list:
            count=0
            for letter in evaluation_dict:
                if isinstance(evaluation_dict[letter], int):
                    if word[evaluation_dict[letter]]==letter:
                        count+=1
            
            if count==len(definite_indexes):
                filter4_list.append(word)

        # if filter4_list is empty, that means there are no found letters in the evaluation with known locations, so just take filter 3 list as the final list
        if not filter4_list:
            filter4_list = filter3_list

        

        # step 5: if the lenght of the evaluation dict is less than 3, then we shouldn't play words with multiple letters.

        filter5_list=[]
        for word in filter4_list:
            unique_letters=[]
            if len(evaluation_dict) < 3:
                for letter in word:
                    if letter not in unique_letters:
                        unique_letters.append(letter)
            if len(unique_letters)==5:
                filter5_list.append(word)
        
        if not filter5_list:
            filter5_list=filter4_list
                
        


        random_index = random.randint(0, len(filter5_list) - 1)
        next_guess = filter5_list[random_index]



    return next_guess

# print(next_guess("swipe", {'P': [0, 1, 2, 4]}))
