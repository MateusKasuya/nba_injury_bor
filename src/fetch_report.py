import requests
from datetime import datetime
from typing import Optional

BASE_URL = "https://ak-static.cms.nba.com/referee/injury/Injury-Report_"
TIMES = ["01AM", "02AM", "03AM", "04AM", "05AM", "06AM", "07AM", "08AM", "09AM", "10AM", "11AM", "12PM", "01PM", "02PM","03PM","04PM","05PM","06PM","07PM","08PM","09PM","10PM","11PM", "12AM"]


def get_valid_report_url() -> Optional[str]:
    today = datetime.today().strftime("%Y-%m-%d")

    for time_slot in TIMES:
        url = f"{BASE_URL}{today}_{time_slot}.pdf"
        response = requests.head(url)
        if response.status_code == 200:
            print(f"✅ Encontrado: {url}")
            return url
        else:
            print(f"❌ Não encontrado: {url}")
    
    print("Nenhum relatório encontrado para hoje.")
    return None
