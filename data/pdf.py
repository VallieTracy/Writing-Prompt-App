import PyPDF2
# pdf file object
# you can find find the pdf file with complete code in below

pdf_file = open('2500_writing_prompts.pdf', 'rb')

# pdf reader object
#pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# number of pages in pdf
#print(pdfReader.numPages)
print(f'Number of pages: {pdf_reader.numPages}')

# a page object
#pageObj = pdfReader.getPage(0)
# pageObj = pdf_reader.getPage(6)

# extracting text from page
# this will print the text you can also save that into String

# page_string = pageObj.extractText()
# parsed = page_string.split('    ')
# print(parsed)
# print(len(parsed))
# print(parsed[-2])

def parse_pdf():
    all_pages = []
    for i in range(0, 8):
        pageObj = pdf_reader.getPage(i)
        page_string = pageObj.extractText()
        parsed_page = page_string.split('    ')
        for parsed in parsed_page:
            all_pages.append(parsed)
        print(f'{i}, length is {len(all_pages)}')
    return all_pages

all_pages_list = parse_pdf()
print(len(all_pages_list))

def remove_n(a_list):
    target = '\n'
    cleaner_list = []
    for word in a_list:
        if target in word:
            word = word.replace(target, '')
            cleaner_list.append(word)
        else:
            cleaner_list.append(word)
    return cleaner_list

clean_list = remove_n(all_pages_list)
print(len(clean_list))

def foreign(a_list):
    ok = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz -/'

    funky_words = []
    for word in a_list:
        for letter in word:
            if letter not in ok:
                funky_words.append(word)
    return funky_words

funky_words = foreign(clean_list)
print(funky_words)
print(len(funky_words))

def remove_funky(arr):
    new_list = []
    for word in clean_list:
        if word not in arr:
            new_list.append(word)
    return new_list

cleaned_list = remove_funky(funky_words)
print(len(cleaned_list))
print(cleaned_list)

for item in cleaned_list:
    if item == '':
        print('found empty item')








