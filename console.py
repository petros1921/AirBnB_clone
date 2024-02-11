#!/usr/bin/python3
"""Define a Air_BNB interactive console."""

import cmd
import json
import shlex
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse_arguments(arguments):
    curly_braces = re.search(r"\{(.*?)\}", arguments)
    brackets = re.search(r"\[(.*?)\]", arguments)
    if curly_braces is None:
        if brackets is None:
            return [item.strip(",") for item in split(arguments)]
        else:
            lexer = split(arguments[:brackets.span()[0]])
            ret_list = [item.strip(",") for item in lexer]
            ret_list.append(brackets.group())
            return ret_list
    else:
        lexer = split(arguments[:curly_braces.span()[0]])
        ret_list = [item.strip(",") for item in lexer]
        ret_list.append(curly_braces.group())
        return ret_list


class HBNBConsole(cmd.Cmd):

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):

        pass

    def default(self, arguments):

        argument_dict = {
            "all": self.do_list_all,
            "show": self.do_show_object,
            "destroy": self.do_destroy_object,
            "count": self.do_count_objects,
            "update": self.do_update_object
        }
        match = re.search(r"\.", arguments)
        if match is not None:
            arg_list = [arguments[:match.span()[0]], arguments[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                command = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argument_dict.keys():
                    call = "{} {}".format(arg_list[0], command[1])
                    return argument_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arguments))
        return False

    def do_quit(self, arguments):

        return True

    def do_EOF(self, arguments):

        print("")
        return True

    def do_create(self, arguments):

        arg_list = parse_arguments(arguments)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBConsole.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

    def do_show(self, arguments):

        arg_list = parse_arguments(arguments)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBConsole.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def do_destroy(self, arguments):

        arg_list = parse_arguments(arguments)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBConsole.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def do_list_all(self, arguments):

        arg_list = parse_arguments(arguments)
        if len(arg_list) > 0 and arg_list[0] not in HBNBConsole.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_list) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_count_objects(self, arguments):

        arg_list = parse_arguments(arguments)
        count = 0
        for obj in storage.all().values():
            if arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update_object(self, arguments):

        arg_list = parse_arguments(arguments)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if arg_list[0] not in HBNBConsole.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:


if __name__ == '__main__':
    HBNBCommand().cmdloop()
