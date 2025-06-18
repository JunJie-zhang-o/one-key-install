import getpass
import sys
import time
from pathlib import Path
from time import monotonic

from textual import events, on
from textual.app import App, ComposeResult, Widget
from textual.binding import Binding
from textual.containers import Center, Grid, Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widgets import (Button, Footer, Header, Label, ListItem, ListView,
                             MarkdownViewer, ProgressBar, RichLog, Rule,
                             Static)
from textual.widgets._header import HeaderTitle

from onekeyinstall import _version
from onekeyinstall.installer import Installer
from onekeyinstall.registry import ToolRegistry
from onekeyinstall.utils import System, get_shell_executor


class OKIHeader(Header):

    def __init__(self):
        super().__init__()
        self.tall = True

    def compose(self):
        yield HeaderTitle()

    def _on_click(self, e):
        e.prevent_default()  # 拒绝调用父类的事件处理


class OKIProgressBar(Widget):

    def __init__(self, pb_name: str = "OP:"):
        super().__init__(id="oki-pb")
        self._pb_name = pb_name
        self._label = Label(self._pb_name, id="oki-pb-label")
        self._progress_bar = ProgressBar(total=100,id="oki-pb-pb")
        # self.set_zero()

    def compose(self) -> ComposeResult:

        with Horizontal(id="horizontal_pb"):
            yield self._label
            yield self._progress_bar

    def set_zero(self) -> None:
        self._progress_bar.update(progress=100, total=100)

    def set_total(self, total: int) -> None:
        self._progress_bar.total = total

    def set_indeterminate_state(self) -> None:
        pass

    def set_progress_rate(self, progress_rate: int) -> None:
        # pass
        self._progress_bar.update(progress=progress_rate)


class OKIListItem(ListItem):

    def __init__(self, index, name) -> None:
        super().__init__()
        self._show_index = index
        self._show_name = name

    def compose(self):
        with Horizontal():
            yield Label(" ")
            yield Label(str(self._show_index))
            yield Label(" ")
            yield Label(self._show_name)


class OKIListView(Widget):
    

    class Selected(Message):
        

        def __init__(self, installer:Installer):
            self._installer = installer
            super().__init__()


    current_selected = reactive("")

    def __init__(self) -> None:
        super().__init__(id="oki-listview")
        self.styles.border = ("round", "#6c6c4f")
        self.border_title = "Optional Installation Items"
        self.styles.border_title_align = "center"

        self._registry = ToolRegistry()._commands
        self._selected = ""


    def compose(self):
        self.list_view = ListView()
        with Vertical(id="vertical_listview"):
            yield self.list_view


    async def on_mount(self) -> None:
        await self.update_items(items=ToolRegistry.list())


    async def update_items(self, items=ToolRegistry.list()):
        self.list_view.clear()
        for index, value in enumerate(items):
            item = OKIListItem(index=index, name=value)
            await self.list_view.append(item)
        # 取消默认选中项
        self.list_view.index = None


    @on(ListView.Highlighted)
    def handle_index(self):
        # self.app.query_one(RichLog).write(str(self.list_view.index))
        if self.list_view.highlighted_child:
            self.current_selected = self.list_view.highlighted_child._show_name


    def watch_current_selected(self, current_selected: str) -> None:
        if self._selected != "":
            self.border_subtitle = f"{self._selected}.{current_selected}"  
        else:
            self.border_subtitle = f"{current_selected}"  
            

    async def on_key(self, event):
        # TODO 实际的逻辑应该OKI中去,不建议在这里进行处理
        if event.key in ["right", "d"]:
            if self.current_selected not in self._selected:
                self._selected += self.current_selected
                next_items = ToolRegistry.get(self._selected)
                if type(next_items) is dict:
                    await self.update_items(next_items)
        elif event.key in ["left", "a"]:
            if self._selected.find(".") == -1:
                self._selected = ""
                items = ToolRegistry.list()
            else:
                self._selected = self._selected[:self._selected.find(".", -1)-1]
                items = ToolRegistry.get(self._selected)
            self.current_selected = ""
            await self.update_items(items)
        
        elif event.key == "enter":
            
            _cls = ToolRegistry.get(f"{self._selected}.{self.current_selected}")
            def check_tip_screen_ret(ret):
                if ret:
                    # 启动安装
                    self.post_message(self.Selected(_cls))
            if _cls:
                self.app.push_screen(OKITipsScreen("123"), check_tip_screen_ret)

        


