# https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.deb


# curl基本上都有 但是wget不一定需要自己安装

# curl -o name url
from email import header
import urllib.request
from pathlib import Path
from onekeyinstall.utils import ShellExecutor, check_installation


class Downloader:

    DEFAULT_DOWNLOAD_PATH = f"/tmp/onekeyinstall"

    def __init__(self, executor: ShellExecutor = ShellExecutor(False, True, True)):
        self._executor = executor

        Path(self.DEFAULT_DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)


    def download(self, url: str, output_file: str):

        if check_installation("wget"):
            self._wget(url, output_file)
        elif check_installation("curl"):
            self._curl(url, output_file)
        else:
            self._urllib(url, output_file)
        return f"{self.DEFAULT_DOWNLOAD_PATH}/{output_file}"


    def _curl(self, url: str, output_file: str):
        # cmd = ["curl", "-o", f"{self.DEFAULT_DOWNLOAD_PATH}/{output_file}", url, "2>&1"]
        cmd = f"curl -o {self.DEFAULT_DOWNLOAD_PATH}/{output_file} {url} 2>&1"
        self._executor.run(cmd)
        


    def _wget(self, url: str, output_file: str):
        # cmd = ["wget", "-O", f"{self.DEFAULT_DOWNLOAD_PATH}/{output_file}", url, " 2>&1"]
        cmd = f"wget -O {self.DEFAULT_DOWNLOAD_PATH}/{output_file} {url} --progress=bar:force 2>&1"
        self._executor.run(cmd)


    def _urllib(self, url: str, output_file: str):
        # urllib.request.urlretrieve(url, save_path)    # simple download

        headers = {"User-Agent": "Mozilla/5.0"}
        # headers = None

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(f"{self.DEFAULT_DOWNLOAD_PATH}/{output_file}", "wb") as out_file:
            out_file.write(response.read())



if __name__ == '__main__':
    downloader = Downloader()
    # downloader._curl(url="https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.deb", output_file="wechat.deb")
    downloader._wget(url="https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.deb", output_file="wechat.deb")
    # downloader._urllib(url="https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.deb", output_file="wechat.deb")
