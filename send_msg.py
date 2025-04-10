import pyautogui as pg
import webbrowser as web
import time
from get_data import open_profissional, open_respostas

# xhost + local:

def exit_webpg():
    time.sleep(2)
    pg.keyDown('ctrl')
    pg.press('w')
    pg.keyUp('ctrl')

def direct_msg(phone, message):
    web.open("https://web.whatsapp.com/send?phone="+phone+"&text="+message)
    time.sleep(5)
    pg.press("enter")
    
def send_msg(phone, message):
    web.open("https://web.whatsapp.com") #Open url
    time.sleep(10)
    search_bar = pg.locateOnScreen('search_bar.png') #Search in printscreen for search_bar
    search_bar_x, search_bar_y = pg.center(search_bar) #Get coordinates
    pg.click(search_bar_x, search_bar_y)
    pg.write(phone) #Search phone number
    pg.press('enter') #Select first match
    time.sleep(1)
    pg.write(message) #Write message
    pg.press("enter") #Send
    pg.click(search_bar_x + 250, search_bar_y) #Erase phone number from searchbar


if __name__ == '__main__':
    df_respostas = open_respostas()
    df_profissional = open_profissional()
    
    print(df_profissional)
    
    # phone = "558585410805"
    # message = "Hello pyautogui!"
    # # direct_msg(phone, message)
    # send_msg(phone, message)
    # time.sleep(3)
    # exit_webpg()