class OKIRichLog(Widget):
    
    DEFAULT_OKI_DESC_FILE_PATH = Path(__file__).parent.joinpath("res", "oki.md")

    def __init__(self) -> None:
        super().__init__(id="oki-richlog")
        self.can_focus = False
        self.styles.border = ("round", "#795453")
        self.border_title = "Detail Information"
        self.styles.border_title_align = "center"
        # self.border_subtitle = "4456"     # note 用来显示当前已经选中的安装项

    def compose(self):
        
        self._text = MarkdownViewer(Path(self.DEFAULT_OKI_DESC_FILE_PATH).read_text(), show_table_of_contents=False)
        self._rich_log = RichLog(id="log")
        self._rich_log.can_focus = False
        self._rich_log.styles.height = "1fr"
        self._rich_log.styles.overflow_y = "auto"
        self._progress_bar = OKIProgressBar()
        self._progress_bar.styles.height = "auto"
        self._title = Label()
        with Vertical(id="vertical_log"):
            yield self._text
            yield Rule()
            yield self._title
            yield self._rich_log
            yield self._progress_bar
            # yield Label("Item 1")

    # 首行显示,当前正在执行的命令名称
    # 需要呼出交互
    # 确认交互内容

    def set_description(self, text: str):
        self._text.render_str(text)

    
    def set_installer_name(self, name: str):
        self.border_subtitle = f"Install {name}"

    
    def set_title(self, title: str):
        self._title.update(title)


    def add_log(self, log: str):
        self._rich_log.write(log)

    
    def clear_log(self):
        self._rich_log.clear()

class OKIStatusBar(Widget):


    system_t = reactive(monotonic)

    def __init__(self):
        super().__init__(id="oki-status-bar")
        self.styles.border = ("round", "#5a6c5b")
        self.can_focus = False
        self.border_title = f"System Status"
        self.styles.border_title_align = "center"
        # create timer
        self.timer = self.set_interval(1 / 60, self.update_sys_t, pause=False)
        # self.timer.resume()

        self._system = System()

    def update_sys_t(self):
        self.system_t = monotonic()  # 更新该响应式数据时，会自动调用以watch开头的方法如 watch_system_t
        self.border_subtitle = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"

    def watch_system_t(self, t):
        pass

    def compose(self):
        yield Static(f"🖥️ OS:{self._system.os}")
        yield Static(f"🧬 Arch:{self._system.arch}")
        yield Static(f"🌍 Locale:{self._system.locale}")
        yield Static(f"📦 Distribution:{self._system.distribution}")
        yield Static(f"🧾 SysVersion:{self._system.version}")
        yield Static(f"💻 Shell:{get_shell_executor()}")
        yield Static(f"🛠️  SWVersion:{_version}")
        yield Static(f"🐍 Python:{sys.version}")
        yield Static(f"👤 User:{getpass.getuser()}")




