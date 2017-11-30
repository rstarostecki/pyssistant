from sqlite3 import dbapi2

class AssistantDataBase:

    def __init__(self):
        self.db_location = "commands.db"

    def reinit(self):
        con = dbapi2.connect(self.db_location)
        con.execute("DROP TABLE IF EXISTS commands")
        con.execute("CREATE TABLE commands (\
                id INTEGER PRIMARY KEY, \
                module_name TEXT,\
                class_name TEXT,\
                entry_name TEXT,\
                command_name TEXT UNIQUE,\
                active INTEGER)")
    
    def insert(self, data):
        module_name, class_name, entry_name, command_name = data
        con = dbapi2.connect(self.db_location)
        con.execute("INSERT INTO commands  (module_name, class_name, entry_name, command_name, active)\
         VALUES ('"+module_name+"', '"+class_name+"', '"+entry_name+"', '"+command_name+"', '1')")
        con.execute("COMMIT")
    
    def show_all(self):
        con = dbapi2.connect(self.db_location)
        res = con.execute("Select * from commands")
        for r in res:
            iden, module_name, class_name, entry_name, command_name, active = r
            print("{}\t{}\t{}\t{}\t{}\t{}".format(iden, module_name, class_name, entry_name, command_name, active))

    def get_modules(self):
        results = []
        con = dbapi2.connect(self.db_location)
        res = con.execute("Select module_name from commands  where active='1' group by module_name")
        for r in res:
            results.append(r[0])
        return results

    def get_classes(self):
        results = []
        con = dbapi2.connect(self.db_location)
        res = con.execute("Select module_name, class_name from commands  where active='1' group by class_name")
        for r in res:
            results.append(r)
        return results

    def lookup(self, command_name, limit):
        results = []
        con = dbapi2.connect(self.db_location) 
        res = con.execute('SELECT class_name, entry_name, command_name\
                            from commands where command_name like "%'+command_name+'%"\
                            ORDER BY command_name LIMIT '+str(limit)+'')
        for r in res:
            results.append(r)
        return results
        
#a = AssistantDataBase()
#a.reinit()
#a.insert(("wincontrol","WinCtrl","open_device_manager","open device manager"))
#a.insert(("wincontrol","WinCtrl","open_network_connections","open network connections"))
#a.insert(("wincontrol","WinCtrl","edit_environment_variables","edit environment variables"))
##a.insert(("wincontrol","WinCtrl","edit_timedate_settings","edit timedate settings"))
#AssistantDataBase().insert(("wincontrol","WinCtrl","open_folder_downloads","open folder downloads"))
#AssistantDataBase().insert(("wincontrol","WinCtrl","run_cmd","run cmd"))

#a = AssistantDataBase()
#a.reinit()
#a.insert(("testmodule","TestMod","metod1","open zone"))
#a.insert(("testmodule","TestMod","metod2","zoneter"))
#a.insert(("testmodule","classname","entry4","command32"))
#a.insert(("modname3","classname","entry5","command42"))
#a.show_all()
#a.get_modules()
#a.get_classes()

#print(a.lookup("2",5))
#print(a.lookup("4",5))
