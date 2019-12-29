from sqlalchemy import Column, Integer, String, Table, ForeignKey, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class LexicalEntry(Base):
    __tablename__ = "lexical_entries"
    id = Column(CHAR(35), primary_key=True)
    kljuc = Column(String(64), index=True)
    zapis = Column(String(32), nullable=True)
    besedna_vrsta = Column(String(32), nullable=True)
    vrsta = Column(String(32), nullable=True)
    norma = Column(String(32), nullable=True)
    SPSP = Column(String(32), nullable=True)
    SP2001 = Column(String(32), nullable=True)
    tip = Column(String(32), nullable=True)
    vid = Column(String(32), nullable=True)
    spol_svojine = Column(String(32), nullable=True)
    stevilo_svojine = Column(String(32), nullable=True)

    def __repr__(self):
        return f"<LexicalEntry {self.id}>"


class Lemma(Base):
    __tablename__ = "lemmas"
    id = Column(Integer, primary_key=True)
    zapis_oblike = Column(String(255), index=True)
    naglasena_beseda_1 = Column(String(255), nullable=True)
    naglasena_beseda_2 = Column(String(255), nullable=True)
    naglasena_beseda_3 = Column(String(255), nullable=True)
    naglasena_beseda_4 = Column(String(255), nullable=True)
    lexical_entry_id = Column(
        CHAR(35), ForeignKey("lexical_entries.id"), nullable=False, index=True
    )
    lexical_entry = relationship(
        "LexicalEntry",
        backref=backref("lemmas", cascade="all, delete-orphan", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<Lemma {self.zapis_oblike}/>"


class WordForm(Base):
    __tablename__ = "word_forms"
    id = Column(Integer, primary_key=True)
    msd = Column(String(32), nullable=True)
    stevilo = Column(String(32), nullable=True)
    stopnja = Column(String(32), nullable=True)
    sklon = Column(String(32), nullable=True)
    dolocnost = Column(String(32), nullable=True)
    nikalnost = Column(String(32), nullable=True)
    zivost = Column(String(32), nullable=True)
    spol = Column(String(32), nullable=True)
    spol_svojine = Column(String(32), nullable=True)
    stevilo_svojine = Column(String(32), nullable=True)
    oblika = Column(String(32), nullable=True)
    oseba = Column(String(32), nullable=True)
    lexical_entry_id = Column(
        CHAR(35), ForeignKey("lexical_entries.id"), nullable=False, index=True
    )
    lexical_entry = relationship(
        "LexicalEntry",
        backref=backref("word_forms", cascade="all, delete-orphan", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<WordForm {self.msd}/>"


class FormRepresentation(Base):
    __tablename__ = "form_representations"
    id = Column(Integer, primary_key=True)
    zapis_oblike = Column(String(255), index=True)
    SPSP = Column(String(32), nullable=True)
    norma = Column(String(32), nullable=True)
    tip = Column(String(32), nullable=True)
    pogostnost = Column(Integer, default=0)
    naglasena_beseda_1 = Column(String(255), nullable=True)
    naglasena_beseda_2 = Column(String(255), nullable=True)
    naglasena_beseda_3 = Column(String(255), nullable=True)
    naglasena_beseda_4 = Column(String(255), nullable=True)
    SAMPA_1 = Column(String(255), nullable=True)
    SAMPA_2 = Column(String(255), nullable=True)
    SAMPA_3 = Column(String(255), nullable=True)
    SAMPA_4 = Column(String(255), nullable=True)
    IPA_1 = Column(String(255), nullable=True)
    IPA_2 = Column(String(255), nullable=True)
    IPA_3 = Column(String(255), nullable=True)
    IPA_4 = Column(String(255), nullable=True)
    word_form_id = Column(
        Integer, ForeignKey("word_forms.id"), nullable=False, index=True
    )
    word_form = relationship(
        "WordForm",
        backref=backref(
            "form_representations", cascade="all, delete-orphan", lazy="dynamic"
        ),
    )
    lexical_entry_id = Column(
        CHAR(35), ForeignKey("lexical_entries.id"), nullable=False, index=True
    )
    lexical_entry = relationship(
        "LexicalEntry",
        backref=backref(
            "form_representations", cascade="all, delete-orphan", lazy="dynamic"
        ),
    )
