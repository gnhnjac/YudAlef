# external - history, 
from http.client import TOO_MANY_REQUESTS
from os import listdir
from os.path import isfile, join, isdir, dirname, abspath
import os
import shutil
import subprocess
import sys
import re

def filter_empty_strings(lst):
    return list(filter(lambda x: x != "", lst))

STDOUT = sys.stdout

class Frame:

    def __init__(self):
        with open("env_vars.txt", "r") as f:
            self.env_vars = f.read().split("\n")
        
        self.redirect_file = ""
        self.command_history = []
        self.current_directory = abspath(self.get_environment_variable("HOME"))
        if self.current_directory == "":
            self.current_directory = "C:\\"

    def check_for_exe_redirect_wrapper(self, name, args):
        
        file_to_run = self.check_for_exe_in_path_and_return_it(name)

        if "|" in args:
            ps1 = file_to_run
            args1 = args[:args.index("|")]
            ps2 = args[args.index("|")+1:]
            args2 = ps2[1:]
            ps2 = ps2[0]
            ps2 = self.check_for_exe_in_path_and_return_it(ps2)

            if ps2 == 0:
                print(f"Command {ps2} not found.")
                return 0
            if ps1 == 0:
                print(f"Command {ps1} not found.")
                return 0
            
            prefix1 = "python " if ps1[-3:] == ".py" else ""
            ps1 = subprocess.Popen((prefix1 + ps1 + " " + " ".join(args1)), stdout=subprocess.PIPE)

            prefix2 = "python " if ps2[-3:] == ".py" else ""

            ps2 = subprocess.call((prefix2 + ps2 + " " + " ".join(args2)), stdin=ps1.stdout)
            ps1.wait()

            return 1

            

        if file_to_run == 0:
            if self.redirect_file != "":
                self.redirect_file = ""
                sys.stdout = STDOUT
            return 0

        if self.redirect_file != "":
            with open(self.redirect_file, "w") as f:
                if name[-4:] == ".exe":
                    subprocess.run([file_to_run] + args, stdout=f)
                    return 1
                elif name[-3:] == ".py":
                    subprocess.run(["python",file_to_run] + args, stdout=f)
                    return 1
        else:
            if name[-4:] == ".exe":
                subprocess.run([file_to_run] + args)
                return 1
            elif name[-3:] == ".py":
                subprocess.run(["python",file_to_run] + args)
                return 1
        
        if self.redirect_file != "":
            self.redirect_file = ""
            sys.stdout = STDOUT
        
        return 1


    def check_for_exe_in_path_and_return_it(self, name):

        path = self.get_environment_variable("PATH")

        if len(filter_empty_strings(name.replace("/","\\").split("\\"))) > 1:
            if isfile(name):
                res = Frame.check_for_exe_in_dir_and_return_it(name, join(self.current_directory, name))
                if res != 0:
                    return res
                else:
                    return 0
            else:
                return 0

        res = Frame.check_for_exe_in_dir_and_return_it(name, self.current_directory)
        if res != 0:
            return res

        for subpath in path.split(";"):
            if subpath == '':
                continue
            res = Frame.check_for_exe_in_dir_and_return_it(name, subpath)
            if res != 0:
                return res

        return 0
    
    @staticmethod
    def check_for_exe_in_dir_and_return_it(name, direc):
        for fil in [f for f in listdir(direc) if isfile(join(direc, f))]:
            res = Frame.check_for_exe_and_return_it(name, join(direc, fil))
            if res != 0:
                return res
        return 0
    
    @staticmethod
    def check_for_exe_and_return_it(wantedname, name):
        if name.split("\\")[-1:][0] == wantedname:
            if name[-4:] == ".exe" or name[-3:] == ".py":
                return name
        return 0

    
    def get_environment_variable(self, name):
        for var in self.env_vars:
            if var.split("=")[0] == name:
                return var[len(name)+1:]
        return 0
    
    def set_environment_variable(self, name, value):

        if self.get_environment_variable(name) != 0:
            for i in range(len(self.env_vars)):
                if self.env_vars[i].split("=")[0] == name:
                    self.env_vars[i] = self.env_vars[i][:len(name)+1] + value
        else:
            self.env_vars.append(f"{name}={value}")
        
        with open("env_vars.txt", "w") as f:
            f.write("\n".join(self.env_vars))
        return 1
    
    def remove_environment_variable(self, var):

        for i in range(len(self.env_vars)):
            if self.env_vars[i].split("=")[0] == var:
                del self.env_vars[i]
                break
    
        with open("env_vars.txt", "w") as f:
            f.write("\n".join(self.env_vars))
        return 1

    def dir(self, args):
        """
        dir - list directory contents

        Usage: dir [OPTIONS] [FILE]

        [FILE]:
        Can be left empty to view current directory contents.
        Can use absolute path or relative path.

        [OPTIONS]:
        -d Display only directories
        -f Display only files
        """
        
        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, ["f","d"])

        if not isvalid:
            print(cause)
            return 0

        directory = self.current_directory
        if len(reg) == 1:
            if ".." in reg[0]:
                reg[0] = reg[0].replace("..", dirname(self.current_directory))
            if isdir(reg[0]):
                directory = reg[0]
            elif isdir(join(self.current_directory, reg[0])):
                directory = join(self.current_directory, reg[0])
            else:
                print(f"Cannot find directory {reg[0]}")
                return 0


        if "f" in opt and "d" in opt or opt == []:
            files = [f for f in listdir(directory)]
        elif "f" in opt:
            files = [f for f in listdir(directory) if isfile(join(directory, f))]
        elif "d" in opt:
            files = [f for f in listdir(directory) if isdir(join(directory, f))]
        
        for f in files:
            prefix = "<DIR> " if isdir(join(directory, f)) else ""
            print(prefix + f)
        
        return 1
    
    def cd(self, args):
        """
        cd - change the working directory

        Usage: cd [FILE]

        [FILE]:
        Can be left empty to show current working directory
        Can use absolute path or relative path.
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, [])

        if not isvalid:
            print(cause)
            return 0
        
        if len(reg) == 0:
            print(self.current_directory)
            return 1
        elif len(reg) == 1:
            if ".." in reg[0]:
                reg[0] = reg[0].replace("..", dirname(self.current_directory))
            if isdir(reg[0]):
                self.current_directory = abspath(reg[0])
                return 1
            elif isdir(join(self.current_directory, reg[0])):
                self.current_directory = abspath(join(self.current_directory, reg[0]))
                return 1
            else:
                print(f"Directory {reg[0]} doesn't exist.")
                return 0
    
    def help(self, args):
        """
        help - get help for a certain command

        Usage: help [COMMAND]
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, [])

        if not isvalid:
            print(cause)
            return 0
        
        if len(reg) == 0:
            print("Must supply a command.")
            return 0
        
        if self.check_command_validity(reg[0]):
            print(getattr(self, reg[0]).__doc__)
            return 1
    
    def exit(self, args):
        """
        exit - exit the shell

        Usage: exit
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 0, [])

        if not isvalid:
            print(cause)
            return 0

        sys.exit(0)
    
    def set(self, args):
        """
        set - set an environment variable

        Usage: set [VAR]=[VALUE]
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, [])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) == 0:
            print("Must supply variable.")
            return 0

        var = reg[0].split("=")
        value = "".join(var[1:])
        var = var[0]

        self.set_environment_variable(var, value)

        return 1
    
    def echo(self, args):
        """
        echo - echo string back to the shell

        Usage: echo [STRING]
        """

        print("".join(args))

        return 1
    
    def rmenv(self, args):
        """
        rmenv - remove an environment variable

        Usage: rm [VAR]
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, [])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) == 0:
            print("Must supply variable.")
            return 0

        if reg[0] == "PATH":
            print("Permission denied.")
            return 0

        self.remove_environment_variable(reg[0])

        return 1
    
    def type(self, args):
        """
        type - print the contents of a non binary file

        Usage: type [OPTIONS] [PATH]

        [OPTIONS]:
        -L Display line numbers

        [PATH]:
        Can be relative or absolute.
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, ["L"])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) == 0:
            print("Must supply filename.")
            return 0

        path = ""

        if isfile(reg[0]):
            path = reg[0]
        elif isfile(join(self.current_directory, reg[0])):
            path = join(self.current_directory, reg[0])
        else:
            print(f"File {reg[0]} not found.")
            return 0
        try:
            with open(path, "r") as f:
                lines = f.readlines()
                for line_num, line in zip(range(len(lines)),lines):
                    prefix = str(line_num) + " " if "L" in opt else ""
                    print(prefix + line, end="")
            return 1
            
        except UnicodeDecodeError:
            print("Tried to read binary file.")
            return 0
        
    def clear(self, args):
        """
        clear - clears the console

        Usage: clear
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 0, [])

        if not isvalid:
            print(cause)
            return 0

        os.system('cls')

        return 1

    def mv(self, args):
        """
        mv - move file/directory to another location

        Usage: mv [ORIGIN FILE/DIRECTORY] [DESTINATION FILE/DIRECTORY]

        Notes: 
        Can rename file in destination.
        Paths can be relative/absolute paths.
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 2, [])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) < 2:
            print("Must supply origin and destination.")
            return 0

        origin = reg[0]
        destination = reg[1]

        if isdir(join(self.current_directory, origin)) or isfile(join(self.current_directory, origin)):
            origin = join(self.current_directory, origin)
        if not isdir(destination) or not isfile(dirname(destination)):
            destination = join(self.current_directory, destination)

        if not isfile(origin) and not isdir(origin):
            print(f"Origin {origin} not found.")
            return 0
        
        if (isfile(origin) and not isdir(dirname(destination))) or (isdir(origin) and not isdir(destination)):
            print("Destination directory doesn't exist.")
        
        shutil.move(origin, destination)

        return 1
    
    def cp(self, args):
        """
        cp - copy file/directory to another location

        Usage: cp [ORIGIN FILE/DIRECTORY] [DESTINATION FILE/DIRECTORY]

        Notes: Paths can be relative or absolute paths.
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 2, [])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) < 2:
            print("Must supply origin and destination.")
            return 0

        origin = reg[0]
        destination = reg[1]

        if isdir(join(self.current_directory, origin)) or isfile(join(self.current_directory, origin)):
            origin = join(self.current_directory, origin)
        if not isdir(destination) or not isfile(dirname(destination)):
            destination = join(self.current_directory, destination)

        if not isfile(origin) and not isdir(origin):
            print(f"Origin {origin} not found.")
            return 0

        if (isfile(origin) and not isdir(dirname(destination))) or (isdir(origin) and not isdir(destination)):
            print("Destination directory doesn't exist.")

        if isdir(origin):
            shutil.copytree(origin, destination)
        elif isfile(origin):
            shutil.copy(origin, destination)

        return 1 

    def rm(self, args):
        """
        rm - removes a file/directory

        Usage: rm [FILE/DIRECTORY]

        [FILE/DIRECTORY]:
        Can be relative or absolute path
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, [])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) < 1:
            print("Must supply filename.")
            return 0

        if len(filter_empty_strings(reg[0].replace("/","\\").split("\\"))) == 1:
            reg[0] = join(self.current_directory, reg[0])

        if not isfile(reg[0]) and not isdir(reg[0]):
            print(f"File {reg[0]} not found.")
            return 0

        if isdir(join(self.current_directory, reg[0])) or isfile(join(self.current_directory, reg[0])):
            reg[0] = join(self.current_directory, reg[0])

        if isdir(reg[0]):
            shutil.rmtree(reg[0])
        elif isfile(reg[0]):
            os.remove(reg[0])

        return 1 
    
    def mkdir(self, args):

        """
        mkdir - creates a new directory

        Usage: mkdir [DIRECTORY]

        [DIRECTORY]:
        Can be relative or absolute path.
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, [])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) < 1:
            print("Must supply directory path.")
            return 0

        if len(filter_empty_strings(reg[0].replace("/","\\").split("\\"))) > 1:
            print("Can only create 1 directory at once. Please don't nest them.")
            return 0

        if not isdir(dirname(reg[0])):
            reg[0] = join(self.current_directory, reg[0])

        os.mkdir(reg[0])

        return 1
    
    def touch(self, args):
        """
        touch - creates a new file

        Usage: touch [FILENAME]

        [FILENAME]:
        Path can be relative or absolute.
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, [])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) < 1:
            print("Must supply filename.")
            return 0
        if isdir(dirname(join(self.current_directory, reg[0]))):
            reg[0] = join(self.current_directory, reg[0])
        elif not isdir(dirname(reg[0])):
            print("File path doesn't exist.")

        with open(reg[0], 'w') as f:
            pass

        return 1
    
    def exec(self, args):

        """
        exec - executes a bat file

        Usage: exec [FILENAME]

        [FILENAME]:
        Path can be relative or absolute.
        """

        reg, opt = Frame.parse_args(args)

        isvalid, cause = Frame.check_argument_validity(reg, opt, 1, [])

        if not isvalid:
            print(cause)
            return 0

        if len(reg) < 1:
            print("Must supply filename.")
            return 0

        path = ""

        if isfile(reg[0]):
            path = reg[0]
        elif isfile(join(self.current_directory, reg[0])):
            path = join(self.current_directory, reg[0])
        else:
            print(f"File {reg[0]} not found.")
            return 0
        
        subprocess.call([path])

        return 1



    def in_root(self):
        if len(self.current_directory.split("\\")) == 2 and self.current_directory.split("\\")[1] == "":
            return True
        return False

    @staticmethod
    def parse_args(args):
        optional = []
        reg =[]

        for arg in args:
            if "-" == arg[0]:
                arg = arg[1:]
                if len(arg) > 1:
                    arg = list(arg)
                optional += arg
            else:
                reg.append(arg)

        reg_new = []
        concatting = False
        j = 0
        for i in range(len(reg)):
            
            if concatting:
                reg_new[j] += " " + reg[i]
                if "\"" in reg[i]:
                    concatting = False
                    j += 1
                continue
            
            if "\"" in reg[i]:
                concatting = True

            reg_new.append(reg[i])
        
        reg = [p.replace('"', "") for p in reg_new]

        return (reg, optional)

    def parse_environment_variables(self, command):

        for i in range(len(command)):
            for occurence in re.findall(r'%(.*?)%', command[i]):
                env_var = self.get_environment_variable(occurence)
                if env_var != 0:
                    command[i] = command[i].replace(f"%{occurence}%", env_var)
        return command

    
    @staticmethod
    def check_argument_validity(reg, opt, reg_max_len, opt_list):
        if len(reg) > reg_max_len:
            return 0, "Too many arguments."
        for var in opt:
            if var not in opt_list:
                return 0, f"Option -{var} not found."
        return 1, "Success"
    

    def check_command_validity(self, command):
        if hasattr(self.__class__, command) and callable(getattr(self.__class__, command)):
            return 1
        else:
            return 0

    def activate_redirect(self,args):
        if ">" in args:
            
            ind = args.index(">")

            f = args[ind+1]

            if isfile(join(self.current_directory, f)):
                f = join(self.current_directory, f)
            
            del args[ind]
            del args[ind]

            if not isfile(f):
                print("Redirect is not a valid filename.")
                return -1

            self.redirect_file = f
            return f
    
        return 0



frame = Frame()

while True:
    try:
        command = filter_empty_strings(frame.parse_environment_variables(filter_empty_strings(input(frame.current_directory + ">").split(" "))))
        args = []
        if len(command) == 0:
            continue
        elif len(command) > 1:
            args = command[1:]
        command = str.lower(command[0])

        if frame.activate_redirect(args) == -1:
            continue

        if frame.check_command_validity(command):
            if frame.redirect_file != "":
                with open(frame.redirect_file, "w") as sys.stdout:
                    getattr(frame, command)(args)
            else:
                getattr(frame, command)(args)
            
            if frame.redirect_file != "":
                frame.redirect_file = ""
                sys.stdout = STDOUT
        elif frame.check_for_exe_redirect_wrapper(command, args):
            pass
        else:
            print(f"Command {command} not found.")

    except Exception as e:
        print(e)