import sys
import zipfile
from os.path import isfile

from lxml import etree
from sqlalchemy.orm import Session
from uni2ascii import uni2ascii


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
    def get_lexical_entries(cls, zip_filename, xml_filename):
        if isfile(zip_filename):
            with zipfile.ZipFile(zip_filename, "r") as zfh:
                for name in zfh.namelist():
                    if name.endswith("/"):
                        continue
                    if xml_filename in name:
                        yield from cls._parse(zfh.open(name))
        else:
            raise OSError(f"{zip_filename} does not exist!")

    @staticmethod
    def _parse(file):
        current = None
        previous = None
        lexical_entry = {
            "id": None,
            "lemmas": [],
            "word_forms": [],
            "related_forms": [],
        }
        lemma = {}
        word_form = {"form_representations": []}
        form_representation = {}
        related_form = {}

        context = etree.iterparse(file, events=("start", "end"))
        _, root = next(context)

        for event, element in context:
            if element.tag == "LexicalEntry":
                if event == "start":
                    current = element.tag
                    previous = None
                    lexical_entry["id"] = element.attrib["id"]
                elif event == "end":
                    yield lexical_entry
                    current = None
                    previous = None
                    lexical_entry = {
                        "id": None,
                        "lemmas": [],
                        "word_forms": [],
                        "related_forms": [],
                    }
                    root.clear()

            elif element.tag == "Lemma":
                if event == "start":
                    previous = current
                    current = element.tag
                elif event == "end":
                    current = previous
                    previous = None
                    lexical_entry["lemmas"].append(lemma)
                    lemma = {}

            elif element.tag == "WordForm":
                if event == "start":
                    previous = current
                    current = element.tag
                elif event == "end":
                    current = previous
                    previous = None
                    lexical_entry["word_forms"].append(word_form)
                    word_form = {"form_representations": []}

            elif element.tag == "FormRepresentation":
                if event == "start":
                    previous = current
                    current = element.tag
                elif event == "end":
                    current = previous
                    previous = None
                    word_form["form_representations"].append(form_representation)
                    form_representation = {}

            elif element.tag == "RelatedForm":
                if event == "start":
                    previous = current
                    current = element.tag
                elif event == "end":
                    current = previous
                    previous = None
                    lexical_entry["related_forms"].append(related_form)
                    related_form = {}

            elif element.tag == "feat":
                if event == "start":
                    if current == "Lemma":
                        lemma[uni2ascii(element.attrib["att"])] = element.attrib["val"]
                    elif current == "WordForm":
                        word_form[uni2ascii(element.attrib["att"])] = element.attrib[
                            "val"
                        ]
                    elif current == "FormRepresentation":
                        form_representation[
                            uni2ascii(element.attrib["att"])
                        ] = element.attrib["val"]
                    elif current == "RelatedForm":
                        related_form[uni2ascii(element.attrib["att"])] = element.attrib[
                            "val"
                        ]
                    else:
                        lexical_entry[
                            uni2ascii(element.attrib["att"])
                        ] = element.attrib["val"]
