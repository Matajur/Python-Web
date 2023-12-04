import argparse
import logging
from pathlib import Path
from shutil import copyfile
from threading import Thread, Semaphore
from time import time

"""
python sorter --source -s SourceFolder
python sorter --output -o OutputFolder
"""

parser = argparse.ArgumentParser(description="App for sorting files in folder")
parser.add_argument("-s", "--source", help="Source folder", required=True)
parser.add_argument("-o", "--output", help="Output folder")
args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")

source_folder = Path(source)
if output:
    output_folder = Path(output)
else:
    output_folder = Path(f"{source} (sorted)")

threads = []


def parse_folder(path: Path, condition: Semaphore) -> None:
    with condition:
        logging.debug(f"Start parsing folder '{path}'")
        for el in path.iterdir():
            if el.is_file():
                th = Thread(target=handle_file, args=(el, condition))
                th.start()
                threads.append(th)
            else:
                th = Thread(target=parse_folder, args=(el, condition))
                th.start()
                threads.append(th)
        logging.debug(f"End parsing folder '{path}'")


def handle_file(file: Path, condition: Semaphore) -> None:
    with condition:
        logging.debug(f"Start handling file '{file}'")
        ext = file.suffix.lstrip(".")
        new_path = output_folder / ext
        if not ext:
            new_path = output_folder / "!unknown"
        try:
            new_path.mkdir(exist_ok=True, parents=True)
            copyfile(file, new_path / file.name)
        except OSError as e:
            logging.error(e)
        logging.debug(f"End handling file '{file}'")


if __name__ == "__main__":
    timer = time()
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    pool = Semaphore(10)

    thread = Thread(target=parse_folder, args=(source_folder, pool))
    thread.start()
    threads.append(thread)

    [th.join() for th in threads]

    print(
        f"Sorting files is finished, folder '{source}' can be deleted\nOperation has taken {round(time() - timer, 4)}s"
    )
