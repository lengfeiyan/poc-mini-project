"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) == 0:
        return []
    result_list = [list1[0]]
    last_index = 0
    for dummy_index in range(1,len(list1)):
        if list1[dummy_index] != list1[last_index]:
            result_list.append(list1[dummy_index])
            last_index = dummy_index
    return result_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result_list = []
    #list3 = remove_duplicates(list1)
    for dummy_element in list1:
        if list2.count(dummy_element) > 0 and result_list.count(dummy_element) == 0:
            result_list.append(dummy_element)
    return result_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """
    result_list = []
    list1_length = len(list1)
    list2_length = len(list2)
    list1_index = 0
    list2_index = 0
    while list1_index < list1_length and list2_index < list2_length:
        if list1[list1_index] <= list2[list2_index]:
            result_list.append(list1[list1_index])
            list1_index = list1_index + 1
        else:
            result_list.append(list2[list2_index])
            list2_index = list2_index + 1
    
    if list1_index < list1_length:
        result_list.extend(list1[list1_index:])
    if list2_index < list2_length:
        result_list.extend(list2[list2_index:])
        
    return result_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
       mid = len(list1) / 2
       return merge(merge_sort(list1[0:mid]),merge_sort(list1[mid:]))

# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    elif len(word) == 1:
        return ["",word]
    else:
        result_strings = []
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        new_strings = []
        for rest_string in rest_strings:
            for dummy_index in range(len(rest_string)):
                #在首位插入
                if dummy_index == 0:
                    new_string = first + rest_string
                    new_strings.append(new_string)
                #在中间插入                
                else:
                    new_string = rest_string[0:dummy_index] + first + rest_string[dummy_index:]
                    new_strings.append(new_string)
            #在末尾插入
            new_strings.append(rest_string + first)
            
        result_strings.extend(rest_strings)
        result_strings.extend(new_strings)
        
        return result_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    
    words = []
    for line in netfile.readlines():
        words.append(line.replace('\n',''))
    
    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    