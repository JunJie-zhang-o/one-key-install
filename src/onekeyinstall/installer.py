









from abc import ABC, abstractmethod
from ast import List
from queue import Queue
from typing import Callable

from onekeyinstall.downloader import Downloader
from onekeyinstall.helper import EnvHelper
from onekeyinstall.pm import PMExecutor
from onekeyinstall.utils import ShellExecutor, System
from onekeyinstall.utils import OKILogging as logging
from onekeyinstall.cmds import Pipeline


logger = logging.getLogger()


class Installer(ABC):
    
    PACKAGE_NAME = ""


    def __init__(self, executor:ShellExecutor = ShellExecutor(True, True, True), system: System = System()):
        
        self._executor        = executor
        self._system          = system
        self.pm_executor      = PMExecutor(distribution=self._system.distribution)
        self.downloader       = Downloader(executor=ShellExecutor(False, True, True))
        self.env_helper       = EnvHelper(EnvHelper.get_default_shell())



        self._pre_install     = Pipeline()
        self._install         = Pipeline()
        self._post_install    = Pipeline()
        self._pre_uninstall   = Pipeline()
        self._uninstall       = Pipeline()
        self._post_install    = Pipeline()

        self._dependency:List[Installer]      = []


        self.register_install()
        self.register_uninstall()


    @abstractmethod
    def register_install(self):
        self._install.add(" ".join(self.pm_executor.get_cmd("install", self.PACKAGE_NAME)), lambda:self.pm_executor.install(self.PACKAGE_NAME))


    @abstractmethod
    def register_uninstall(self):
        self._uninstall.add(" ".join(self.pm_executor.get_cmd("remove", self.PACKAGE_NAME)), lambda:self.pm_executor.remove(self.PACKAGE_NAME))
    

    @abstractmethod
    def description(self) -> str:
        pass




class OKIInstaller:


    def __init__(self, installer: Installer, title_callback:Callable, log_callback:Callable, progress_bar_callback:Callable, ):
        
        self._installer:Installer = installer()

        self._title_callback = title_callback
        self._log_callback = log_callback
        self._progress_bar_callback = progress_bar_callback



    def install(self):
        
        for func_name, func in self._installer._install.commands.items():
            self._title_callback(func_name)
            func()
            # 对于文件和环境变量类型的,对日志如何处理



    def uninstall(self):
        pass