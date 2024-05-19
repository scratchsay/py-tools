import os
import webbrowser
import pyautogui
import keyboard
import time

class Notepad:

    def __init__(self, width=300, height=300):
        self.width = width
        self.height = height
        self.file = None

    def open_file(self):
        self.file = pyautogui.prompt(text='Enter file path:', title='Open File')
        if self.file:
            try:
                with open(self.file, 'r') as f:
                    content = f.read()
                    pyautogui.write(content)
            except FileNotFoundError:
                pyautogui.alert(text='File not found!', title='Error', button='OK')

    def new_file(self):
        self.file = None
        pyautogui.write('\n')

    def save_file(self):
        if self.file is None:
            self.file = pyautogui.prompt(text='Enter file name:', title='Save File', default='Untitled.txt')
        content = pyautogui.screenshot(region=(100, 100, 500, 300))
        content.save(self.file)

    def cut(self):
        keyboard.press_and_release('ctrl+x')

    def copy(self):
        keyboard.press_and_release('ctrl+c')

    def paste(self):
        keyboard.press_and_release('ctrl+v')

    def quit_application(self):
        pyautogui.alert(text='Exiting Notepad', title='Info', button='OK')
        exit()

    def show_about(self):
        webbrowser.open("https://www.bing.com/search?q=get+help+with+notepad+in+windows+10&filters=guid:%224466414-en-dia%22%20lang:%22en%22&form=T00032&ocid=HelpPane-BingIA")

    def run(self):
        while True:
            action = pyautogui.confirm(text='Choose action:', title='Notepad', buttons=['Open', 'New', 'Save', 'Cut', 'Copy', 'Paste', 'Quit', 'About'])
            if action == 'Open':
                self.open_file()
            elif action == 'New':
                self.new_file()
            elif action == 'Save':
                self.save_file()
            elif action == 'Cut':
                self.cut()
            elif action == 'Copy':
                self.copy()
            elif action == 'Paste':
                self.paste()
            elif action == 'Quit':
                self.quit_application()
            elif action == 'About':
                self.show_about()

notepad = Notepad()
notepad.run()
