from abc import ABC, abstractmethod
from io import TextIOWrapper
from pathlib import Path
import platform
from typing import Dict, Literal, Union
import os

class Shell(ABC):

    @classmethod
    @abstractmethod
    def append_env(cls, name, value) -> str:
        pass

    # @classmethod
    # @abstractmethod
    # def append_line(cls, line: str):
    #     pass

    @classmethod
    @abstractmethod
    def get_default_env_file(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def activate_custom_env_file(cls, custom_env) -> str:
        pass


class ShellBash(Shell):

    @classmethod
    def append_env(cls, name, value) -> str:
        return f'export {name}="{value}":${name}'

    @classmethod
    def get_default_env_file(cls) -> str:
        return Path.home().joinpath(".bashrc")

    @classmethod
    def activate_custom_env_file(cls, custom_env) -> str:
        return f"[ -f ~/{custom_env} ] && source ~/{custom_env}"


class ShellZsh(ShellBash):

    @classmethod
    def get_default_env_file(cls) -> str:
        return Path.home().joinpath(".zshrc")


class ShellFish(Shell):

    @classmethod
    def append_env(cls, name, value) -> str:
        return f"set -x {name} {value} ${name}"

    @classmethod
    def get_default_env_file(cls) -> str:
        return Path.home().joinpath(".config","fish","config.fish")

    @classmethod
    def activate_custom_env_file(cls, custom_env) -> str:
        return f"[ -f ~/{custom_env} ] && source ~/{custom_env}"


class ShellIDontKnow(Shell):
    pass


# 环境变量
class EnvHelper:

    DEFAULT_CUSTOM_ENV_FILE = Path.home().joinpath(".one-key-install", ".oki_env")
    SHELLS:Dict[str,Shell] = {
        "bash": ShellBash,
        "zsh": ShellZsh,
        "fish": ShellFish,
    }
    OS = platform.platform().lower()

    def __init__(self, shell_type: Literal["bash", "zsh", "fish"]):
        self._shell = self.SHELLS.get(shell_type, None)
        if self._shell is None:
            print("The Shell Is InValid")
            quit()
        self._file_helper = FileHelper(file_path=self.DEFAULT_CUSTOM_ENV_FILE)


    def append_env(self, name, value):

        if self.OS in ["linux", "darwin"]:
            with self._file_helper as f:
                f.write(f"{self._shell.append_env(name, value)}\n")
        elif self.OS == "windows":
            # TODO how to append env in win sys
            pass

    @classmethod
    def get_default_shell(cls) -> Union[str, None]:
        if cls.OS in ["linux", "darwin"]:
            _SHELL = os.environ.get("SHELL")
            if "zsh" in _SHELL:
                return "zsh"
            elif "bash" in _SHELL:
                return "bash"
            elif "fish" in _SHELL:
                return "fish"
        return None


# 配置文件
class FileHelper:

    def __init__(self, file_path: Union[Path, str], mode: Literal["w", "a", "w+", "a+"] = "a"):

        self._file_path = Path(file_path)
        self._file_obj: Union[None, TextIOWrapper] = None
        self._mode = mode

        self.touch(self._file_path)


    def __enter__(self) -> TextIOWrapper:
        self._file_obj = self._file_path.open(self._mode, encoding="utf-8")
        return self._file_obj


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file_obj.close()
        self._file_obj = None


    def write_line(self, text: str, flush: bool = True):
        if not self._file_obj:
            self._file_obj = self._file_path.open(self._mode, encoding="utf-8")
        self._file_obj.write(f"{text}\n")
        if flush:
            self._file_obj.flush()
        self._file_obj.close()

    @classmethod
    def mkdir(cls, path):
        Path(path).mkdir(parents=True, exist_ok=True)

    @classmethod
    def touch(cls, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        if not Path(path).exists():
             Path(path).touch()

    @classmethod
    def exists(cls, path) -> bool:
        return Path(path).exists()


if __name__ == "__main__":
    # print(ShellFish.get_default_env_file())

    p = Path("~/.one-key-install/.oki_env")
    p.mkdir(parents=True, exist_ok=True)
    print(p.exists())