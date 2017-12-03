

from tkinter import *
import threading
from importlib import import_module
from pynput import keyboard
from pynput.mouse import Button, Controller
from db_assistant import AssistantDataBase
from infrastructure import Infrastructure

def click(position):
    mouse = Controller()
    lastpos = mouse.position
    mouse.position = position
    mouse.click(Button.left, 1)
    mouse.position = lastpos

class AssistantGUI:
    
    def __init__(self):
        self.root = Tk()
        self.text = Text(self.root, height=12, width=32)
        self.text.pack()
        self.root.attributes("-topmost", True)
        self.empty_title = ""

    def is_focused(self):
        return self.root.focus_displayof() != None

    def show(self):
        self.root.deiconify()
        click((self.root.winfo_x(), self.root.winfo_y()))
    
    def hide(self):
        self.root.withdraw()

    def set_empty_title(self, empty_title):
        self.empty_title = empty_title

    def update_head(self, head):
        if head != "": 
            self.root.title(head)
        else:
            self.root.title(self.empty_title)

    def update_text(self, text):
        self.text.delete('1.0', END)
        self.text.insert(END, text)
    
class Executor:

    def __init__(self):
        self.modules = {}
        self.objects = {}
        self.commands = []
        self.position = 0
        self.command_name = ""
        self.root = None
        self.command_listener = None
        self.content_listener = None
        self.last_command = ""
        self.db = AssistantDataBase()
    
    def start(self):
        modules_list = self.db.get_modules()
        for module_name in modules_list:
            try:
                self.modules[module_name] = import_module(module_name)
            except:
                print("module_name="+module_name+" failed")
        
        classes = self.db.get_classes()
        for module_name, class_name in classes:
            try:
                self.objects[class_name] = getattr(self.modules[module_name], class_name)()
            except:
                print("class_name="+class_name+" failed")

    def get_commands(self):
        return (self.position, self.commands)

    def append_char(self, newchar):
        self.command_name += newchar
        self._update()

    def remove_char(self):
        self.command_name = self.command_name[:-1]
        self._update()
    
    def reset(self):
        self.last_command = None
        self.command_name = ""
        self.position = 0
        self._update()

    def run(self):
        if len(self.commands) > self.position:
            class_name, entry_name, command_name = self.commands[self.position]
            try:
                getattr(self.objects[class_name], entry_name)()
                self.reset()
                return True
            except:
                print("Command: "+command_name+" failed")
                return False

    def move_up(self):
        if self.position > 0 : 
            self.position -= 1
            self._update()

    def move_down(self):
        if self.position < len(self.commands) -1 :
            self.position += 1
            self._update()
    
    def set_content_listener(self, new_listener):
        self.content_listener = new_listener

    def set_command_listener(self, new_listener):
        self.command_listener = new_listener

    def _update(self):
        if self.last_command != self.command_name:
            cmds = self.db.lookup(self.command_name, 16)
            self.commands.clear()
            for cmd in cmds:
                self.commands.append(cmd)
            self.position = 0
            self.last_command = self.command_name

        if self.content_listener != None:
            self.content_listener(self.get_commands())
        if self.command_listener != None:
            self.command_listener(self.command_name)
     

class Assistant:

    def __init__(self):
        if not Infrastructure().db_file_exists():
            Infrastructure().build_path()
            self.build_default_db()

        self.gui = AssistantGUI()
        self.gui.set_empty_title("[enter command]")
        self.gui.hide()
        self.executor = Executor()
        self.executor.set_content_listener(self.content_changed)
        self.executor.set_command_listener(self.command_changed)
        self.executor.start()
        self.mainTread = threading.Thread(target=self.worker)
        self.visible = False
        self.lastKeyPressed = keyboard.Key.ctrl_l
        self.updateContent(self.executor.get_commands())

    def build_default_db(self):
        db = AssistantDataBase()
        db.reinit()
        db.update_known_modules()

    def content_changed(self, data):
        self.updateContent(data)
    
    def command_changed(self, data):
        self.gui.update_head(data)

    def start(self):
        self.mainTread.start()
        mainloop()
        self.listenerThread.stop()

    def worker(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            self.listenerThread = listener
            self.listenerThread.join()

    def on_press(self, key):
        try:
            self.lastKeyPressed = key
            if self.visible and self.gui.is_focused():
                if key == keyboard.Key.space:
                    self.executor.append_char(" ")
                elif key == keyboard.Key.backspace:
                    self.executor.remove_char()
                elif hasattr(key,"char") and key.char.isalnum() :
                    self.executor.append_char(key.char)
                if key == keyboard.Key.enter:
                    if self.executor.run() == True:
                        self.gui.hide()
                        self.visible = False
                elif key == keyboard.Key.up:
                    self.executor.move_up()
                elif key == keyboard.Key.down:
                    self.executor.move_down()
        except AttributeError:
            print("AttributeError")

    def on_release(self, key):
        if key == keyboard.Key.ctrl_l and self.lastKeyPressed == key:
            self.activationTrigger()

    def activationTrigger(self):
        if self.visible:
            self.gui.hide()
            self.visible = False
        else:
            self.gui.show()
            self.visible = True
            self.executor.reset()
    
    def updateContent(self, data):     
        pos, cmds = data
        text = ""
        i = 0
        for c in cmds: 
            a, b , name = c
            if pos == i:
                text +=" * "+name+"\n"
            else:
                text +="   "+name+"\n"
            i+=1
        self.gui.update_text(text)
