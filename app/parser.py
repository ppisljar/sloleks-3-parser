import sys
import zipfile
from os.path import isfile

from lxml import etree
from sqlalchemy.orm import Session

from slovene_g2p import SloveneG2P
from slovene_form_generator import Mte6Translate, PatternPredictor
from slovene_accentuator import SloveneAccentuator

mte_translate = Mte6Translate()
accentuator = SloveneAccentuator()
predictor = PatternPredictor()
g2p = SloveneG2P()

class Parser:
    def __init__(self, *args, **kwargs):
        self._verbose = kwargs.get("verbose", True)
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
                        yield from cls._parse(zfh.open(name), name)
        else:
            raise OSError(f"{zip_filename} does not exist!")

    @staticmethod
    def _parse(file, fname):
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
                    
                elif event == "end":
                    if element.text is not None:
                        lexical_entry["lemma"] = element.text.strip()

                    current = previous
                    previous = None

            elif element.tag == "status":
                if event == "start":
                    previous = current
                    current = element.tag
                    
                elif event == "end":
                    if element.text is not None:
                        lexical_entry["status"] = element.text.strip()

                    current = previous
                    previous = None

            elif element.tag == "measureList":
                if event == "start":
                    previous = current
                    current = element.tag
                    

                elif event == "end":
                    freq = element.find(".//measure")
                    if freq is not None and freq.text is not None:
                        lexical_entry["frequency"] = freq.text.strip()

                    current = previous
                    previous = None

            elif element.tag == "lexicalUnit":
                if event == "start":
                    previous = current
                    current = element.tag
                    

                elif event == "end":
                    lexical_entry["source"] = fname
                    lexical_entry["id"] = element.attrib["sloleksId"]
                    lexical_entry["sloleks_key"] = element.attrib["sloleksKey"]
                    lexical_entry["lexeme_type"] = element.attrib["type"]
                    lexeme = element.find(".//lexeme")
                    if lexeme is not None and lexeme.text is not None:
                        lexical_entry["lexeme"] = lexeme.text.strip()

                    current = previous
                    previous = None

            elif element.tag == "grammar":
                if event == "start":
                    previous = current
                    current = element.tag

                elif event == "end":
                    category = element.find(".//category")
                    if category is not None and category.text is not None:
                        lexical_entry["category"] = category.text.strip()
                    
                    subcategory = element.find(".//subcategory")
                    if subcategory is not None and subcategory.text is not None:
                        lexical_entry["pronaunciation"] = subcategory.text.strip()

                    subcategory = element.find(".//grammarFeature[@name='type']")
                    if subcategory is not None and subcategory.text is not None:
                        lexical_entry["type"] = subcategory.text.strip()

                    subcategory = element.find(".//grammarFeature[@name='aspect']")
                    if subcategory is not None and subcategory.text is not None:
                        lexical_entry["aspect"] = subcategory.text.strip()

                    current = previous
                    previous = None

            elif element.tag == "wordForm":
                if event == "start":
                    previous = current
                    current = element.tag

                
                elif event == "end":
                    msd = element.find("msd")
                    if msd is not None and msd.text is not None:
                        word_form["msd"] = msd.text.strip()
                        lexical_entry["msd"] = mte_translate.get_lemma_msd(msd.text.strip())
                        word_form["msd_language"] = msd.get("language")
                        word_form["msd_system"] = msd.get("system")

                    vform = element.find(".//grammarFeature[@name='vform']")
                    if vform is not None and vform.text is not None:
                        word_form["vform"] = vform.text.strip()

                    number = element.find(".//grammarFeature[@name='number']")
                    if number is not None and number.text is not None:
                        word_form["number"] = number.text.strip()

                    gender = element.find(".//grammarFeature[@name='gender']")
                    if gender is not None and gender.text is not None:
                        word_form["gender"] = gender.text.strip()

                    degree = element.find(".//grammarFeature[@name='degree']")
                    if degree is not None and degree.text is not None:
                        word_form["degree"] = degree.text.strip()

                    case = element.find(".//grammarFeature[@name='case']")
                    if case is not None and case.text is not None:
                        word_form["case"] = case.text.strip()

                    definiteness = element.find(".//grammarFeature[@name='definiteness']")
                    if definiteness is not None and definiteness.text is not None:
                        word_form["definiteness"] = definiteness.text.strip()

                    person = element.find(".//grammarFeature[@name='person']")
                    if person is not None and person.text is not None:
                        word_form["person"] = person.text.strip()


                    type = element.find(".//grammarFeature[@name='type']")
                    if type is not None and type.text is not None:
                        word_form["type"] = type.text.strip()

                    negative = element.find(".//grammarFeature[@name='negative']")
                    if negative is not None and negative.text is not None:
                        word_form["negative"] = negative.text.strip()

                    aspect = element.find(".//grammarFeature[@name='aspect']")
                    if aspect is not None and aspect.text is not None:
                        word_form["aspect"] = aspect.text.strip()

                    animate = element.find(".//grammarFeature[@name='animate']")
                    if animate is not None and animate.text is not None:
                        word_form["animate"] = animate.text.strip()

                    clitic = element.find(".//grammarFeature[@name='clitic']")
                    if clitic is not None and clitic.text is not None:
                        word_form["clitic"] = clitic.text.strip()

                    owner_gender = element.find(".//grammarFeature[@name='owner_gender']")
                    if owner_gender is not None and owner_gender.text is not None:
                        word_form["owner_gender"] = owner_gender.text.strip()

                    owner_number = element.find(".//grammarFeature[@name='owner_number']")
                    if owner_number is not None and owner_number.text is not None:
                        word_form["owner_number"] = owner_number.text.strip()

                    ortographies = element.findall(".//orthography")
                    orthography = ortographies[0] if len(ortographies) > 0 else None

                    if len(ortographies) > 2: 
                        print(f'more than two ortography! {lexical_entry["lemma"]} {len(ortographies)}')
                        
                    o = 0
                    for orthography in ortographies:
                        o+=1    
                        if 0 > 8: break
                        if orthography is not None:
                            if  "morphological_pattern_code" in word_form and word_form["morphological_pattern_code"] != orthography.get("morphologyPatterns"): 
                                print(f'mpc is not same !!!!')
                                raise Exception('BAD')
                            
                            word_form["morphological_pattern_code"] = orthography.get("morphologyPatterns")
                            orthographyForm = orthography.find("form")
                            if orthographyForm is not None and orthographyForm.text is not None:
                                word_form["form_"+str(o)] = orthographyForm.text.strip()

                            measure = orthography.find(".//measureList/measure")
                            if measure is not None and measure.text is not None:
                                word_form["frequency_" + str(o)] = int(measure.text.strip())

                    accentuations = element.findall(".//accentuation/form")

                    if len(accentuations) == 0: 
                        print(f'no accentuations! {word_form["form_1"]} {len(accentuations)}')
                        #accentuations = element.findall(".//accentuation/form")
                        #print(etree.tostring(element, pretty_print=True))
                        

                    a = 0
                    accs = {}
                    for accentuation in accentuations:
                        a+=1
                        if a > 8: break
                        if accentuation is not None and accentuation.text is not None:
                            if accentuation.text.strip() in accs:
                                continue
                            accs[accentuation.text.strip()] = 1
                            word_form["ACC_"+str(a)] = accentuation.text.strip()

                    # Find the first pronunciation element and extract IPA and SAMPA forms
                    pronunciations = element.findall(".//pronunciationList/pronunciation")

                    if len(pronunciations) == 0: 
                        print(f'no pronunciations! {word_form["form_1"]} {len(pronunciations)}')
                    #    pronunciations = element.findall(".//pronunciationList/pronunciation")
                    #    print(etree.tostring(element, pretty_print=True))
                        
                    p = 0
                    pps = {}
                    for first_pronunciation in pronunciations:
                        p += 1
                        if p > 8: break
                        if first_pronunciation is not None:
                            ipa_form = first_pronunciation.find(".//form[@script='IPA']")
                            if ipa_form is not None and ipa_form.text is not None:
                                if ipa_form.text.strip() in pps:
                                    continue
                                pps[ipa_form.text.strip()] = 1
                                word_form["IPA_" + str(p)] = ipa_form.text.strip()

                            sampa_form = first_pronunciation.find(".//form[@script='SAMPA']")
                            if sampa_form is not None and sampa_form.text is not None:
                                word_form["SAMPA_" + str(p)] = sampa_form.text.strip()


                    if "IPA_1" not in word_form:
                        word_form["IPA_1"] = g2p.ipa(word_form["form_1"], word_form["msd"], predictor.predict_morphological_pattern(lexical_entry["lemma"], word_form["msd"]))

                    if "SAMPA_1" not in word_form:
                        word_form["SAMPA_1"] = g2p.sampa(word_form["form_1"], word_form["msd"], predictor.predict_morphological_pattern(lexical_entry["lemma"], word_form["msd"]))
                
                    current = previous
                    previous = None
                    lexical_entry["word_forms"].append(word_form)
                    word_form = {}