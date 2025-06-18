


# yourcli/registry.py
from dataclasses import dataclass
from enum import Enum
from typing import List, Literal

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
                    if key != keys[-1]:
                        _commands_dict[key] = {}
                        _commands_dict = _commands_dict[key]
                else:
                    if key == keys[-1]: # 检查实际参数是否已经被注册
                        raise ValueError(f"{'.'.join(_keys)} is already registered")
                    else:
                        _commands_dict = cls._commands.get(key)
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
        return _dict_get(name.split("."))


    @classmethod
    def list(cls):
        return list(cls._commands.keys())


    @classmethod
    def print(self):
        pass


class SupportSysVersion(str, Enum):
    Ubuntu1804 = "Ubuntu1804"
    Ubuntu2004 = "Ubuntu2004"
    Ubuntu2204 = "Ubuntu2204"


# TODO 如何注册到指定的系统版本上
def register(name: str, ):
    def decorator(command_cls):
        ToolRegistry.register(name, command_cls)
        return command_cls
    return decorator


def register1(name: str, sys_version: SupportSysVersion):
    if not sys_version in SupportSysVersion.__members__.keys():
        raise ValueError(f"ToolRegistry.register Error:{sys_version} not in ")
    def decorator(command_cls):
        ToolRegistry.register(f"{sys_version}.{name}", command_cls)
    return decorator
    



if __name__ == "__main__":
    ToolRegistry.register("a.b.c.d.e", "wget")
    register1("ab.c", SupportSysVersion.Ubuntu1804)