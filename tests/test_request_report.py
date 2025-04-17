from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from src.request_report import NBAInjuryReport


# --- TESTE 1: Transformar datetime em string correta ---
def test_transform_time_to_str_before_half_hour(monkeypatch):
    report = NBAInjuryReport()

    # Mock datetime antes dos 30 min (ex: 14:15 => busca 13PM)
    mocked_now = datetime(
        2025, 4, 17, 14, 15, tzinfo=ZoneInfo('America/New_York')
    )
    monkeypatch.setattr(report, '_get_current_datetime', lambda: mocked_now)

    result = report._transform_time_to_str()
    assert result == '2025-04-17_01PM'


def test_transform_time_to_str_after_half_hour(monkeypatch):
    report = NBAInjuryReport()

    # Mock datetime depois dos 30 min (ex: 14:45 => busca 14PM)
    mocked_now = datetime(
        2025, 4, 17, 14, 45, tzinfo=ZoneInfo('America/New_York')
    )
    monkeypatch.setattr(report, '_get_current_datetime', lambda: mocked_now)

    result = report._transform_time_to_str()
    assert result == '2025-04-17_02PM'


# --- TESTE 2: Verifica URL montada corretamente e resposta simulada ---
def test_request_report_success(mocker):
    report = NBAInjuryReport()

    # Mock o método de data/hora
    mocker.patch.object(
        report, '_transform_time_to_str', return_value='2025-04-17_01PM'
    )

    # Mock HEAD (sucesso)
    mock_head = mocker.patch('src.request_report.requests.head')
    mock_head.return_value.status_code = 200

    # Mock GET (retorna PDF fake)
    mock_get = mocker.patch('src.request_report.requests.get')
    mock_get.return_value.content = b'%PDF-FAKE'

    result = report.request_report()

    assert result == b'%PDF-FAKE'
    mock_head.assert_called_once()
    mock_get.assert_called_once()


def test_request_report_not_found(mocker):
    report = NBAInjuryReport()

    # Mock data
    mocker.patch.object(
        report, '_transform_time_to_str', return_value='2025-04-17_01PM'
    )

    # HEAD retorna 404
    mock_head = mocker.patch('src.request_report.requests.head')
    mock_head.return_value.status_code = 404

    result = report.request_report()

    assert result is None
    mock_head.assert_called_once()
