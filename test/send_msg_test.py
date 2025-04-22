import pytest
import subprocess
import builtins
from unittest.mock import patch, MagicMock
from src import send_msg as bot  # Supondo que seu arquivo original se chama whatsapp_bot.py

def test_enable_localhost_execution(monkeypatch):
    mock_run = MagicMock()
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    bot.enable_localhost_execution()
    mock_run.assert_called_once_with("xhost + local:", shell=True, executable="/bin/bash")

def test_exit_webpg(monkeypatch):
    pg_mock = MagicMock()
    monkeypatch.setattr(bot, "pg", pg_mock)

    result = bot.exit_webpg()
    assert result is None or result == -1  # Retorna -1 apenas se RuntimeError (mockado aqui não acontece)

def test_direct_msg(monkeypatch):
    mock_open = MagicMock()
    mock_press = MagicMock()
    monkeypatch.setattr(bot.web, "open", mock_open)
    monkeypatch.setattr(bot.pg, "press", mock_press)

    bot.direct_msg("123456", "mensagem")
    mock_open.assert_called_once()
    mock_press.assert_called_with("enter")

def test_open_page_success(monkeypatch):
    mock_open = MagicMock(return_value=True)
    monkeypatch.setattr(bot.web, "open", mock_open)

    response = bot.open_page()
    assert response is True

def test_open_page_fail(monkeypatch):
    mock_open = MagicMock(return_value=False)
    monkeypatch.setattr(bot.web, "open", mock_open)

    with pytest.raises(ConnectionError):
        bot.open_page()
