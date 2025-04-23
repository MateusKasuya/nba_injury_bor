import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.request_report import NBAInjuryReport

if __name__ == '__main__':
    report = NBAInjuryReport()

    report.request_report()
    
    
