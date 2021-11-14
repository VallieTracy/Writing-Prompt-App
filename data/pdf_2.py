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

spaces = []
no_spaces = []
for word in cleaner_list:
    if word.startswith(' '):
        spaces.append(word)
    else:
        no_spaces.append(word)
 
counter = 0
for word in no_spaces:
    if len(word) == 0:
        counter += 1
print(counter)

# KEEP THIS CHUNK OF CODE BELOW THIS LINE!
new_no_spaces = []
for word in no_spaces:
    if len(word) != 0:
        new_no_spaces.append(word)
print(f'new_no_spaces length is {len(new_no_spaces)}')
# This is good what's right above this line!!!!!!!

counter = 0
for word in spaces:
    if len(word) == 0:
        counter += 1
print(counter)
 
 # VALLIE, Do any words end with a space? Something to keep in mind perhaps...

print(spaces)





ok = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz '
target = ' '

# dict_of_words = {}
# for word in cleaner_list:
#     counter = 0
#     for letter in word:
#         if letter == target:
#             counter += 1
#     dict_of_words[word] = counter

# my_keys = []
# for key, value in dict_of_words.items():
#     if value >= 2:
#         my_keys.append(key)
# print(my_keys)
# print(len(my_keys))

    
