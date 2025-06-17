
# deprerate 与键盘和鼠标交互不方便,暂时不用
from datetime import datetime
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from rich.table import Table


class OKIConsole:



    def __init__(self) -> None:
        
        
        self.layout = self._layout()
        self.layout["title"].update(self._header())




    def _header(self):
        table = Text("One Key Install", justify="center", style="bold blue", tab_size=2)
        # table = Table()
        # table.add_column("One Key Install", justify="center")
        grid = Table.grid(expand=True)
        # grid.add_column(justify="center")
        # grid.add_column(justify="right")
        grid.add_row(
            # "[b]One Key Install[/b]",
            Text("One Key Install", justify="center", style="bold blue", tab_size=2),
            # datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        grid.add_row(
            # "12",
            Text(datetime.now().ctime().replace(":", "[blink]:[/]"),justify="right")

        )
        return grid
    

    def _layout(self):
        layout = Layout(name="root")

        layout.split(
            Layout(name="title", ratio=1),
            Layout(name="Option", ratio=3),
            Layout(name="Output", ratio=3)
        )
        layout["Option"].split_row(
            Layout(name="op", ratio=3),
            Layout(name="Description", ratio=2),
        )
        return layout


layout = Layout()

layout.split_column(
    Layout(name="title", ratio=1),
    Layout(name="Option", ratio=2),
    Layout(name="Output", ratio=3)
)
layout["Option"].split_row(
    Layout(name="op"),
    Layout(name="Description"),
)
# layout["right"].split(
#     Layout(Panel("Hello")),
#     Layout(Panel("World!"))
# )

layout["title"].update(Panel(OKIConsole()._header(), style="white on blue"))

print(layout)   
input()
# print(layout.tree)   