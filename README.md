# Wordle Solver

This program solves a Wordle styled puzzle! Given a 5 letter word from the user and a (somewhat) complete list of words from the English dictionary, my searching algorithm plays words based on the following logic:
1. The first guess takes 5 unique letters from the 13 most common letters in the English alphabet.
2. Once the word is played, it's passed through several checks:
     a) Have any letters been found (orange)?
     b) Are there any letters in the correct position (green)?
3. If any there are any orange/green letters, we condense an instance of our list to contain only the words that align with the previous findings, which becomes the new list in the next iteration
4. We keep track of findings by storing letters and their indexes in a dictionary as key-value pairs. For example, if the correct word is "BREAD" and the program plays "BLACK", the evaluation ouputs {'B': 0, 'A': [1,3,4]}. The value of 'B' is an integer (green) so we have found the first letter. 'A''s value is a list of integers (orange) - it cannot be in position 0 because that has already been found. It was played at position 2 in "BLACK", so the only remaining possibilities are at position 1, 3 or 4.
5. Once the guess has been evaluated and our list of words has condensed, the program makes the next guess. This repeats until the word has been found.

DISCLAIMER: I wrote this while I was still learning how to code, have mercy...
