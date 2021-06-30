from sqlalchemy.sql.expression import null, text
from models import MlBook,EnBook,KeyWord,keytoverse
import pandas as pd
from sqlalchemy import func,or_,and_


#Function to add Books data from JSON
def dbentry(jsonobj, sessionobj, lang):

#checking which language is coming
    session = sessionobj
    if (lang == "Ml"):
        db_model = MlBook
    elif (lang == "En"):
        db_model = EnBook

#extracting common data from the input         
    book_code = (jsonobj["book"]['bookCode']).upper()
    chapter_data = jsonobj["chapters"]
    total_chapters = len(chapter_data)


#checking for data exist
#adding data to database
    book_query = session.query(db_model).filter(db_model.book == book_code).first()
    if book_query:
        print("Book Already Saved")
    else:
        for i in range(total_chapters):
            book_entry = []
            chapterNum = chapter_data[i]["chapterNumber"]
            contents = chapter_data[i]["contents"]
            for content in range(len(contents)):
                
                new_entry = db_model(
                    book = book_code,  
                    chapter = int(chapterNum),
                    versenum = int(contents[content]["verseNumber"]),
                    verse =    contents[content]["verseText"]
                )
                book_entry.append(new_entry)

        session.add_all(book_entry)
        session.commit()   

#adding keywords tables after malayalm book added
    keywordadd(session,db_model)


#Function to add special keyword reference

def keywordadd(session,db_model):
    df = pd.read_csv(r'inputfiles\biblewords.csv')
    keyword_dict = df.to_dict()
    keyword_entry = []

#entry all special words to db and check for duplication        
    for indx in range(len(keyword_dict['SL.No'])):
        spl_word = keyword_dict['Special words'][indx]
        query_spl = session.query(KeyWord).filter(KeyWord.word == spl_word)
        #print(query_spl.count())
        if  query_spl.count() == 0:
            new_entry = KeyWord(
                                word = spl_word,  
                                englishtrans = (keyword_dict['English translation'][indx]).upper(),
                                description =  keyword_dict['Description'][indx]
                            )
            session.add(new_entry)
            session.commit()
            session.refresh(new_entry)
#adding reference of special words to versetokey based on language upload
    rows = session.query(KeyWord)
    query_find_count = 0
    for row in rows:
        current_id = row.id
        if db_model == MlBook:
            current_word = row.word
            query_find = session.query(db_model).filter(db_model.verse.contains(current_word))
            query_find_count =  query_find.count()
        elif db_model == EnBook:
            current_word = row.englishtrans
            current_word_l = current_word.lower()
            current_word_c = current_word.capitalize()
            query_find = session.query(db_model).filter(or_(db_model.verse.contains(current_word_l),db_model.verse.contains(current_word_c)))
            query_find_count =  query_find.count()
        #print(current_word)    
        #print(query_find.count())
        if query_find_count:
            for q in query_find:
                v_id = q.id
                if db_model == MlBook:
                    query_exist = session.query(keytoverse)\
                    .filter(and_(keytoverse.key_id == current_id,keytoverse.verse_id_ml == v_id))
                    if query_exist.count() == 0:
                        new_entry = keytoverse(
                                        verse_id_ml =  v_id, 
                                        key_id =  current_id  
                                    )
                        session.add(new_entry)
                        session.commit()
                elif db_model == EnBook:
                    query_exist = session.query(keytoverse)\
                    .filter(and_(keytoverse.key_id == current_id,keytoverse.verse_id_en == v_id))
                    if query_exist.count() == 0:
                        new_entry = keytoverse(
                                        verse_id_en =  v_id, 
                                        key_id =  current_id  
                                    )
                        session.add(new_entry)
                        session.commit()
                        