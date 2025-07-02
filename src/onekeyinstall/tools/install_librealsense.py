



from onekeyinstall.installer import Installer
from onekeyinstall.registry import register
from onekeyinstall.utils import Arch, get_offline_install_package_suffix


@register("docker")
class InstallDocker(Installer):


    """
    sudo mkdir -p /etc/apt/keyrings
    curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp | sudo tee /etc/apt/keyrings/librealsense.pgp > /dev/null
    
    echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.intel.com/Debian/apt-repo `lsb_release -cs` main" | \
    sudo tee /etc/apt/sources.list.d/librealsense.list
    sudo apt-get update
    """


    def register_install(self):
        # return super().register_install()
        self._install.add("", lambda: self.pm_executor.install("curl"))
        self._install.add("", lambda: self._executor.run("sudo mkdir -p /etc/apt/keyrings"))
        self._install.add("", lambda: self._executor.run("curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp | sudo tee /etc/apt/keyrings/librealsense.pgp > /dev/null"))
        cmd = ("echo"
               "\" deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.intel.com/Debian/apt-repo `lsb_release -cs` main | \\ \""
               "sudo tee /etc/apt/sources.list.d/librealsense.list")
        self._install.add("", lambda: self._executor.run(cmd))
        self._install.add("", lambda: self.pm_executor.update())

    

    def register_uninstall(self):
        self._uninstall.add("", lambda: self._executor.run("dpkg -l | grep \"realsense\" | cut -d \" \" -f 3 | xargs sudo dpkg --purge "))