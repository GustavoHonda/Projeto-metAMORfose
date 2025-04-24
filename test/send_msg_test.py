import pytest
from unittest.mock import patch, MagicMock
import builtins
from src import send_msg as bot
from pathlib import Path

@patch("subprocess.run")
def test_enable_localhost_execution(mock_run):
    bot.enable_localhost_execution()
    mock_run.assert_called_once_with("xhost + local:", shell=True, executable="/bin/bash")


@patch("time.sleep")
@patch("pyautogui.keyDown")
@patch("pyautogui.keyUp")
@patch("pyautogui.press")
def test_exit_webpg(mock_press, mock_keyup, mock_keydown, mock_sleep):
    result = bot.exit_webpg()
    mock_keydown.assert_called_once_with("ctrl")
    mock_press.assert_called_once_with("w")
    mock_keyup.assert_called_once_with("ctrl")
    assert result is None


@patch("webbrowser.open")
@patch("pyautogui.press")
@patch("time.sleep")
def test_direct_msg(mock_sleep, mock_press, mock_open):
    bot.direct_msg("123456789", "Hello")
    mock_open.assert_called_once()
    mock_press.assert_called_with("enter")


@patch("webbrowser.open", return_value=True)
@patch("src.send_msg.enable_localhost_execution")
def test_open_page_success(mock_enable, mock_open):
    result = bot.open_page()
    assert result is True
    mock_open.assert_called_once()
    mock_enable.assert_called_once()


@patch("webbrowser.open", return_value=False)
@patch("src.send_msg.enable_localhost_execution")
def test_open_page_fail(mock_enable, mock_open):
    with pytest.raises(ConnectionError):
        bot.open_page()


@patch("pyautogui.locateOnScreen", return_value=(100, 100, 50, 20))
@patch("pyautogui.center", return_value=(125, 110))
@patch("pathlib.Path.iterdir")
@patch("pathlib.Path.resolve")
def test_locate_search_bar(mock_resolve, mock_iterdir, mock_center, mock_locate):
    mock_resolve.return_value = Path("./tests/img")
    mock_iterdir.return_value = [Path("./tests/img/fake.png")]
    result = bot.locate_serch_bar()
    assert result == (125, 110)


@patch("pyautogui.click")
@patch("pyautogui.write")
@patch("pyautogui.hotkey")
@patch("pyautogui.press")
@patch("time.sleep")
def test_send_msg(mock_sleep, mock_press, mock_hotkey, mock_write, mock_click):
    bot.send_msg("123456", ["linha 1", "linha 2"], (100, 100))
    assert mock_click.call_count == 2
    assert mock_write.call_count == 3  # phone + 2 lines
    mock_hotkey.assert_called_with("shift", "enter")
    mock_press.assert_called_with("enter")


def test_text_message():
    result = bot.text_message("Gu Silva", "12345", "dor nas costas", "200")
    assert isinstance(result, tuple)
    assert "Gu Silva" in result[1]
