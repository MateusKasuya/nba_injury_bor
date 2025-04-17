import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.request_report import get_valid_report_url

if __name__ == '__main__':
    get_valid_report_url()
