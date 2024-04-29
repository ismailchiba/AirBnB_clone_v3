#!/usr/bin/python3
'''
    Implementing the console for the HBnB project.
'''
import cmd
import json
import shlex
import models
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    '''
        Contains the entry point of the command interpreter.
    '''
    prompt = "(hbnb) "

    def do_quit(self, args):
        '''
            Quit command to exit the program.
        '''
        return True

    def do_EOF(self, args):
        '''
            Exits after receiving the EOF signal.
        '''
        return True

    def do_create(self, args):
        '''
            Create a new instance of class BaseModel and saves it
            to the JSON file.
        '''
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            args = shlex.split(args)
            new_instance = eval(args[0])()
            for i in args[1:]:
                try:
                    key, value = i.split("=")
                    value = value.replace("_", " ")
                    if hasattr(new_instance, key):
                        setattr(new_instance, key, eval(value))
                except (ValueError, IndexError):
                    pass
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        '''
            Print the string representation of an instance based on
            the class name and id given as args.
        '''
        args = shlex.split(args)
        if len(args) < 2:
            print("** class name missing **" if len(args) == 0 else "** instance id missing **")
            return
        obj_dict = storage.all(args[0])
        try:
            if args[0] not in models.__all__:
                raise NameError
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        try:
            value = obj_dict[key]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        '''
            Deletes an instance based on the class name and id.
        '''
        args = shlex.split(args)
        if len(args) < 2:
            print("** class name missing **" if len(args) == 0 else "** instance id missing **")
            return
        class_name, class_id = args[0], args[1]
        obj_dict = storage.all()
        if class_name not in models.__all__:
            print("** class doesn't exist **")
            return
        key = class_name + "." + class_id
        try:
            del obj_dict[key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, args):
        '''
            Prints all string representation of all instances
            based or not on the class name.
        '''
        obj_list = []
        objects = storage.all(args)
        if args and args not in models.__all__:
            print("** class doesn't exist **")
            return
        for obj in objects.values():
            obj_list.append(str(obj))
        print(obj_list)

    def do_update(self, args):
        '''
            Update an instance based on the class name and id
            sent as args.
        '''
        storage.reload()
        args = shlex.split(args)
        if len(args) < 4:
            print("** class name missing **" if len(args) == 0 else
                  "** instance id missing **" if len(args) == 1 else
                  "** attribute name missing **" if len(args) == 2 else
                  "** value missing **")
            return
        class_name, class_id, attr_name, attr_value = args
        obj_dict = storage.all()
        if class_name not in models.__all__:
            print("** class doesn't exist **")
            return
        key = class_name + "." + class_id
        try:
            obj_value = obj_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, attr_name))
            setattr(obj_value, attr_name, attr_type(attr_value))
            obj_value.save()
        except AttributeError:
            print("** no attribute found **")

    def emptyline(self):
        '''
            Prevents printing anything when an empty line is passed.
        '''
        pass

    def do_count(self, args):
        '''
            Counts/retrieves the number of instances.
        '''
        storage.reload()
        obj_list = [obj for obj in storage.all().values() if isinstance(obj, eval(args))]
        print(len(obj_list))

    def default(self, args):
        '''
            Catches all the function names that are not explicitly defined.
        '''
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy}
        args = shlex.split(args)
        if len(args) < 2:
            print("*** Unknown syntax:", args[0])
            return
        cmd_arg = args[0] + " " + args[1]
        func_name = args[2]
        try:
            func = functions[func_name]
            func(cmd_arg)
        except KeyError:
            print("*** Unknown command:", func_name)


if __name__ == "__main__":
    '''
        Entry point for the loop.
    '''
    HBNBCommand().cmdloop()
