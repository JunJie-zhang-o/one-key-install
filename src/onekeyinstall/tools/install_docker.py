



from onekeyinstall.installer import Installer
from onekeyinstall.registry import register
from onekeyinstall.utils import Arch, get_offline_install_package_suffix




@register("docker")
class InstallDocker(Installer):



    def pre_install(self):
        pass



    def register_install(self):
        # return super().register_install()
        self._install.add("setup docker apt repo", self.setup_docker_apt_repo)
        self._install.add("install docker", lambda: self._executor.run("sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"))
        self._install.add("add user to docker group", lambda: self._executor.run("sudo usermod -aG docker $USER"))
    


    def setup_docker_apt_repo(self):
        self.pm_executor.update()
        self.pm_executor.install("ca-certificates")
        self.pm_executor.install("curl")
        self._executor.run(f"sudo install -m 0755 -d /etc/apt/keyrings")
        for i in range(5):
            self._executor.run(f"sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc")
        self._executor.run(f"sudo chmod a+r /etc/apt/keyrings/docker.asc")
        docker_apt_source_cmd = (
            "echo "
            "\"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] "
            "https://download.docker.com/linux/ubuntu "
            "$( . /etc/os-release && echo \\\"${UBUNTU_CODENAME:-$VERSION_CODENAME}\\\" ) stable\" | "
            "sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"
        )
        self._executor.run(docker_apt_source_cmd)
        self.pm_executor.update()




    def register_uninstall(self):

        self._uninstall.add("", lambda: self._executor.run("sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras"))
        self._uninstall.add("", lambda: self._executor.run("sudo rm -rf /var/lib/containerd"))
        self._uninstall.add("", lambda: self._executor.run("sudo rm -rf /var/lib/docker"))
        self._uninstall.add("", lambda: self._executor.run("sudo rm /etc/apt/sources.list.d/docker.list"))
        self._uninstall.add("", lambda: self._executor.run("sudo rm /etc/apt/keyrings/docker.asc"))



