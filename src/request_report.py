from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests

import io
import re
from pypdf import PdfReader


class NBAInjuryReport:
    def __init__(self):
        pass

    def _get_zone_info(self):
        US_TZ = ZoneInfo("America/New_York")

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
            hour_str = "12AM"

        elif current_hour < 12:
            hour_str = f"{current_hour:02}AM"

        elif current_hour == 12:
            hour_str = "12PM"

        else:
            hour_str = f"{current_hour - 12:02}PM"

        current_date = str(current_date)
        time_str = f"{current_date}_{hour_str}"

        return time_str

    def _request_report(self) -> bytes:
        BASE_URL = "https://ak-static.cms.nba.com/referee/injury/Injury-Report_"
        time_str = self._transform_time_to_str()

        dynamic_url = f"{BASE_URL}{time_str}.pdf"
        head_response = requests.head(dynamic_url)
        status_code = head_response.status_code

        if status_code == 200:
            print(f"✅ Encontrado: {dynamic_url}")
            response = requests.get(dynamic_url)

            content = response.content

            return content

        else:
            print(f"❌ Relatório não encontrado para {time_str}.")

            return None

    def _bytes_to_stream(self):
        content = self._request_report()
        content_stream = io.BytesIO(content)

        return content_stream

    def _pdf_reader(self):
        reader = PdfReader(self._bytes_to_stream())

        # Lê todas as páginas
        raw_text = ""
        for idx, page in enumerate(reader.pages):
            raw_text += f"\n=== PAGE {idx + 1} ===\n"
            raw_text += page.extract_text() + "\n"

        # Tokeniza por palavra
        tokens = [t.strip() for t in raw_text.split() if t.strip()]

        games = []
        i = 0
        current_game = None
        current_team = None

        status_options = {"Out", "Available", "Questionable", "Doubtful"}

        while i < len(tokens):
            # Detecta novo jogo: horário + (ET) + matchup
            if re.match(r"\d{2}:\d{2}", tokens[i]) and (
                i + 2 < len(tokens) and "@" in tokens[i + 2]
            ):
                if current_game:
                    games.append(current_game)

                current_game = {
                    "time": f"{tokens[i]} {tokens[i + 1]}",
                    "matchup": tokens[i + 2],
                    "teams": [],
                }
                current_team = None
                i += 3
                continue

            # Detecta jogador (nome + status + razão)
            elif (
                "," in tokens[i]
                and i + 2 < len(tokens)
                and tokens[i + 2] in status_options
            ):
                player_name = f"{tokens[i]} {tokens[i + 1]}"
                status = tokens[i + 2]
                reason_tokens = []
                i += 3
                while i < len(tokens):
                    token = tokens[i]
                    if (
                        token in status_options
                        or re.match(r"\d{2}:\d{2}", token)
                        or "," in token
                    ):
                        break
                    reason_tokens.append(token)
                    i += 1
                reason = " ".join(reason_tokens)

                if current_team:
                    current_team["players"].append(
                        {"name": player_name, "status": status, "reason": reason}
                    )
                continue

            # Detecta nome do time (título contínuo com palavras sem pontuação)
            elif (
                tokens[i].istitle() and i + 1 < len(tokens) and tokens[i + 1].istitle()
            ):
                team_tokens = []
                while (
                    i < len(tokens)
                    and tokens[i].istitle()
                    and "," not in tokens[i]
                    and tokens[i] not in status_options
                ):
                    team_tokens.append(tokens[i])
                    i += 1

                possible_team = " ".join(team_tokens)
                if (
                    current_game
                    and possible_team
                    and not any(
                        t.get("name") == possible_team for t in current_game["teams"]
                    )
                ):
                    current_team = {"name": possible_team, "players": []}
                    current_game["teams"].append(current_team)
                continue

            else:
                i += 1

        if current_game:
            games.append(current_game)

        return games

    # def export_to_json(self, filepath="data/injury_report.json"):
    #     data = self.pdf_reader()
    #     with open(filepath, "w", encoding="utf-8") as f:
    #         json.dump(data, f, ensure_ascii=False, indent=2)
    #     print(f"✅ Relatório salvo em {filepath}")

    # def caracters_lenght(self):
    #     data = self._pdf_reader()

    #     for element in data:

    #         print(type(element))
    #         print(len(str(element)))
    #         print(element)
