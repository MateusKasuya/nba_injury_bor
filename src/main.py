import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.request_report import NBAInjuryReport
from src.postx import create_tweet

from datetime import datetime

import time

if __name__ == "__main__":
    report = NBAInjuryReport()
    games = report._pdf_reader()

    for game in games:

        time.sleep(5)

        text = str(game)[:250]  # deixa espaço
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = f"{text} ({timestamp})"

        create_tweet(text=text)


    # for game in games:

    #     print(str(game))
    # create_tweet(text= str(game))
