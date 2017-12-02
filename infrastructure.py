import pathlib
import knownpaths
import os
import sys

pyssistant_commands = [ ("Infrastructure","restart","x restart"),
                        ("Infrastructure","build_path","x build path")]

class Infrastructure:
    class __Infrastructure:
        def __init__(self):
            pass
    instance = None
    def __init__(self):
        if Infrastructure.instance == None:
            Infrastructure.instance = Infrastructure.__Infrastructure()
            Infrastructure.instance.PROGRAMS_PATH = knownpaths.get_path(
                knownpaths.FOLDERID.LocalAppData, user_handle=knownpaths.UserHandle.current) +"/Programs"
            Infrastructure.instance.ROOT_PATH = Infrastructure.instance.PROGRAMS_PATH+"/Pyssistant"
            Infrastructure.instance.DB_PATH = Infrastructure.instance.ROOT_PATH+"/commands.db"
            Infrastructure.instance.MODULES_DATA_PATH = Infrastructure.instance.ROOT_PATH+"/modules_data"

    def build_path(self):
        pathlib.Path(Infrastructure.instance.ROOT_PATH).mkdir(parents=True, exist_ok=True)
        pathlib.Path(Infrastructure.instance.MODULES_DATA_PATH).mkdir(parents=True, exist_ok=True)
    
    def get_db_path(self):
        return Infrastructure.instance.DB_PATH

    def set_db_path(self, path):
        Infrastructure.instance.DB_PATH = path

    def get_module_data_path(self, module_name):
        path = Infrastructure.instance.MODULES_DATA_PATH+"/"+module_name
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def db_file_exists(self):
        return pathlib.Path(Infrastructure.instance.DB_PATH).is_file()

    def restart(self):
        os.execv(sys.executable, ['python'] + sys.argv)