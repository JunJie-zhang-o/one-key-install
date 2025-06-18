



from dataclasses import dataclass
from typing import Literal, Union, List

from onekeyinstall.utils import ShellExecutor


@dataclass
class SystemPackageManagerCMD:
    install   : Union[str, List[str]]
    list      : Union[str, List[str]]
    update    : Union[str, List[str]]
    remove    : Union[str, List[str]]
    search    : Union[str, List[str]]
    show      : Union[str, List[str]]



apt                 = SystemPackageManagerCMD(
    install         = ["apt-get", "install", "-y"],     # apt for human user interaction, apt-get for script
    list            = ["apt-get", "list"],
    update          = ["apt-get", "update", "-y"],
    remove          = ["apt-get", "remove", "-y"],
    search          = ["apt-get", "search"],
    show            = ["apt-get", "show"],
)

dnf                 = SystemPackageManagerCMD(
    install         = ["dnf", "install", "-y"],
    list            = ["dnf", "list"],
    update          = ["dnf", "update", "-y"],
    remove          = ["dnf", "remove", "-y"],
    search          = ["dnf", "search"],
    show            = ["dnf", "show"],
)

yum                 = SystemPackageManagerCMD(
    install         = ["yum", "install", "-y"],
    list            = ["yum", "list",],
    update          = ["yum", "update", "-y"],
    remove          = ["yum", "remove", "-y"],
    search          = ["yum", "search"],
    show            = ["yum", "show"],
)

pacman              = SystemPackageManagerCMD(
    install         = ["pacman", "-S", "--noconfirm"],
    list            = ["pacman", "-Q",],
    update          = ["pacman", "-Syu", "--noconfirm"],
    remove          = ["pacman", "-R", "--noconfirm"],
    search          = ["pacman", "-Ss"],
    show            = ["pacman", "-Si"],
)

zypper              = SystemPackageManagerCMD(
    install         = ["zypper", "install", "-y"],
    list            = ["zypper", "packages"],  # zypper 没有 list 命令，"packages"更合适
    update          = ["zypper", "refresh && zypper update", "-y"],
    remove          = ["zypper", "remove", "-y"],
    search          = ["zypper", "search"],
    show            = ["zypper", "info"],
)

apk                 = SystemPackageManagerCMD(
    install         = ["apk", "add", "--no-confirm"],
    list            = ["apk", "info"],
    update          = ["apk", "update"],
    remove          = ["apk", "del",],
    search          = ["apk", "search"],
    show            = ["apk", "info"],
)



PackageManager = {
    "ubuntu"    : apt,
    "debian"    : apt,
    "fedora"    : dnf,
    "centos"    : yum,
    "alpine"    : apk,
    "opensuse"  : zypper,
    "suse"      : zypper,
    "arch"      : pacman,
}






class PMExecutor(ShellExecutor):


    def __init__(self, distribution: Literal["ubuntu"] = "ubuntu"):
        super().__init__(capture_output=True, verbose=True, check=True)
        if distribution == "ubuntu":
            self.pm = apt


    def get_cmd(self, func, name):
        _cmd = getattr(self.pm, func)
        if isinstance(self.pm.install, list):
            return ["sudo"] + _cmd + [name]
        else:
            return f"sudo {_cmd} {name}"


    def install(self, name: str):
        cmd = self.get_cmd("install", name)
        self.run(cmd)
        

    def update(self):
        cmd = self.pm.update
        self.run(cmd)


    def remove(self, name: str):
        cmd = self.get_cmd("remove", name)
        self.run(cmd)


    def list(self, name: str = None):
        cmd = self.get_cmd("list", name)
        self.run(cmd)


    def search(self, name: str):
        cmd = self.get_cmd("search", name)
        self.run(cmd)


    def show(self, name: str):
        cmd = self.get_cmd("show", name)
        self.run(cmd)



if __name__ == "__main__":

    pme = PMExecutor(distribution="ubuntu")

    pme.install("git")