import sys
import zipfile
from os.path import isfile

from lxml import etree
from sqlalchemy.orm import Session


class Parser:
    def __init__(self, *args, **kwargs):
        self._verbose = kwargs.get("verbose", False)
        self._logger = kwargs.get("logger")
        self._session = kwargs.get("session")
        if not self._session:
            self._logger.critical("Session undefined")
            sys.exit(1)
        if not isinstance(self._session, Session):
            self._logger.critical("Session must be of type session")
            sys.exit(1)
        self._data = None

    @classmethod
    def get_lexical_entries(cls, zip_filename):
        if isfile(zip_filename):
            print(" loading zip file ...")
            with zipfile.ZipFile(zip_filename, "r") as zfh:
                names = zfh.namelist()
                names.sort()
                for name in names:
                    if name.endswith("/"):
                        continue
                    if name.endswith(".xml"):
                        print(f" processing file {name} ...")
                        yield from cls._parse(zfh.open(name))
        else:
            raise OSError(f"{zip_filename} does not exist!")

    @staticmethod
    def _parse(file):
        current = None
        previous = None
        lexical_entry = {
            "id": None,
            "word_forms": [],
        }

        context = etree.iterparse(file, events=("start", "end"))
        _, root = next(context)

        for event, element in context:
            if element.tag == "entry":
                if event == "start":
                    current = element.tag
                    previous = None
                    word_form = {}
                elif event == "end":
                    yield lexical_entry
                    current = None
                    previous = None
                    lexical_entry = {
                        "id": None,
                        "word_forms": [],
                    }
                    root.clear()

            elif element.tag == "lemma":
                if event == "start":
                    previous = current
                    current = element.tag
                    if element.text is not None:
                        lexical_entry["lemma"] = element.text.strip()
                elif event == "end":
                    current = previous
                    previous = None

            elif element.tag == "lexicalUnit":
                if event == "start":
                    previous = current
                    current = element.tag

                    lexical_entry["id"] = element.attrib["sloleksId"]
                    lexical_entry["sloleks_key"] = element.attrib["sloleksKey"]
                    lexical_entry["norma"] = element.attrib["type"]
                    lexeme = element.find(".//lexeme")
                    if lexeme is not None and lexeme.text is not None:
                        lexical_entry["lexeme"] = lexeme.text.strip()

                elif event == "end":
                    current = previous
                    previous = None

            elif element.tag == "grammar":
                if event == "start":
                    previous = current
                    current = element.tag

                    category = element.find(".//category")
                    if category is not None and category.text is not None:
                        lexical_entry["type"] = category.text.strip()
                    
                    subcategory = element.find(".//subcategory")
                    if subcategory is not None and subcategory.text is not None:
                        lexical_entry["pronaunciation"] = subcategory.text.strip()

                elif event == "end":
                    current = previous
                    previous = None

            elif element.tag == "wordForm":
                if event == "start":
                    previous = current
                    current = element.tag

                    msd = element.find("msd")
                    if msd is not None and msd.text is not None:
                        word_form["msd"] = msd.text.strip()

                    vform = element.find(".//grammarFeature[@name='vform']")
                    if vform is not None and vform.text is not None:
                        word_form["oblika"] = vform.text.strip()

                    number = element.find(".//grammarFeature[@name='number']")
                    if number is not None and number.text is not None:
                        word_form["stevilo"] = number.text.strip()

                    gender = element.find(".//grammarFeature[@name='gender']")
                    if gender is not None and gender.text is not None:
                        word_form["spol"] = gender.text.strip()

                    degree = element.find(".//grammarFeature[@name='degree']")
                    if degree is not None and degree.text is not None:
                        word_form["stopnja"] = degree.text.strip()

                    case = element.find(".//grammarFeature[@name='case']")
                    if case is not None and case.text is not None:
                        word_form["sklon"] = case.text.strip()

                    definiteness = element.find(".//grammarFeature[@name='definiteness']")
                    if definiteness is not None and definiteness.text is not None:
                        word_form["dolocnost"] = definiteness.text.strip()

                    person = element.find(".//grammarFeature[@name='person']")
                    if person is not None and person.text is not None:
                        word_form["oseba"] = person.text.strip()

                    orthography = element.find(".//orthography")
                    if orthography is not None:
                        word_form["tip"] = orthography.get("morphologyPatterns")
                        orthographyForm = orthography.find("form")
                        if orthographyForm is not None and orthographyForm.text is not None:
                            word_form["zapis_oblike"] = orthographyForm.text.strip()

                    accentuation = element.find(".//accentuation/form")
                    if accentuation is not None and accentuation.text is not None:
                        word_form["naglasena_beseda_1"] = accentuation.text.strip()

                    # Find the first pronunciation element and extract IPA and SAMPA forms
                    first_pronunciation = element.find(".//pronunciationList/pronunciation")
                    if first_pronunciation is not None:
                        ipa_form = first_pronunciation.find(".//form[@script='IPA']")
                        if ipa_form is not None and ipa_form.text is not None:
                            word_form["IPA_1"] = ipa_form.text.strip()

                        sampa_form = first_pronunciation.find(".//form[@script='SAMPA']")
                        if sampa_form is not None and sampa_form.text is not None:
                            word_form["SAMPA_1"] = sampa_form.text.strip()


                elif event == "end":
                    current = previous
                    previous = None
                    lexical_entry["word_forms"].append(word_form)
                    word_form = {}()


                elif event == "end":
                    current = previous
                    previous = None
                    lexical_entry["word_forms"].append(word_form)
                    word_form = {}