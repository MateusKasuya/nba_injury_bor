import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.request_report import NBAInjuryReport
from src.postx import create_tweet

if __name__ == "__main__":
    report = NBAInjuryReport()
    games = report._pdf_reader()

    for game in games:
        text = str(game)

        if len(text) <= 280:
            create_tweet(text=text)
        else:
            create_tweet(text=text[:280])

    # for game in games:

    #     print(str(game))
    # create_tweet(text= str(game))
