import pytest
from unittest.mock import patch, MagicMock
from src import send_msg as send_msg
from pathlib import Path
import pandas as pd

@patch("src.send_msg.subprocess.run")
def test_enable_localhost_execution(mock_run)-> None:
    send_msg.enable_localhost_execution()
    mock_run.assert_called_once_with("xhost + local:", shell=True, executable="/bin/bash")


@patch("pyautogui.hotkey")
def test_exit_webpg(mock_hotkey)-> None:
    with pytest.raises(SystemExit):
        result = send_msg.exit_webpg()
        mock_hotkey.assert_called_once_with("ctrl", "w")


@patch("webbrowser.get")
@patch("src.send_msg.enable_localhost_execution")
def test_open_page_success(mock_enable, mock_get)-> None:
    # Simula o retorno do método `open()` do controlador
    mock_browser = mock_get.return_value
    mock_browser.open.return_value = True

    # Chama a função
    result = send_msg.open_page()

    # Verifica se a função retornou True
    assert result is True
    mock_enable.assert_called_once()
    mock_get.assert_called_once()


@patch("webbrowser.get")
@patch("src.send_msg.enable_localhost_execution")
def test_open_page_fallback(mock_enable, mock_get) -> None:
    # Simula que o primeiro não deu certo
    mock_web = MagicMock()
    mock_web.open.return_value = False

    # Simula que o chrome também deu errado
    mock_chrome = MagicMock()
    mock_chrome.open.return_value = False

    # Agora o firefox deu certo
    mock_firefox = MagicMock()
    mock_firefox.open.return_value = True

    # Mock da sequência de chamados:
    mock_get.side_effect = [mock_chrome, mock_firefox]

    response = send_msg.open_page()

    assert response == mock_firefox.open.return_value
    mock_enable.assert_called_once()
    assert mock_get.call_count == 2


@patch("pyautogui.locateOnScreen", return_value=(100, 100, 50, 20))
@patch("pyautogui.center", return_value=(125, 110))
@patch("pathlib.Path.iterdir")
@patch("pathlib.Path.resolve")
def test_locate_search_bar(mock_resolve, mock_iterdir, mock_center, mock_locate)-> None:
    mock_resolve.return_value = Path("./tests/img")
    mock_iterdir.return_value = [Path("./tests/img/fake.png")]
    result = send_msg.locate_search_bar()
    assert result == (125, 110)


@patch("pyautogui.click")
@patch("pyautogui.write")
@patch("pyautogui.hotkey")
@patch("pyautogui.press")
@patch("time.sleep")
def test_send_msg(mock_sleep, mock_press, mock_hotkey, mock_write, mock_click)-> None:
    send_msg.send_msg("123456", ["linha 1", "linha 2"], (100, 100), (500, 500))
    assert mock_click.call_count == 1
    assert mock_write.call_count >= 14 # Assuming random errors
    mock_hotkey.assert_called_with("shift", "enter")
    mock_press.assert_called_with("enter")


def test_text_message()-> None:
    df = pd.DataFrame([{"name_paciente":"Gustavo Akio Honda3","name_professional":"Gustavo Akio Honda4","description":"description1", "phone_paciente":"11950440023","phone_professional":"11950440023","area":"psicologia","datetime":"31/08/2024 21:33:09","price_min":"35","price_max":"150"}])
    result = send_msg.text_message(df)
    assert isinstance(result, tuple)
    assert type(result) is tuple