
import mouse
from infrastructure import Infrastructure
import pathlib
import keyboard

prompter_universal_entry = "prompter_entry"

class PrompterLoader():

    def __init__(self):
        self.db_loc = Infrastructure().get_module_data_path("prompter")

    def load_pyssistant_commands(self):
        cmds = []
        for prompter_file in pathlib.Path(self.db_loc).iterdir():
            if prompter_file.is_file() and prompter_file.match("*.prompter"):
                cmds.append(("Prompter", prompter_universal_entry, "prompter "+prompter_file.name.split('.')[0]))
        return cmds

    
    def get_content(self, path):
        with open(path, 'r') as myfile:
            data=myfile.read()
        return data

    def load_prompter_definition(self):
        defs = {}
        for prompter_file in pathlib.Path(self.db_loc).iterdir():
            if prompter_file.is_file() and prompter_file.match("*.prompter"):
                defs["prompter "+prompter_file.name.split('.')[0]] = self.get_content(str(prompter_file))
        return defs

pyssistant_commands = PrompterLoader().load_pyssistant_commands()

class Prompter:

    def __init__(self):
        self.command = ""
        self.defs = PrompterLoader().load_prompter_definition()
    
    def set_command(self, command):
        self.command = command

    def prompter_entry(self):
        try:
            self.prompter(self.defs[self.command])
        except:
            print("Prompter for "+self.command+" failed")
        pass

    def prompter(self, text):
        mouse.click()
        if "\n" in text :
            keyboard.write(text)
        else :
            keyboard.write(text, exact=True)