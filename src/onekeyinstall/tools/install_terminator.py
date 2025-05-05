from onekeyinstall.installer import Installer
from onekeyinstall.registry import ToolRegistry



from onekeyinstall.registry import register



@register("terminal.terminator")
class InstallTerminator(Installer):
    
    PACKAGE_NAME = "terminator"


# todo:配置文件的更新
# todo:字体的依赖安装