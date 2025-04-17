from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests


class NBAInjuryReport:
    def __init__(self):
        pass

    def _get_zone_info(self):
        US_TZ = ZoneInfo('America/New_York')

        return US_TZ

    def _get_current_datetime(self) -> datetime:
        current_datetime = datetime.now(tz=self._get_zone_info())

        return current_datetime

    def _get_current_date(self, current_datetime: datetime) -> date:
        current_date = current_datetime.date()

        return current_date

    def _get_current_hour(self, current_datetime: datetime) -> int:
        current_hour = current_datetime.hour

        return current_hour

    def _get_current_minute(self, current_datetime: datetime) -> int:
        current_minute = current_datetime.minute

        return current_minute

    def _get_datetime_elements(self) -> tuple:
        current_datetime = self._get_current_datetime()

        current_date = self._get_current_date(current_datetime)
        current_hour = self._get_current_hour(current_datetime)
        current_minute = self._get_current_minute(current_datetime)

        return current_date, current_hour, current_minute

    def _transform_time_to_str(self) -> str:

        (
            current_date,
            current_hour,
            current_minute,
        ) = self._get_datetime_elements()

        if current_minute < 30:
            current_hour = current_hour - 1

        if current_hour == 0:
            hour_str = '12AM'

        elif current_hour < 12:
            hour_str = f'{current_hour:02}AM'

        elif current_hour == 12:
            hour_str = '12PM'

        else:
            hour_str = f'{current_hour - 12:02}PM'

        current_date = str(current_date)
        time_str = f'{current_date}_{hour_str}'

        return time_str

    def request_report(self) -> bytes:
        BASE_URL = (
            'https://ak-static.cms.nba.com/referee/injury/Injury-Report_'
        )
        time_str = self._transform_time_to_str()

        dynamic_url = f'{BASE_URL}{time_str}.pdf'
        head_response = requests.head(dynamic_url)
        status_code = head_response.status_code

        if status_code == 200:
            print(f'✅ Encontrado: {dynamic_url}')
            response = requests.get(dynamic_url)

            content = response.content

            return content

        else:
            print(f'❌ Relatório não encontrado para {time_str}.')

            return None
