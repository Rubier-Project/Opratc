#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dev: Host1let
"""
BufferArgv Library
~~~~~~

Controll Your Data in Terminal 
```
from Buffer.BufferArgv import BufferConsole
```
"""

import sys
import json

class BufferAttribute(object):
    def __init__(self, dic):
        self.dic = dic
        for key in dic.keys():
            setattr(self, key, dic[key])

class BufferForm(BufferAttribute):
    def __init__(self, dic):
        super().__init__(dic)
        
class BufferList(object):
    def __init__(self,
                 List: list = [],
                 ):
        
        self.list = List
        
    def parse(self):
        bfd = {}

        for i in range(len(self.list)):
            bfd[str(i+1)] = self.list[i]

        return bfd

    def isexists(self, target):
        if target in self.list:
            return True
        else:return False

    def isinfrontof(self, target, indexes):
        isit = False

        if target in self.list:
            try:
                indx = self.list.index(target)
                if indx == indexes:
                    isit = True
                else:isit = False
            except Exception as e:return e
        
        return isit
    
    def indexexists(self, target):
        if target in self.list:
            return self.list.index(target)
        else:return False

class Things(object):
    def __init__(self) -> None:
        self.def_attrs = ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']

    def __str__(self) -> str:
        return json.dumps(dir(self), indent=2)
    
    @property
    def options(self) -> list:
        opts = []

        for item in dir(self):
            if item.startswith("__") and item in self.def_attrs:pass
            else:opts.append(item)

        opts.remove("def_attrs")
        opts.remove("options")
        
        return opts

