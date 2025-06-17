









from abc import ABC, abstractmethod
from ast import List

from onekeyinstall.downloader import Downloader
from onekeyinstall.helper import EnvHelper
from onekeyinstall.pm import PMExecutor
from onekeyinstall.utils import ShellExecutor, System
from onekeyinstall.cmds import Pipeline

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


    @abstractmethod
    def register_install(self):
        self._install.add(self.pm_executor.get_cmd("install", self.PACKAGE_NAME), lambda:self.pm_executor.install(self.PACKAGE_NAME))


    @abstractmethod
    def register_uninstall(self):
        self._uninstall.add(self.pm_executor.get_cmd("remove", self.PACKAGE_NAME), lambda:self.pm_executor.install(self.PACKAGE_NAME))
    

    @abstractmethod
    def description(self) -> str:
        pass