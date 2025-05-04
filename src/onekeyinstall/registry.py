


# yourcli/registry.py
class ToolRegistry:
    _commands = {}

    @classmethod
    def register(cls, name: str, command_cls):

        if name.find(".") >= 0:
            pre, post = name.split(".")
            if pre not in cls._commands:
                cls._commands[pre] = {}
                cls._commands[pre][post] = command_cls
            elif pre in cls._commands and post not in cls._commands[pre]:
                cls._commands[pre][post] = command_cls
            else:
                raise ValueError(f"{name} is already registered")
        else:
            if name not in cls._commands:
                cls._commands[name] = command_cls
            else:
                raise ValueError(f"{name} is already registered")
    

    @classmethod
    def get(cls, name):
        return cls._commands.get(name)


    @classmethod
    def list(cls):
        return list(cls._commands.keys())


    @classmethod
    def print(self):
        pass



# 检查是否已经安装
import shutil
def check_installation(package_name):
    """
    检查是否已经安装指定软件包

    参数:
    package_name (str): 要检查的软件包名称

    返回:
    bool: 如果软件包已安装，则返回True，否则返回False
    """

    if shutil.which(package_name):
        # print("系统已安装 wget")\
        return True
    else:
        # print("系统未安装 wget")
        return False