class BufferConsole(object):
    def __init__(self):
        self.last_things = Things()
        self.handlers = []
        self.buffer_list = BufferList
        self.modes = [
            'in_front_of',
            'on_call',
            'equals_with'
        ]
        self.string_abs = [
            "str",
            "string",
            "strings"
        ]
        self.int_abs = [
            "int",
            "integer",
            "number"
        ]
        self.dict_abs = [
            "dict",
            "dictionary",
            "json"
        ]
        self.bool_abs = [
            "bool",
            "boolean",
            "true-false"
        ]
    
    def getDictArgv(self):
        return BufferList(sys.argv).parse()
    
    def isArray(self, array: str):
        try:
            return {"is_array": True, "array": json.loads(array)}
        except:return {"is_array": False}

    def isBoolean(self, boolean: str):
        try:
            if boolean.startswith("t"):
                return {"is_boolean": True, "boolean": bool("T"+boolean[1:])}
            elif boolean.startswith("f"):
                return {"is_boolean": True, "boolean": bool("F"+boolean[1:])}
            else:return {"is_boolean": True, "boolean": bool(boolean)}
        except:return {"is_boolean": False}
    
    def addFlag(self, *flags, mode: str = "in_front_of", obj_type: str = "str"):
        def decorator(func):
            self.handlers.append({func: {"flags": list(set(flags)), "mode": mode, "type": obj_type.lower()}})
            return func
        return decorator
    
    def setFilter(self, flags_list: list, err_message: str, _exit: bool = True):
        """
        Check The all arguments and detect the mistakes\n

        Use 'B@ARGV' key word in your err_message to see invalid argument:\n

        buffer.setFilter(\n
            flags_list=[ '-h', '--help' ],\n
            err_message="Invalid Key: B@ARGV",
            _exit=True
            )

        Parameters:
            - **flags_list** (list): The flags used in the script.
            - **err_message** (str): Message printed if an invalid argument is detected.
            - **_exit** (bool): If True, the program will terminate upon detecting an invalid argument.
        """

        flags = list(set(flags_list))
        argvs = sys.argv

        for argv in argvs:
            if argv.startswith("-"):
                if not argv in flags:
                    print(err_message.replace("B@ARGV", argv))

                    if _exit:
                        exit(1)

    def trust(self):
        for handler in self.handlers:
            func = list(handler.keys())[0]
            flags = handler[func]['flags']
            mode = handler[func]['mode']
            type = handler[func]['type']

            argv = self.buffer_list(sys.argv).parse()
            arg_key = list(argv.keys())
            arg_val = list(argv.values())

            if mode == "in_front_of":

                for flag in flags:

                    setattr(self.last_things, flag.replace("-", ""), "NONECALL")

                    if flag in arg_val:
                        arg_index = arg_val.index(flag)
                        ifo_key = str(arg_index+2)
                        cleared_key = argv[str(arg_index+1)].replace("-", "")

                        if ifo_key in arg_key:

                            if type in self.string_abs:
                                setattr(self.last_things, cleared_key, argv[ifo_key])
                                
                            elif type in self.int_abs:
                                if argv[ifo_key].isdigit():
                                    setattr(self.last_things, cleared_key, int(argv[ifo_key]))
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])

                            elif type in self.dict_abs:
                                status = self.isArray(argv[ifo_key])

                                if status['is_array']:
                                    setattr(self.last_things, cleared_key, status['array'])
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])
                                
                            elif type in self.bool_abs:
                                status = self.isBoolean(argv[ifo_key])

                                if status['is_boolean']:
                                    setattr(self.last_things, cleared_key, status['boolean'])
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])
                        else:
                            setattr(self.last_things, cleared_key, "Null")

            elif mode == "on_call":
                for flag in flags:

                    setattr(self.last_things, flag.replace("-", ""), "NONECALL")

                    if flag in arg_val:
                        arg_index = arg_val.index(flag)
                        k = argv[str(arg_index+1)]
                        cleared_key = k.replace("-", "")

                        if k in arg_val:
                            setattr(self.last_things, cleared_key, True)

                        else:
                            setattr(self.last_things, cleared_key, False)

            elif mode == "equals_with":
                for flag in flags:
                    setattr(self.last_things, flag.replace("-", ""), "NONECALL")
                    for arg in sys.argv:
                        if arg.startswith(flag):
                            if "=" in arg:
                                splitted_data = arg.split("=")[-1]

                                if not splitted_data.strip() == "":

                                    if type in self.string_abs:
                                        setattr(self.last_things, flag.replace("-", ""), splitted_data)

                                    elif type in self.int_abs:
                                        if splitted_data.isdigit():
                                            setattr(self.last_things, flag.replace("-", ""), int(splitted_data))
                                        else:
                                            setattr(self.last_things, flag.replace("-", ""), splitted_data)

                                    elif type in self.dict_abs:
                                        status = self.isArray(splitted_data)
                                        
                                        if status['is_array']:
                                            setattr(self.last_things, flag.replace("-", ""), status['array'])
                                        else:setattr(self.last_things, flag.replace("-", ""), splitted_data)
                                    
                                    elif type in self.bool_abs:
                                        status = self.isBoolean(splitted_data)

                                        if status['is_boolean']:
                                            setattr(self.last_things, flag.replace("-", ""), status['boolean'])
                                        else:setattr(self.last_things, flag.replace("-", ""), splitted_data)
                                    else:setattr(self.last_things, flag.replace("-", ""), "NONEEQUALS")
                                else:setattr(self.last_things, flag.replace("-", ""), splitted_data)
                            else:setattr(self.last_things, flag.replace("-", ""), "NONEEQUALS")
                        
            func(self.last_things)

