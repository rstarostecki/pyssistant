from sqlite3 import dbapi2
from infrastructure import Infrastructure

from importlib import import_module


pyssistant_commands = [ ("AssistantDataBase","update_known_modules","x db update known")]


class AssistantDataBase:

    def __init__(self):
        pass

    def reinit(self):
        con = dbapi2.connect(Infrastructure().get_db_path())
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
        con = dbapi2.connect(Infrastructure().get_db_path())
        con.execute("INSERT INTO commands  (module_name, class_name, entry_name, command_name, active)\
         VALUES ('"+module_name+"', '"+class_name+"', '"+entry_name+"', '"+command_name+"', '1')")
        con.execute("COMMIT")
    
    def delete_module(self, module_name):
        con = dbapi2.connect(Infrastructure().get_db_path())
        con.execute("DELETE FROM commands WHERE module_name='"+module_name+"'")
        con.execute("COMMIT")
    
    def update_module(self, module_name):
        try:
            mod = import_module(module_name)
            if mod:
                self.delete_module(module_name)
            definition = getattr(mod,"pyssistant_commands")
            for cmd in definition :
                class_name, entry_name, command_name = cmd
                self.insert((module_name, class_name, entry_name, command_name))
        except:
            print(module_name+ " Failed")
            return False
    
    def show_all(self):
        con = dbapi2.connect(Infrastructure().get_db_path())
        res = con.execute("Select * from commands")
        for r in res:
            iden, module_name, class_name, entry_name, command_name, active = r
            print("{}\t{}\t{}\t{}\t{}\t{}".format(iden, module_name, class_name, entry_name, command_name, active))

    def get_modules(self):
        results = []
        con = dbapi2.connect(Infrastructure().get_db_path())
        res = con.execute("Select module_name from commands  where active='1' group by module_name")
        for r in res:
            results.append(r[0])
        return results

    def get_classes(self):
        results = []
        con = dbapi2.connect(Infrastructure().get_db_path())
        res = con.execute("Select module_name, class_name from commands  where active='1' group by class_name")
        for r in res:
            results.append(r)
        return results

    def lookup(self, command_name, limit):
        results = []
        con = dbapi2.connect(Infrastructure().get_db_path()) 
        phrases = command_name.split()
        if len(phrases) == 1:
            res = con.execute('SELECT class_name, entry_name, command_name\
                        from commands where command_name like "%'+phrases[0]+'%"\
                        ORDER BY command_name LIMIT '+str(limit)+'')
        elif len(phrases) == 2:
            res = con.execute('SELECT class_name, entry_name, command_name\
                        from commands where command_name like "%'+phrases[0]+'%" and command_name like "%'+phrases[1]+'%"\
                        ORDER BY command_name LIMIT '+str(limit)+'')
        elif len(phrases) > 2:
            res = con.execute('SELECT class_name, entry_name, command_name\
                        from commands where command_name like "%'+phrases[0]+'%"\
                            and command_name like "%'+phrases[1]+'%"\
                            and command_name like "%'+phrases[2]+'%"\
                        ORDER BY command_name LIMIT '+str(limit)+'')
        else:
            res = con.execute('SELECT class_name, entry_name, command_name\
                        from commands\
                        ORDER BY command_name LIMIT '+str(limit)+'')

        for r in res:
            results.append(r)

        return results 

    def update_known_modules(self):
        self.update_module("db_assistant")
        self.update_module("wincontrol")
        self.update_module("infrastructure")
        