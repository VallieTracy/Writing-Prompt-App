import PyPDF2

pdf_file = open('2500_writing_prompts.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# print(f'Number of pages: {pdf_reader.numPages}')

def parse_pdf():
    """Go thru each page of pdf and add to a list.
    Will return all pages in one list"""
    
    all_pages = []
    
    for i in range(0, 8):
        pageObj = pdf_reader.getPage(i)
        page_string = pageObj.extractText()
        """Words/phrases in pdf split by 4 spaces"""
        parsed_page = page_string.split('    ')
        for parsed in parsed_page:
            all_pages.append(parsed)
        
    return all_pages

all_pages_list = parse_pdf()

def remove_n(arr):
    """Remove '\n from a list'"""
    
    target = '\n'
    cleaned_list = []
    
    for word in arr:
        if target in word:
            word = word.replace(target, '')
            cleaned_list.append(word)
        else:
            cleaned_list.append(word)
    
    return cleaned_list

no_n_list = remove_n(all_pages_list)

def foreign_chars(arr):
    """Find characters not in American alphabet
    Returns a list"""

    ok = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz -/'
    funky_words = []
    
    for word in arr:
        for letter in word:
            if letter not in ok:
                funky_words.append(word)
    return funky_words

funky_words = foreign_chars(no_n_list)

def remove_funky(arr):
    """Remove words that contain foreign characters
    Returns a list"""
    
    funks_removed = []
    
    for word in no_n_list:
        if word not in arr:
            funks_removed.append(word)

    return funks_removed

cleaner_list = remove_funky(funky_words)
print(len(cleaner_list))

def edge_case_empty(arr):
    """I discovered that there are five cases of elements that are empty but not picked up
    in other functions, so I'm removing them in this function quick.  5 elements total."""
    
    cleaner_list = []
    for word in arr:
        if word != '':
            cleaner_list.append(word)
    return cleaner_list

cleaner_list = edge_case_empty(cleaner_list)
print(len(cleaner_list))

def create_space_lists(arr):
    """Loop thru a list and determine if an element starts with a space.
    Depending on that, it will then add it to one of two newly created lists.
    Will return a set of two lists."""

    spaces = []
    no_spaces = []

    for word in arr:
        if word.startswith(' '):
            spaces.append(word)
        else:
            no_spaces.append(word)

    return (spaces, no_spaces)

both_lists = create_space_lists(cleaner_list)
spaces_list = both_lists[0]
no_spaces_list = both_lists[1]

# Do I need this function? Not quite sure, but it does create some useful data
def find_spaces(arr, space_count):
    """Loop thru a list, count number of spaces in each item and return a dictionary
    with element as key and count as value.
    Based on number of spaces specified (parameter space_count), will also return keys + number of keys.
    Space_count is an integer. Returns those three items as a set"""
    
    target = ' '
    dict_of_words = {}
    
    for word in arr:
        counter = 0
        for letter in word:
            if letter == target:
                counter += 1
        dict_of_words[word] = counter

    my_keys = []
    for key, value in dict_of_words.items():
        if value >= space_count:
            my_keys.append(key)
    return (my_keys, len(my_keys), dict_of_words)

# ************************************************
# no_spaces_list is good, no spaces at front, no multiple spaces between, have not checked end yet
# check for spaces at end once I have all words into one list again
# for i in range(len(no_spaces_list)):
#     print(f'{i}.{no_spaces_list[i]}')
# ************************************************

# Broken up spaces_list into two lists to make it easier to see in terminal
spaces_list_1 = []
for i in range(0, 1000):
    spaces_list_1.append(spaces_list[i])
spaces_list_2 = []
for i in range(1000, len(spaces_list)):
    spaces_list_2.append(spaces_list[i])

new_spaces_1 = []
for word in spaces_list_1:
    word = word[1:]
    new_spaces_1.append(word)
bad_words_1 = []
for word in new_spaces_1:
    if word.startswith(' '):
        bad_words_1.append(word)
#print(bad_words_1)
good_bad_words_1 = []
for word in bad_words_1:
    word = word[1:]
    good_bad_words_1.append(word)
#print(good_bad_words_1)
# good_bad_words_1 is good list from spaces_list_1
spaces_1_minus_bad = []
for word in new_spaces_1:
    if word not in bad_words_1:
        spaces_1_minus_bad.append(word)

#print(len(spaces_1_minus_bad))
largest_1 = []
for word in spaces_1_minus_bad:
    if word != '':
        largest_1.append(word)
#print(len(largest_1))

new_spaces_2 = []
for word in spaces_list_2:
    word = word[1:]
    new_spaces_2.append(word)
bad_words_2 = []
for word in new_spaces_2:
    if word.startswith(' '):
        bad_words_2.append(word)
print(bad_words_2)
good_bad_words_2 = []
for word in bad_words_2:
    word = word[1:]
    good_bad_words_2.append(word)
print(good_bad_words_2)
# good_bad_words_2 is good list from spaces_list_2
spaces_2_minus_bad = []
for word in new_spaces_2:
    if word not in bad_words_2:
        spaces_2_minus_bad.append(word)

print(len(spaces_2_minus_bad))
largest_2 = []
for word in spaces_2_minus_bad:
    if word != '':
        largest_2.append(word)

# largest_2 has two instances where there are two items separated by two spaces
print(f'length of largest_2: {len(largest_2)}')
new_words = []
for item in largest_2:
    if '  ' in item:
        words = item.split('  ')
        for word in words:
            new_words.append(word)
print(new_words)
next_new_words = []
for word in new_words:
    if word.startswith(' '):
        word = word[1:]
        next_new_words.append(word)
    else:
        next_new_words.append(word)
print(next_new_words)
for item in largest_2:
    if '  ' in item:
        largest_2.remove(item)
print(f'length of largest_2: {len(largest_2)}')
print(len(next_new_words))
print(len(largest_2))



        


# spaces_list_1 and spaces_list_2 were created from spaces_list
# spaces_list has a length of around 1982 I believe
# I brought it into two parts
# spaces_list_1 was broken down further, and those parts are done
# those two parts that are done are called largest_1 and good_bad_words_1
# to keep all lists together, no_spaces_list is also good
# PUT LISTS in BELOW TO CHECK THEM LINE BY LINE IN TERMINAL:
# for i in range(len(largest_2)):
#     print(f'{i}.{largest_2[i]}')


# no_spaces_list is good
# largest_1 is good
# good_bad_words_1 is good
# good_bad_words_2 is good
# largest_2 is good
# next_new_words is good

# NEED TO JOIN THE ABOVE 6 LISTS!

lists = (no_spaces_list, largest_1, largest_2, good_bad_words_1, good_bad_words_2, next_new_words)
final_list = no_spaces_list+largest_1+largest_2+good_bad_words_1+good_bad_words_2+next_new_words
print(f'the length of final list is {len(final_list)}')
endings = []
for word in final_list:
    if word[-1] == ' ':
        final_list.remove(word)
        word = word[:-1]
        endings.append(word)
        


result = final_list + endings
# DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!








 







# print(len(new_spaces))

# still_spaces = []
# for word in new_spaces:
#     counter = 0
#     if word.startswith(' '):
#         still_spaces.append(word)

# new_still_spaces = []
# for word in new_still_spaces:
#     word = word[1:]
#     new_still_spaces.append(word)









    
