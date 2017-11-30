
import subprocess
from subprocess import call
import knownpaths

class WinCtrl:

    def __init__(self):
        pass

    def open_device_manager(self):
        '''@command: open device manager
        '''
        call(["mmc", "devmgmt.msc"])
    
    def open_network_connections(self):
        '''@command: open network connections
        '''
        call(["control","ncpa.cpl"])

    def edit_environment_variables(self):
        '''@command: edit environment variables
        '''
        subprocess.Popen("rundll32 sysdm.cpl,EditEnvironmentVariables")

    def edit_timedate_settings(self):
        '''@command: edit timedate settings
        '''
        call(["control","timedate.cpl"])
    
    def open_folder(self, path):
        call(["explorer", path])
    
    def open_folder_downloads(self):
        '''@command: open folder downloads
        '''
        self.open_folder(knownpaths.get_path(
            knownpaths.FOLDERID.Downloads, user_handle=knownpaths.UserHandle.current))

    def run_cmd(self):
        '''@command: run cmd
        '''
        subprocess.Popen("cmd")



#import ctypes

#dll = ctypes.windll.shell32
#buf = ctypes.create_string_buffer(300)
#dll.SHGetSpecialFolderPathA(None, buf, 0x0005, False)
#path = dll.SHGetKnownFolderPath(shellcon.FOLDERID_AccountPictures,
  #                                0, # see KNOWN_FOLDER_FLAG
 #                                 0) # current user
#print(path)
#import os
#call(["rundll32","sysdm.cpl,EditEnvironmentVariables"])
#os.system("rundll32 sysdm.cpl,EditEnvironmentVariables")
#ncpa.cpl - network connections
#
#os.system("ncpa.cpl")