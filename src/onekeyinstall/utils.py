

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



class System:
    """
    Get System Base Info
    """
    def __init__(self):
        self.os = platform.system().lower()
        self.arch = platform.machine()

        if self.os == "linux":
            self.distribution, self.version = self.__linux_info()
        elif self.os == "windows":
            self.distribution = platform.release()
            self.version = platform.version()
        elif self.os == "darwin":
            self.distribution, self.version = self.__mac_info()


    def __linux_info(self):
        with open("/etc/os-release") as f:
            os_release = dict(line.strip().replace("\"", "").split("=", 1) for line in f if "=" in line)
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

            while True:

                ret = select.select([process.stdout, process.stderr], [], [])

                for fd in ret[0]:
                    line = process.stdout.readline()
                    if line:
                        if self.verbose:
                            print(f"[stdout] {line.strip()}")
                        if self.capture_output:
                            stdout_lines.append(line)
                    if fd == process.stderr.fileno():
                        line = process.stderr.readline()
                        if line:
                            if self.verbose:
                                print(f"[stderr] {line.strip()}")
                            if self.capture_output:
                                stderr_lines.append(line)

                if process.poll() is not None:
                    break


            returncode = process.wait()

            if self.check and returncode != 0:
                raise subprocess.CalledProcessError(returncode, cmd)

            return result
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            return e



# 环境变量


# 配置文件


if __name__ == '__main__':
    executor = ShellExecutor(capture_output=True, verbose=True, check=True)
    result = executor.run("ls -l")
    # print(result.stdout)

