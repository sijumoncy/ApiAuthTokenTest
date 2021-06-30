import sqlalchemy
from sqlalchemy.sql.functions import count
from main import engine
from sqlalchemy.sql.elements import Null
from scripts.adddbdata import keywordadd
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import null
from sqlalchemy.sql import text
from models import MlBook,EnBook,KeyWord,keytoverse

#FUNCTION FOR FETCH BOOK
def fetchbook(bookcode,chapter,lang,session):
    book_code = bookcode.upper()
    chapter = chapter
    lang_code = lang.capitalize()

    #checking which language request
    session = session
    if (lang_code == "Ml"):
        db_model = MlBook
    elif (lang_code == "En"):
        db_model = EnBook
    else:
        return {"msg":"Provide a valid language code 'Ml - En'"}    

    books = session.query(db_model).filter(db_model.book == book_code).filter(db_model.chapter == chapter)
    if books.count():
        verse_list = {
        "book":book_code,
        "chapter":chapter,
        "contents":[]
        }
        for b in books:
            dict =  {
                "verseNumber": b.versenum,
                "verseText": b.verse
            }
            verse_list["contents"].append(dict)
        #print(verse_list)
        return verse_list    
    else:
        return {"msg":"sorry such data not exist, check the data provided"}    


            
#FUNCTION FOR FETCH VERSE
def fetchverse(bookcode,chapter,language_code,verse_number,session):
    book_code = bookcode.upper()
    chapter = chapter
    lang_code = language_code.capitalize()
    verse_number = verse_number

    #checking which language request
    session = session
    if (lang_code == "Ml"):
        db_model = MlBook
    elif (lang_code == "En"):
        db_model = EnBook
    else:
        return {"msg":"Provide a valid language code 'Ml - En'"}

    verses = session.query(db_model.verse).filter(db_model.book == book_code).filter(db_model.chapter == chapter).filter(db_model.versenum == verse_number)
    if verses.count():
        data = {
            "book":bookcode,
            "chapter":chapter,
            "verseNumber":verse_number
        }
        for verse in verses:
            data["verseText"] = verse["verse"]

        return data    
    else:
        return {"msg":"provided wrong reference"}   




#FUNCTION FOR FETCH WORD special       
def fetchword(word,session):
    word = word.upper()
    word_id = null
    word_list =[]
    query_check = session.query(KeyWord).filter(KeyWord.englishtrans == word)
    if query_check.count():
        for query in query_check:
            word_id = query.id
        #m_qr = session.query(MlBook).join(keytoverse).join(EnBook).filter(keytoverse.key_id == word_id)

        create_view_statement = text(f"""CREATE VIEW mlandkey as  SELECT ml_books.id, ml_books.book, ml_books.chapter, ml_books.versenum, ml_books.verse
FROM ml_books JOIN keytoverse ON ml_books.id = keytoverse.verse_id_ml
WHERE keytoverse.key_id = {word_id}""") 

        merge_statement = text("""CREATE VIEW finalview as select m.book,m.chapter,m.versenum,m.verse, g.verse as enverse from mlandkey m join en_books g on 
m.book = g.book and m.chapter = g.chapter and m.versenum = g.versenum
        """)

        delete_statement = ("""drop view mlandkey""")

        with engine.connect() as con:
            con.execute(create_view_statement)
            con.execute(merge_statement)
            result = con.execute("""SELECT * FROM finalview""")
            for r in result:
                d = {
                   "bookcode":r.book,
                   "chapter":r.chapter,
                    "verseNumber":r.versenum,
                    "verse_ml":r.verse,
                    "verse_en":r.enverse
                }
                word_list.append(d)
            con.execute("""drop view finalview""")
            con.execute(delete_statement)
        return word_list    
    else:
        return {"msg":"Keyword is not present. Try a new one"}


#FUNCTION FOR RANDOM WORD FETCH
def randomword(word,session,lang):
    lang_code = lang.capitalize()
    word_list=[]
    if (lang_code == "Ml"):
        db_model = MlBook
    elif (lang_code == "En"):
        db_model = EnBook
    else:
        return {"msg":"Provide a valid language code 'Ml - En'"}

    query_find = session.query(db_model).filter(db_model.verse.contains(word))  
    if query_find.count():
        for q in query_find:
            temp = {
                "Book":q.book,
                "Chapter":q.chapter,
                "VerseNumber":q.versenum,
                "Verse":q.verse
            } 
            word_list.append(temp)
        return word_list    
    else:
        return {"msg":"No Result Found !!"}


'''
SQL JOIN 
select m.versenum, m.verse , k.verse_id , k.key_id from 
ml_books as m inner join (select verse_id, key_id from keytoverse where key_id = 2 ) as k on 
(m.id = k.verse_id )	
'''        

