

import os
import platform

from enum import StrEnum


class LinuxDistroVersion(StrEnum):
    # Ubuntu
    UBUNTU_24_04 = "Ubuntu 24.04"
    UBUNTU_22_04 = "Ubuntu 22.04"
    UBUNTU_20_04 = "Ubuntu 20.04"

    # Debian
    DEBIAN_12 = "Debian 12"
    DEBIAN_11 = "Debian 11"
    DEBIAN_10 = "Debian 10"

    # Fedora
    FEDORA_40 = "Fedora 40"
    FEDORA_39 = "Fedora 39"
    FEDORA_38 = "Fedora 38"

    # CentOS (Stream)
    CENTOS_STREAM_9 = "CentOS Stream 9"
    CENTOS_STREAM_8 = "CentOS Stream 8"

    # Alpine
    ALPINE_3_19 = "Alpine 3.19"
    ALPINE_3_18 = "Alpine 3.18"
    ALPINE_3_17 = "Alpine 3.17"

    # openSUSE
    OPENSUSE_LEAP_15_6 = "openSUSE Leap 15.6"
    OPENSUSE_LEAP_15_5 = "openSUSE Leap 15.5"
    OPENSUSE_TUMBLEWEED = "openSUSE Tumbleweed"

    # SUSE Linux Enterprise
    SUSE_15_SP5 = "SUSE 15 SP5"
    SUSE_15_SP4 = "SUSE 15 SP4"

    # Arch Linux
    ARCH_ROLLING = "Arch (rolling)"



class Arch(StrEnum):
    X86 = "X86_64"
    ARM = "aarch64"
    LOONGARCH = "loongarch64"



class System:
    """
    Get System Base Info
    """
    def __init__(self):
        self.os = platform.system().lower()
        self.arch = platform.machine()
        self.locale = None
        if self.os == "linux":
            self.distribution, self.version = self.__linux_info()
            self.locale = os.environ.get("LANG", None)
        elif self.os == "windows":
            self.distribution = platform.release()
            self.version = platform.version()
        elif self.os == "darwin":
            self.distribution, self.version = self.__mac_info()
        


    def __linux_info(self):
        with open("/etc/os-release") as f:
            os_release = dict(line.strip().replace("\"", "").split("=", 1) for line in f if "=" in line)
            # todo 添加一个属性是哪个大类的linux发行版,便于识别文件下载的类型
        return os_release["NAME"].lower(), os_release["VERSION"]
    

    def __mac_info(self):
        mac_version = platform.mac_ver()[0]

        if mac_version.startswith("10."):
            return "Catalina", mac_version
        elif mac_version.startswith("11."):
            return "Big Sur", mac_version
        elif mac_version.startswith("12."):
            return "Monterey", mac_version
        elif mac_version.startswith("13."):
            return "Ventura", mac_version
        elif mac_version.startswith("14."):
            return "Sonoma", mac_version
        else:
            return "Unknown", mac_version



    def to_dict(self):
        return {
            "os": self.os,
            "arch": self.arch,
            "distribution": self.distribution,
            "version": self.version
        }
    


    





class ShellCMD:


    def __init__(self):
        pass




class RequireTool:

    def __init__(self):
        pass





import select
import subprocess
from typing import Union, List


class ShellExecutor:
    def __init__(self, capture_output=False, verbose=True, check=False):
        """
        :param capture_output: 是否捕获输出（如需获取返回内容）
        :param verbose: 是否打印输出到终端
        :param check: 是否在命令失败时抛出异常
        """
        self.capture_output = capture_output
        self.verbose = verbose
        self.check = check

    def run(self, cmd: Union[str, List[str]]):
        """
        执行终端命令
        :param cmd: 要执行的命令，可以是字符串或字符串列表
        :return: subprocess.CompletedProcess 对象
        """
        shell = isinstance(cmd, str)

        try:
            process = subprocess.Popen(
                cmd,
                shell=shell,
                stdout=subprocess.PIPE if self.capture_output else None,
                stderr=subprocess.PIPE if self.capture_output else None,
                universal_newlines=True,  # 等同于 text=True，兼容 Py3.6
                bufsize=1,
            )

            stdout_lines = []
            stderr_lines = []

            while self.capture_output:
            
                ret = select.select([process.stdout, process.stderr], [], [], 0.1)

                for fd in ret[0]:
                    # line = process.stdout.readline()
                    line = fd.readline()
                    if line:
                        if self.verbose:
                            # print(f"[stdout] {line.strip()}")
                            prefix = "[stdout]" if fd == process.stdout else "[stderr]"
                            print(f"{prefix} {line.strip()}")
                        if self.capture_output:
                            stdout_lines.append(line) if fd == process.stdout else stderr_lines.append(line)
                    # if fd == process.stderr.fileno():
                    #     line = process.stderr.readline()
                    #     if line:
                    #         if self.verbose:
                    #             print(f"[stderr] {line.strip()}")
                    #         if self.capture_output:
                    #             stderr_lines.append(line)
                print("running")
                if process.poll() is not None:
                    break


            returncode = process.wait()

            if self.check and returncode != 0:
                raise subprocess.CalledProcessError(returncode, cmd)

            return returncode
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            return e



# 环境变量


# 配置文件




# 检查是否已经安装
import shutil
def check_installation(package_name):
    """
    检查是否已经安装指定软件包
    """
    if shutil.which(package_name):
        return True
    else:
        return False


def get_offline_install_package_suffix():
    if check_installation("apt"):
        return ".deb"
    elif check_installation("pacman"):
        return ".pkg.tar.zst"
    elif check_installation("dnf"):
        return ".rpm"
    elif check_installation("yum"):
        return ".rpm"
    elif check_installation("zypper"):
        return ".rpm"
    elif check_installation("apk"):
        return ".apk"

def get_shell_executor():
    """
    获取当前系统的默认shell执行器
    """
    shell = os.environ.get("SHELL")
    if shell:
        return shell
    else:
        return "/bin/bash"


if __name__ == '__main__':
    executor = ShellExecutor(capture_output=True, verbose=True, check=True)
    result = executor.run("ls -l")
    # print(result.stdout)

