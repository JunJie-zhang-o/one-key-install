


# yourcli/registry.py
from dataclasses import dataclass
from typing import List

import functools




class ToolRegistry:
    _commands = {}

    @classmethod
    def register(cls, name: str, command_cls):

        def _dict_set(keys: List[str], value):
            _keys = []
            _commands_dict = cls._commands
            for key in keys:
                _keys.append(key)
                if key not in _commands_dict:
                    _commands_dict[key] = {}
                    _commands_dict = _commands_dict[key]
                else:
                    raise ValueError(f"{'.'.join(_keys)} is already registered")
            _commands_dict[key] = value
        nl = name.split(".")
        _dict_set(nl, command_cls)


    @classmethod
    def get(cls, name):
        def _dict_get(keys: List[str], default=None):
            _key = []
            _commands_dict = cls._commands
            for key in keys:
                if key in _commands_dict:
                    _commands_dict = _commands_dict[key]
                else:
                    return default
            return _commands_dict
        return _dict_get(name)


    @classmethod
    def list(cls):
        return list(cls._commands.keys())


    @classmethod
    def print(self):
        pass



def register(name: str):
    def decorator(command_cls):
        ToolRegistry.register(name, command_cls)
    return decorator
    





if __name__ == "__main__":
    ToolRegistry.register("a.b.c.d.e", "wget")