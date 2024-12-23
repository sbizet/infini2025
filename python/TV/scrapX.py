import pyautogui as gui, time
import os
import sys
import pyperclip
from bs4 import BeautifulSoup
import threading

class FuckX:
    def __init__(self):
        gui.FAILSAFE = False
        self.tweets = []

    def majThread(self):
        threadTweet = threading.Thread(target=self.maj)
        threadTweet.start()

    def maj(self):
        os.system('start chrome')
        time.sleep(0.5)
        """gui.keyDown('alt')
        time.sleep(0.2)
        gui.press(' ')
        gui.press('n')
        gui.keyUp('alt')
        time.sleep(0.5)"""
        gui.keyDown('ctrl')
        gui.press('k')
        time.sleep(0.2)
        gui.keyUp('ctrl')
        time.sleep(0.2)
        gui.press('backspace')
        time.sleep(0.2)
        pyperclip.copy('https://x.com/messages')
        gui.hotkey('ctrl', 'v')
        pyperclip.copy('')
        gui.press('enter')
        time.sleep(3)
        gui.hotkey('ctrl', 'shift', 'i')
        time.sleep(3)
        gui.hotkey('f2')
        time.sleep(0.2)
        gui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        gui.hotkey('ctrl', 'c')
        text = pyperclip.paste()

        soup = BeautifulSoup(text, 'html.parser')

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        lignes = soup.find_all(['div', 'span'], attrs={'data-testid': "tweetText"})

        self.tweets = []
        for l in lignes :
            l2 = l.get_text(separator='\n')
            self.tweets.append(l2.split('\n')[0])
        gui.hotkey('ctrl', 'w')
        print("maj des tweets effectuée")

    def getDernierTweet(self):
        if(len(self.tweets)>0) : return self.tweets[0]
        else : return ""

if __name__ == '__main__':
    twitter = FuckX()
    twitter.maj()
    print(twitter.tweets[0]) # affiche le dernier tweet
