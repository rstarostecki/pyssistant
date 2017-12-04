
import subprocess
from subprocess import call
import knownpaths
import sys
import pathlib
from infrastructure import Infrastructure

pyssistant_commands = [ ("WinCtrl","open_device_manager","open device manager"),
                        ("WinCtrl","open_network_connections","open network connections"), 
                        ("WinCtrl","edit_environment_variables","edit environment variables"),
                        ("WinCtrl","edit_timedate_settings","edit timedate settings"),
                        ("WinCtrl","open_folder_downloads","open folder downloads"),
                        ("WinCtrl","open_folder_appdata","open folder appdata"),
                        ("WinCtrl","open_folder_python","open folder python"),
                        ("WinCtrl","open_folder_python_sites","open folder python sites"),
                        ("WinCtrl","open_pyssistant_home","open folder pyssistant"),
                        ("WinCtrl","run_cmd","run cmd")]


class WinCtrl:

    def __init__(self):
        pass

    def open_device_manager(self):
        subprocess.Popen("mmc devmgmt.msc")
    
    def open_network_connections(self):
        call(["control","ncpa.cpl"])

    def edit_environment_variables(self):
        subprocess.Popen("rundll32 sysdm.cpl,EditEnvironmentVariables")

    def edit_timedate_settings(self):
        call(["control","timedate.cpl"])
    
    def open_folder(self, path):
        call(["explorer", path])
    
    def open_folder_downloads(self):
        self.open_folder(knownpaths.get_path(
            knownpaths.FOLDERID.Downloads, user_handle=knownpaths.UserHandle.current))

    def open_folder_appdata(self):
        self.open_folder(knownpaths.get_path(
            knownpaths.FOLDERID.LocalAppData, user_handle=knownpaths.UserHandle.current))

    def open_folder_python(self):
        self.open_folder(str(pathlib.Path(sys.executable).parent))

    def open_folder_python_sites(self):
        self.open_folder(str(pathlib.Path(sys.executable).parent)+"\\Lib\\site-packages")

    def open_pyssistant_home(self):
        self.open_folder(Infrastructure().get_root_path())

    def run_cmd(self):
        subprocess.Popen("cmd")
