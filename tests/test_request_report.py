from datetime import datetime
from zoneinfo import ZoneInfo

import io
import json

from src.request_report import NBAInjuryReport


# --- TESTE: Transformar datetime em string correta ---
def test_transform_time_to_str_before_half_hour(monkeypatch):
    report = NBAInjuryReport()

    mocked_now = datetime(2025, 4, 17, 14, 15, tzinfo=ZoneInfo("America/New_York"))
    monkeypatch.setattr(report, "_get_current_datetime", lambda: mocked_now)

    result = report._transform_time_to_str()
    assert result == "2025-04-17_01PM"


def test_transform_time_to_str_after_half_hour(monkeypatch):
    report = NBAInjuryReport()

    mocked_now = datetime(2025, 4, 17, 14, 45, tzinfo=ZoneInfo("America/New_York"))
    monkeypatch.setattr(report, "_get_current_datetime", lambda: mocked_now)

    result = report._transform_time_to_str()
    assert result == "2025-04-17_02PM"


# --- TESTE: Requisição do relatório ---
def test_request_report_success(mocker):
    report = NBAInjuryReport()

    mocker.patch.object(
        report, "_transform_time_to_str", return_value="2025-04-17_01PM"
    )
    mock_head = mocker.patch("src.request_report.requests.head")
    mock_head.return_value.status_code = 200

    mock_get = mocker.patch("src.request_report.requests.get")
    mock_get.return_value.content = b"%PDF-FAKE"

    result = report._request_report()

    assert result == b"%PDF-FAKE"
    mock_head.assert_called_once()
    mock_get.assert_called_once()


def test_request_report_not_found(mocker):
    report = NBAInjuryReport()

    mocker.patch.object(
        report, "_transform_time_to_str", return_value="2025-04-17_01PM"
    )
    mock_head = mocker.patch("src.request_report.requests.head")
    mock_head.return_value.status_code = 404

    result = report._request_report()

    assert result is None
    mock_head.assert_called_once()


# --- TESTE: Conversão de bytes para stream ---
def test_bytes_to_stream(mocker):
    report = NBAInjuryReport()

    mocker.patch.object(report, "_request_report", return_value=b"%PDF-FAKE")

    result = report._bytes_to_stream()

    assert isinstance(result, io.BytesIO)
    assert result.read() == b"%PDF-FAKE"


# --- TESTE: Leitura de PDF e parsing do conteúdo ---
# def test_pdf_reader(mocker):
#     report = NBAInjuryReport()

#     # Mocka _bytes_to_stream para qualquer coisa (não importa, já que vamos mockar o PdfReader também)
#     mocker.patch.object(report, '_bytes_to_stream', return_value=io.BytesIO(b"fake pdf content"))

#     # Cria classes fakes corretas para o PdfReader
#     class FakePage:
#         def extract_text(self):
#             return """07:00 PM ORL@BOS
# Orlando Magic
# Suggs, Jalen Out Knee
# Boston Celtics
# Tatum, Jayson Out Wrist
# """

#     class FakeReader:
#         def __init__(self, stream):
#             self.pages = [FakePage()]

#     # Mocka a criação do PdfReader para retornar nosso FakeReader
#     mocker.patch('src.request_report.PdfReader', FakeReader)

#     games = report.pdf_reader()

#     assert isinstance(games, list)
#     assert len(games) == 1
#     assert games[0]["matchup"] == "ORL@BOS"
#     assert len(games[0]["teams"]) == 2
#     assert games[0]["teams"][0]["name"] == "Orlando Magic"
#     assert games[0]["teams"][1]["name"] == "Boston Celtics"


# --- TESTE: Exportação do relatório para JSON ---
def test_export_to_json(tmp_path, mocker):
    report = NBAInjuryReport()

    dummy_data = [{"matchup": "TestMatch", "teams": []}]
    mocker.patch.object(report, "pdf_reader", return_value=dummy_data)

    file_path = tmp_path / "injury_report.json"

    report.export_to_json(filepath=str(file_path))

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    assert data == dummy_data
