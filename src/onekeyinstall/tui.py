from time import monotonic
import time
from textual.app import App, ComposeResult,Widget
from textual.widgets import Footer, Header, Static, ProgressBar, Label, ListView, ListItem
from textual.widgets._header import HeaderTitle
from textual.containers import Center, Vertical, Horizontal
from textual import events
from textual.widgets import RichLog
from textual.reactive import reactive



class OKIHeader(Header):


    def __init__(self):
        super().__init__()
        self.tall = True

    
    def compose(self):
        yield HeaderTitle()


    def _on_click(self, e):
        e.prevent_default() # 拒绝调用父类的事件处理



class OKIProgressBar(Widget):

    

    def __init__(self, pb_name: str="OP:"):
        super().__init__()
        self._pb_name = pb_name
        self._label = Label(self._pb_name, id="oki-pb-label")
        self._progress_bar = ProgressBar(id="oki-pb-pb")
        self.set_zero()


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


    def set_progress_rate(self, progress_rate: int) ->None:
        # pass
        self._progress_bar.update(progress=progress_rate)



class OKIListItem(Widget):


    def __init__(self) -> None:
        super().__init__()


    def compose(self):
        return super().compose()



class OKIListView(Widget):
    def __init__(self) -> None:
        super().__init__(id="oki-listview")
        self.styles.border = ("round", "#6c6c4f")
        self.border_title = "Optional Installation Items"
        self.styles.border_title_align = "center"
        # self.border_subtitle = "4456" # note 用来显示当前的层级


    def compose(self):
        self.list_view = ListView(
            ListItem(
                Horizontal(
                    Label("🍎 Apple", classes="name"),
                    Label("Price: $1", classes="price"),
                )
            ),
            ListItem(
                Horizontal(
                    Label("🍌 Banana", classes="name"),
                    Label("Price: $0.5", classes="price"),
                )
            ),
        )
        with Vertical(id="vertical_listview"):
            yield self.list_view
            # yield Label("Item A")




class OKIRichLog(Widget):
    def __init__(self) -> None:
        super().__init__(id="oki-richlog")
        self.styles.border = ("round", "#795453")
        self.border_title = "Detail Information"
        self.styles.border_title_align = "center"
        # self.border_subtitle = "4456"     # note 用来显示当前已经选中的安装项

    def compose(self):

        self._rich_log = RichLog(id="log")
        self._rich_log.styles.height = "1fr"
        self._rich_log.styles.overflow_y = "auto"
        self._progress_bar = OKIProgressBar()
        # self._progress_bar = ProgressBar()
        self._progress_bar.styles.height = "auto"
        with Vertical(id="vertical_log"):
            yield self._rich_log
            yield self._progress_bar
            # yield Label("Item 1")
    # 首行显示,当前正在执行的命令名称
    # 需要呼出交互
    # 确认交互内容


class OKIStatusBar(Widget):

    system_t = reactive(monotonic)

    def __init__(self):
        super().__init__(id="oki-status-bar")
        self.styles.border = ("round", "#5a6c5b")
        # self.border_title = f"{self.system_t}"
        self.border_title = f"System Status"
        self.styles.border_title_align = "center"
        # self.border_subtitle = "4456"
        # create timer
        self.timer = self.set_interval(1/60, self.update_sys_t, pause=False)
        # self.timer.resume()


    def update_sys_t(self):
        self.system_t = monotonic() # 更新该响应式数据时，会自动调用以watch开头的方法如 watch_system_t
        self.border_subtitle = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"


    def watch_system_t(self, t):
        pass



    def compose(self):
        # 动态显示时间
        # 显示什么系统和版本，什么架构
        # 
        yield Label("this is Label")
        yield Static("This is Static Text")

    


class OKITui(App):

    CSS_PATH = "/home/jay/00-CodeSpace/00-MySelf/03-one-key-install/src/onekeyinstall/tcss/tui.tcss"
    BINDINGS = [
        ("w", "select_up", "向上"),
        ("enter", "select_enter", "选择"),
        ("q", "quit", "退出"),
        ("left", "quit1", "退出1"),
        ("down", "quit2", "退出2"),
        ("right", "quit3", "退出3"),
        ("up", "quit4", "退出4"),
        ("s", "select_down", "向下"),
    ]

    TITLE = "One Key Install App"
    SUB_TITLE = "一件安装"


    def __init__(self):
        # super().__init__(driver_class, css_path, watch_css)
        super().__init__()
        # self.container_up = OKIStatusBar()    # 在这里进行实例化的话，会因为没有事件循环导致报错
        self.container_left = OKIListView()
        self.container_right = OKIRichLog()


    def compose(self) -> ComposeResult:
        # yield Header(icon="")
        yield OKIHeader()
        with Vertical(id="app-vertical"):
            yield OKIStatusBar()        # ? 如果进行实例化后
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
        self.query_one(RichLog).write(event)
        if event.key == "w":
            self.container_left.list_view.action_cursor_up()
            self.query_one(RichLog).write("wwww")
        elif event.key == "s":
            self.container_left.list_view.action_cursor_down()
            self.query_one(RichLog).write("sss")
        elif event.key == "enter":
            self.container_left.list_view.action_select_cursor()
            self.query_one(RichLog).write("enter")






if __name__ == "__main__":
    app = OKITui()
    app.run()