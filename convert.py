# Downloaded file from https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1230/Sloleks2.0.LMF.zip beforehand

import sys

from tqdm import tqdm

import logging
from os.path import isfile, realpath

from app import session_scope
from app.models import LexicalEntry, WordForm
from app.parser import Parser
from app.progress_bar import TqdmStream


class Sloleks:
    def __init__(self, *args, **kwargs):
        self._verbose = kwargs.get("verbose", False)
        self._logger = self._setup_logger(log_file=kwargs.get("log_file", None))
        self._file = "Sloleks.3.0.zip"
        if not isfile(realpath(self._file)):
            raise FileNotFoundError("{} does not exist".format(self._file))

    def get_data(self):
        with session_scope(logger=self._logger) as session:
            p = Parser(session=session, logger=self._logger, verbose=self._verbose)

            i = 0
            for lx in tqdm(
                p.get_lexical_entries(zip_filename=self._file)
            ):
                i = i+1
                lexical_entry = LexicalEntry(
                    **{
                        key: val
                        for key, val in lx.items()
                        if key not in {"word_forms"}
                    },
                )
                if not session.query(LexicalEntry).get(lx["id"]):
                    session.add(lexical_entry)
                else:
                    #if self._verbose:
                    self._logger.info(
                        f"Skipping lexical entity: {lx['id']}"
                    )

                for wf in lx["word_forms"]:
                    word_form = WordForm(
                        **{
                            key: val
                            for key, val in wf.items()
                            if key not in {"form_representations"}
                        },
                        lexical_entry_id=lx["id"]
                    )
                    i = i + 1
                    session.add(word_form)

                if 1 % 1000 == 0:
                    session.commit()
                

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

    try:
        lex = Sloleks(
            log_file=args.log_file, verbose=args.verbose
        )
        lex.get_data()
    except KeyboardInterrupt:
        print("\nProcess interrupted Exiting...")
        sys.exit(1)