class BufferString(object):
    def __init__(self, string: str):
        assert isinstance(string, str), exit("The Self@BufferString did not get a string value")
        self.string = string.split()
        self.last_things = Things()
        self.handlers = []
        self.buffer_list = BufferList
        self.modes = [
            'in_front_of',
            'on_call'
        ]
        self.string_abs = [
            "str",
            "string",
            "strings"
        ]
        self.int_abs = [
            "int",
            "integer",
            "number"
        ]
        self.dict_abs = [
            "dict",
            "dictionary",
            "json"
        ]
        self.bool_abs = [
            "bool",
            "boolean",
            "true-false"
        ]
    
    def getDictArgv(self):
        return BufferList(self.string).parse()
    
    def isArray(self, array: str):
        try:
            return {"is_array": True, "array": json.loads(array)}
        except:return {"is_array": False}

    def isBoolean(self, boolean: str):
        try:
            if boolean.startswith("t"):
                return {"is_boolean": True, "boolean": bool("T"+boolean[1:])}
            elif boolean.startswith("f"):
                return {"is_boolean": True, "boolean": bool("F"+boolean[1:])}
            else:return {"is_boolean": True, "boolean": bool(boolean)}
        except:return {"is_boolean": False}
    
    def addFlag(self, *flags, mode: str = "in_front_of", obj_type: str = "str"):
        def decorator(func):
            self.handlers.append({func: {"flags": list(set(flags)), "mode": mode, "type": obj_type.lower()}})
            return func
        return decorator
    
    def setFilter(self, flags_list: list, err_message: str, _exit: bool = True):
        """
        Check The all arguments and detect the mistakes\n

        Use 'B@ARGV' key word in your err_message to see invalid argument:\n

        buffer.setFilter(\n
            flags_list=[ '-h', '--help' ],\n
            err_message="Invalid Key: B@ARGV",
            _exit=True
            )

        Parameters:
            - **flags_list** (list): The flags used in the script.
            - **err_message** (str): Message printed if an invalid argument is detected.
            - **_exit** (bool): If True, the program will terminate upon detecting an invalid argument.
        """

        flags = list(set(flags_list))
        argvs = self.string

        for argv in argvs:
            if argv.startswith("-"):
                if not argv in flags:
                    print(err_message.replace("B@ARGV", argv))

                    if _exit:
                        exit(1)

    def trust(self):
        for handler in self.handlers:
            func = list(handler.keys())[0]
            flags = handler[func]['flags']
            mode = handler[func]['mode']
            type = handler[func]['type']

            argv = self.buffer_list(self.string).parse()
            arg_key = list(argv.keys())
            arg_val = list(argv.values())

            if mode == "in_front_of":

                for flag in flags:

                    setattr(self.last_things, flag.replace("-", ""), "NONECALL")

                    if flag in arg_val:
                        arg_index = arg_val.index(flag)
                        ifo_key = str(arg_index+2)
                        cleared_key = argv[str(arg_index+1)].replace("-", "")

                        if ifo_key in arg_key:

                            if type in self.string_abs:
                                setattr(self.last_things, cleared_key, argv[ifo_key])
                                
                            elif type in self.int_abs:
                                if argv[ifo_key].isdigit():
                                    setattr(self.last_things, cleared_key, int(argv[ifo_key]))
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])

                            elif type in self.dict_abs:
                                status = self.isArray(argv[ifo_key])

                                if status['is_array']:
                                    setattr(self.last_things, cleared_key, status['array'])
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])
                                
                            elif type in self.bool_abs:
                                status = self.isBoolean(argv[ifo_key])

                                if status['is_boolean']:
                                    setattr(self.last_things, cleared_key, status['boolean'])
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])
                        else:
                            setattr(self.last_things, cleared_key, "Null")

            elif mode == "on_call":
                for flag in flags:

                    setattr(self.last_things, flag.replace("-", ""), "NONECALL")

                    if flag in arg_val:
                        arg_index = arg_val.index(flag)
                        k = argv[str(arg_index+1)]
                        cleared_key = k.replace("-", "")

                        if k in arg_val:
                            setattr(self.last_things, cleared_key, True)

                        else:
                            setattr(self.last_things, cleared_key, False)

            elif mode == "equals_with":
                for flag in flags:
                    setattr(self.last_things, flag.replace("-", ""), "NONECALL")
                    for arg in self.string:
                        if arg.startswith(flag):
                            if "=" in arg:
                                splitted_data = arg.split("=")[-1]
                                if not splitted_data.strip() == "":

                                    if type in self.string_abs:
                                        setattr(self.last_things, flag.replace("-", ""), splitted_data)

                                    elif type in self.int_abs:
                                        if splitted_data.isdigit():
                                            setattr(self.last_things, flag.replace("-", ""), int(splitted_data))
                                        else:
                                            setattr(self.last_things, flag.replace("-", ""), splitted_data)

                                    elif type in self.dict_abs:
                                        status = self.isArray(splitted_data)
                                        
                                        if status['is_array']:
                                            setattr(self.last_things, flag.replace("-", ""), status['array'])
                                        else:setattr(self.last_things, flag.replace("-", ""), splitted_data)
                                    
                                    elif type in self.bool_abs:
                                        status = self.isBoolean(splitted_data)

                                        if status['is_boolean']:
                                            setattr(self.last_things, flag.replace("-", ""), status['boolean'])
                                        else:setattr(self.last_things, flag.replace("-", ""), splitted_data)
                                    else:setattr(self.last_things, flag.replace("-", ""), splitted_data)
                                else:setattr(self.last_things, flag.replace("-", ""), "NONEEQUALS")
                            else:setattr(self.last_things, flag.replace("-", ""), "NONEEQUALS")
                        
            func(self.last_things)