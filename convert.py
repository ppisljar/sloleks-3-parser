# Downloaded file from https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1230/Sloleks2.0.LMF.zip beforehand

import sys

from tqdm import tqdm

import logging
from os.path import isfile, realpath

from app import session_scope
from app.models import LexicalEntry, WordForm
from app.parser import Parser
from app.progress_bar import TqdmStream

duplicates = {}

class Sloleks:
    def __init__(self, *args, **kwargs):
        self._verbose = kwargs.get("verbose", False)
        #self._logger = self._setup_logger(log_file=kwargs.get("log_file", None))
        self._file = "Sloleks.3.0.zip" 
        if not isfile(realpath(self._file)):
            raise FileNotFoundError("{} does not exist".format(self._file))

    def get_data(self):
        with session_scope() as session:
            p = Parser(session=session, logger=None, verbose=self._verbose)

            i = 0
            for lx in tqdm(
                p.get_lexical_entries(zip_filename=self._file)
            ):
                i = i+1
                
                if session.query(LexicalEntry).get(lx["id"]):
                    if lx["id"] not in duplicates: duplicates[lx["id"]] = 0

                    duplicates[lx["id"]] = duplicates[lx["id"]] + 1
                    idnr = duplicates[lx["id"]]
                    lx["id"] = lx["id"] + "_" + str(idnr)
                    lx["sloleks_key"] = lx["sloleks_key"] + "_" + str(idnr)

                    #if self._verbose:
                    #self._logger.info(f"duplicate lexical entity: {lx['id']} {idnr}")
                    # print(lx)

                lexical_entry = LexicalEntry(
                    **{
                        key: val
                        for key, val in lx.items()
                        if key not in {"word_forms"}
                    },
                )
                session.add(lexical_entry)

                
                for wf in lx["word_forms"]:
                    
                    wforms = {}
                    for x in [1,2,3,4,5,6]:
                        if "form_"+str(x) not in wf: break

                        if wf["form_"+str(x)] in wforms:
                            print(f'duplicte form for lemma {lx["lemma"]}: {wf["form_"+str(x)]}')
                            continue
                        
                        wforms[wf["form_"+str(x)]] = 1

                        # each form should be a separate entry
                        word_form = WordForm(
                            **{
                                key: val
                                for key, val in wf.items()
                                if key not in {"form_representations", "form_1", "form_2", "form_3", "form_4", "form_5", "form_6", "ACC_5", "ACC_6", "ACC_7", "ACC_8", "ACC_9", "ACC_10", "IPA_5", "IPA_6", "IPA_7", "IPA_8", "IPA_9", "IPA_10", "SAMPA_5", "SAMPA_6", "SAMPA_7", "SAMPA_8", "SAMPA_9", "SAMPA_10", "frequency_1", "frequency_2", "frequency_3", "frequency_4", "frequency_5", "frequency_6", "frequency_7", "frequency_8", "frequency_9", "frequency_10"}
                            },
                            lexical_entry_id=lx["id"],
                            form=wf["form_"+str(x)],
                            frequency=wf["frequency_"+str(x)] if "frequency_"+str(x) in wf else 0
                            # acc, sampa and ipa .... how to match them to forms ? for now we leave it out with plan to regenerate them
                        )
                    i = i + 1
                    session.add(word_form)

                if i % 10 == 0:
                    session.commit()
            session.commit()
            print(duplicates)
                

    @classmethod
    def _setup_logger(cls, log_file=None):
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        screen_handler = logging.StreamHandler(TqdmStream)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger(cls.__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(screen_handler)

        if log_file:
            file_handler = logging.FileHandler(realpath(log_file), mode="w")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-file", dest="log_file", help="Log file")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Be verbose when parsing the data :v",
    )
    args = parser.parse_args()

    lex = Sloleks(
        log_file=args.log_file, verbose=args.verbose
    )
    lex.get_data()
