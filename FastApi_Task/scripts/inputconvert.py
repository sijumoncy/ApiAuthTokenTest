import re
import os

def texttojson(file_name):
    num = 1
    file_name = file_name
    

    basepath = os.path.dirname(__file__) + '/../files/'
    file_path = basepath + file_name

    with open(file_path, 'r', encoding="UTF-8") as file:
        lines = file.read()
        verse_list = re.split('\d', lines)
        #print(verse_list)

    book = file_name
    book = re.sub(r'\.\w+', '', book)
    book = re.split(r'\_', book)
    #print(book)
    book_lang = book[0]
    book_name = book[1]
    chapter_num = book[2]
    verse_data=[]

    #remove head
    verse_list.pop(0)

    #creating chapter dict
    for line in verse_list:
            if line != '':
                verse_dict = {
                    "verseNumber": num,
                    "verseText": line
                }
                num+=1
                verse_data.append(verse_dict)

    #print(data)    

    book_json = {
        "book":{
            "bookCode": book_name,
            "description":""
        },
        "chapters":[
            {
                "chapterNumber":chapter_num,
                "contents":verse_data

            }
        ]   
    }        



    #print(book_json)

    return book_json    


'''
with open('outputtest.txt', 'a', encoding="UTF-8") as f:
    for line in verse_list:
        if line != '':
            #f.write(str(num)+" "+line+"\n")
            num+=1
'''

            