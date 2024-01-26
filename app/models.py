from sqlalchemy import Column, Integer, String, Table, ForeignKey, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class LexicalEntry(Base):
    __tablename__ = "lexical_entries"
    id = Column(CHAR(35), primary_key=True)
    status = Column(String(16), nullable=True)
    sloleks_key = Column(String(64), index=True)
    lemma = Column(String(64), nullable=True)
    lexeme = Column(String(64), index=True)
    lexeme_type = Column(String(16), nullable=True)
    type = Column(String(16), nullable=True)
    category = Column(String(16), nullable=True)
    pronaunciation = Column(String(16), nullable=True)
    aspect = Column(String(16), nullable=True)
    frequency = Column(Integer, nullable=True)
    msd = Column(String(16), nullable=True)
    source = Column(String(64), index=True)

    def __repr__(self):
        return f"<LexicalEntry {self.id}>"


class WordForm(Base):
    __tablename__ = "word_forms"
    id = Column(Integer, primary_key=True)
    msd = Column(String(16), nullable=True)         #
    msd_system = Column(String(16), nullable=True)  #
    msd_language = Column(String(4), nullable=True)# 
    morphological_pattern_code = Column(String(16), nullable=True) 

    vform = Column(String(16), nullable=True)       # oblika
    number = Column(String(16), nullable=True)      # stevilo
    gender = Column(String(16), nullable=True)      # spol
    type = Column(String(16), nullable=True)          # tip
    person = Column(String(16), nullable=True)          # oseba
    negative = Column(String(16), nullable=True)        # nikalnost
    degree = Column(String(16), nullable=True)         # stopnja
    definiteness = Column(String(16), nullable=True)  # dolocnost
    case = Column(String(16), nullable=True)          # sklon
    aspect = Column(String(16), nullable=True)        # norma
    animate = Column(String(16), nullable=True)        # zivost
    clitic =Column(String(16), nullable=True)     # 
    owner_gender = Column(String(16), nullable=True)   # 
    owner_number = Column(String(16), nullable=True)   # 

    frequency = Column(Integer, nullable=True)      # pogostost

    form = Column(String(64), index=True)

    ACC_1 = Column(String(64), nullable=True)
    ACC_2 = Column(String(64), nullable=True)
    ACC_3 = Column(String(64), nullable=True)
    ACC_4 = Column(String(64), nullable=True)
    SAMPA_1 = Column(String(64), nullable=True)
    SAMPA_2 = Column(String(64), nullable=True)
    SAMPA_3 = Column(String(64), nullable=True)
    SAMPA_4 = Column(String(64), nullable=True)
    IPA_1 = Column(String(64), nullable=True)
    IPA_2 = Column(String(64), nullable=True)
    IPA_3 = Column(String(64), nullable=True)
    IPA_4 = Column(String(64), nullable=True)

    lexical_entry_id = Column(
        CHAR(35), ForeignKey("lexical_entries.id"), nullable=False, index=True
    )
    lexical_entry = relationship(
        "LexicalEntry",
        backref=backref("word_forms", cascade="all, delete-orphan", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<WordForm {self.msd}/>"

