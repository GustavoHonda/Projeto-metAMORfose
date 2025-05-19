import pytest
from unittest.mock import patch, MagicMock
import builtins
from src import send_msg as send_msg
from pathlib import Path

@patch("src.send_msg.subprocess.run")
def test_enable_localhost_execution(mock_run):
    send_msg.enable_localhost_execution()
    mock_run.assert_called_once_with("xhost + local:", shell=True, executable="/bin/bash")


@patch("pyautogui.hotkey")
def test_exit_webpg(mock_hotkey):
    with pytest.raises(SystemExit):
        result = send_msg.exit_webpg()
        mock_hotkey.assert_called_once_with("ctrl", "w")


@patch("webbrowser.open")
@patch("pyautogui.press")
@patch("time.sleep")
def test_direct_msg(mock_sleep, mock_press, mock_open):
    send_msg.direct_msg("123456789", "Hello")
    mock_open.assert_called_once()
    mock_press.assert_called_with("enter")


@patch("webbrowser.get")
@patch("src.send_msg.enable_localhost_execution")
def test_open_page_success(mock_enable, mock_get):
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
def test_open_page_fail(mock_enable, mock_get):
    # Simula falha ao abrir o navegador
    mock_browser = mock_get.return_value
    mock_browser.open.return_value = False

    # Verifica se a exceção é levantada
    with pytest.raises(ConnectionError):
        send_msg.open_page()

    mock_enable.assert_called_once()
    mock_get.assert_called_once()



@patch("pyautogui.locateOnScreen", return_value=(100, 100, 50, 20))
@patch("pyautogui.center", return_value=(125, 110))
@patch("pathlib.Path.iterdir")
@patch("pathlib.Path.resolve")
def test_locate_search_bar(mock_resolve, mock_iterdir, mock_center, mock_locate):
    mock_resolve.return_value = Path("./tests/img")
    mock_iterdir.return_value = [Path("./tests/img/fake.png")]
    result = send_msg.locate_search_bar()
    assert result == (125, 110)


@patch("pyautogui.click")
@patch("pyautogui.write")
@patch("pyautogui.hotkey")
@patch("pyautogui.press")
@patch("time.sleep")
def test_send_msg(mock_sleep, mock_press, mock_hotkey, mock_write, mock_click):
    send_msg.send_msg("123456", ["linha 1", "linha 2"], (100, 100))
    assert mock_click.call_count == 1
    assert mock_write.call_count == 3  
    mock_hotkey.assert_called_with("shift", "enter")
    mock_press.assert_called_with("enter")


def test_text_message():
    result = send_msg.text_message("Gu Silva", "12345", "dor nas costas", "200")
    assert isinstance(result, tuple)
    assert "Gu Silva" in result[1]
