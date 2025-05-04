









from abc import ABC, abstractmethod

from onekeyinstall.pm import PMExecutor
from onekeyinstall.utils import ShellExecutor, System


class Installer(ABC):
    
    PACKAGE_NAME = ""


    def __init__(self, executor:ShellExecutor = ShellExecutor(True, True, True), system: System = System()):
        
        self._executor = executor
        self._system = system
        self.pm_executor = PMExecutor(distribution=self._system.distribution)



    def pre_install(self):
        pass
    

    def install(self):
        self.pm_executor.install(self.PACKAGE_NAME)


    def post_install(self):
        pass
    


    def pre_uninstall(self):
        pass
    

    def uninstall(self):
        self.pm_executor.remove(self.PACKAGE_NAME)


    def post_uninstall(self):
        pass
    
    