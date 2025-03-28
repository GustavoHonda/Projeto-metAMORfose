import pyautogui as pg
import webbrowser as web
import time
import pandas as pd
import random 

def exit_webpg():
    time.sleep(2)
    pg.keyDown('ctrl')
    pg.press('w')
    pg.keyUp('ctrl')

def send_msg(phone, message):
    web.open("https://web.whatsapp.com/send?phone="+phone+"&text="+message)
    time.sleep(5)
    pg.press("enter")
    exit_webpg()
    
def send_n_msg(phone, message):
    web.open("https://web.whatsapp.com") #Open url
    time.sleep(5)
    search_bar = pg.locateOnScreen('search_bar.png') #Search in printscreen for search_bar
    search_bar_x, search_bar_y = pg.center(search_bar) #Get coordinates
    pg.click(search_bar_x, search_bar_y)
    pg.write(phone) #Search phone number
    time.sleep(2)
    pg.click(search_bar_x, search_bar_y+300) #Select first match
    time.sleep(2)
    pg.write(message) #Write message
    pg.press("enter") #Send
    pg.click(search_bar_x + 250, search_bar_y) #Erase phone number from searchbar
    exit_webpg()
    
    


if __name__ == '__main__':
    phone = "11950440023"
    message = "Hello pyautogui!"
    send_msg(phone, message)
    # send_n_msg(phone, message)