# class OKITipsScreen(Screen):
class OKITipsScreen(ModalScreen[bool]):
    """Screen with a dialog to quit."""


    def __init__(self, tips: str = "", btn1_str: str = "Ensure", btn2_str: str = "Cancel"):
        super().__init__()
        self.tips, self.btn1_str, self.btn2_str = tips, btn1_str, btn2_str
        self.selected_button = 0  # 默认选择第一个按钮


    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.tips, id="question"),
            Button(self.btn1_str, variant="error", id="btn1"),
            Button(self.btn2_str, variant="primary", id="btn2"),
            id="tips-dialog",
        )

    def on_mount(self, event):
        self.query_one("#btn1").focus()
        self.query_one("#btn2").remove_class("focused")

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard events for button selection."""
        if event.key == "left":
            self.selected_button = 0
            self.update_button_selection()
        elif event.key == "right":
            self.selected_button = 1
            self.update_button_selection()
        elif event.key == "enter":
            if self.selected_button == 0:
                self.dismiss(True)          # dismiss will auto close TipsScreen
            elif self.selected_button == 1:
                self.dismiss(False)

    def update_button_selection(self):
        """Update button styles based on selected button."""
        btn1 = self.query_one("#btn1")
        btn2 = self.query_one("#btn2")

        if self.selected_button == 0:
            btn1.focus()
            btn2.remove_class("focused")
        else:
            btn2.focus()
            btn1.remove_class("focused")


class OKITui(App):

    CSS_PATH = Path(__file__).parent.joinpath("tcss", "tui.tcss")

    # 这个顺序最好是按照上下左右顺序+字母键的顺序，主要是和footer的显示有关系
    BINDINGS = [
        # Binding("up",    "select_up",     "Up",           show=True, priority=True),      # note:设置priority 优先显示再footer中,并且顺序按照先其他按钮再字母按钮
        Binding("enter", "select_enter",  "Ensure",       show=True, priority=True),
        Binding("w",     "select_up1",    "Up",           show=True, priority=True),
        # Binding("down",  "select_down",   "Down",         show=True, priority=True),
        Binding("a",     "select_left1",  "Parent level", show=True, priority=True),
        Binding("s",     "select_down1",  "Down",         show=True, priority=True),
        # Binding("left",  "select_left",   "Parent level", show=True, priority=True),
        # Binding("right", "select_right",  "Child level",  show=True, priority=True),
        Binding("d",     "select_right1", "Child level",  show=True, priority=True),
        Binding("q",     "quit",          "Quit",         show=True, priority=True),
    ]

    TITLE = "Ooone Key Install App"
    SUB_TITLE = "一键安装"

    def __init__(self):
        super().__init__()
        # self.container_up = OKIStatusBar()    # 在这里进行实例化的话，会因为没有事件循环导致报错
        self.container_left = OKIListView()
        self.container_right = OKIRichLog()

    def compose(self) -> ComposeResult:
        yield OKIHeader()
        with Vertical(id="app-vertical"):
            yield OKIStatusBar()  # ? 如果进行实例化后
            with Horizontal(id="app-horizontal"):
                yield self.container_left
                yield self.container_right
        yield Footer()

    def action_quit(self) -> None:
        self.exit()

    def on_mount(self) -> None:
        # self.screen.styles.background = "darkblue"
        # self.screen.styles.border
        # self.widget1.styles.height = "2fr"    # 通过使用fr进行区域的总等分
        # 可以通过设置达到设置带title的box
        # self.widget.border_title = "Litany Against Fear"
        # self.widget.border_subtitle = "by Frank Herbert, in “Dune”"
        # self.widget.styles.border_title_align = "center"
        pass

    def on_key(self, event: events.Key) -> None:
        # 键盘事件响应
        # print(self.app_focus)
        # self.query_one(RichLog).write(self.app_focus)
        # self.query_one(RichLog).write(event)
        if event.key in ["w", "up"]:
            pass
        elif event.key in ["s", "down"]:
            pass
        elif event.key == "enter":
            pass
        elif event.key == "c":
            self.query_one(RichLog).write("")
            self.query_one(RichLog).clear()
        elif event.key == "u":
            self.query_one(ProgressBar).advance()


    @on(OKIListView.Selected)
    def handle_installer(self, message:OKIListView.Selected) -> None:
        self.query_one(RichLog).write(f"Message:{message._installer}")
        installer = message._installer()

        # pre install

        # install 
        self.container_right.set_installer_name(installer.PACKAGE_NAME)
        for k, v in installer._install.commands.items():
            self.container_right.set_title(k)
            time.sleep(1)
        pass


if __name__ == "__main__":
    app = OKITui()
    app.run()
