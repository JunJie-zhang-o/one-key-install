






# 命令模式，当前的命令内容，以及实际执行的内容，还需要有指定的依赖和顺序



from abc import ABC, abstractmethod
from typing import Any, Callable


class Command(ABC):

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass


class FuncCommand(Command):

    def __init__(self, func: Callable):
        super().__init__()
        self._func = func

    
    def execute(self, **kwargs):
        return self._func(**kwargs)


class Pipeline:

    def __init__(self):
        self.commands = {}


    def add(self, name: str, command:Command):
        self.commands.update({name: command})
        return self


    def run(self):
        # for command in self.commands:
        #     ret = command()
        # for tip,
        # note 应该在实际的执行侧进行执行,或者需要将当前的command name 传出去,以用来显示
        pass
