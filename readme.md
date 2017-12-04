# PYSSISTANT 

Fast way to run anything you want without mouse and eye focus.

Pyssistant is a simple tool designed for developers working on Windows OS. Main purpose is to provide fast way to run anything you want without mouse and eye focus. You can open known folders, device manager, network connections, paste any predefined text, address, url whatever. Everything with keyboard control and with minimum signs as possible. 

## Current version  0.1.0

This project is made for my own purpose and it works for me enough so I'm not tending to work on it much more. I've spended about 10h and I'm satisfied.

Pyssistant is designed to be easy extensible, If you know how to do it. Feel free

## How to use it

1. Clone repository
2. Run pyssistant or add pythonw.exe path_to_pyssistant to startup folder.
    1. Durring first start pyssitant creates home folder in AppData/local folder of your current user, and prepare basic command.db where any pyssistant commands are registered
    2. Press CTRL to show or hide PYSSISTANT.
    3. Enter any command full or partial name and press Enter or gravis sign ` tu run command. (In some cases you should run pyssistan as admin)
3. If you want to add new commands: add new to existing modules or write new module. Each module have 'pyssistant_commands' list with commands. Look at infrastructure.py as example. If you want to add new module add them also in _update_known_modules_ method in db_assistant.py. 
    1. Then restart application with 'restart' command (aka. x restart) and reload commands.db with 'x db update known' command (You can type 'db' and in basic cases it's enough. You don't need to remember whole name of command, this is why is so simple.)

### Prompter module

Prompter is designed to write any predefined text directly.  (It works very simple. It clicks mouse where it points and writes text.) . You can define any text, template, whatever by creating text file with '.prompter' extension. Content of file will be treated as text to type. Files should be placed in 'pyssistant home path'/modules/prompter/.