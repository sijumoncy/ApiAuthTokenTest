from sqlalchemy import MetaData,Column,String,Integer,Boolean,Text,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



metadata = MetaData()
Base = declarative_base()

class MlBook(Base):
    __tablename__ = 'ml_books'

    id = Column(Integer,primary_key=True,autoincrement=True)
    book = Column(String(50))
    chapter = Column(Integer)
    versenum  = Column(Integer)
    verse = Column(Text)

class EnBook(Base):
    __tablename__ = 'en_books'

    id = Column(Integer,primary_key=True,autoincrement=True)
    book = Column(String(50))
    chapter = Column(Integer)
    versenum  = Column(Integer)
    verse = Column(Text)


class KeyWord(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String)
    englishtrans = Column(String)
    #reference = Column(Integer, ForeignKey('ml_books.id'))
    description = Column(Text)

class keytoverse(Base):
    __tablename__ = 'keytoverse'

    id = Column(Integer,primary_key=True)
    verse_id_ml = Column(Integer, ForeignKey('ml_books.id'))
    verse_id_en = Column(Integer, ForeignKey('en_books.id'))   
    key_id = Column(Integer, ForeignKey('keywords.id'))    




