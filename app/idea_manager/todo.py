import datetime
from random import choice
from typing import Any, Dict, Final, Callable, Iterator

import click

from idea_manager.tools import load_json, add_hotkeys, clear_input, export_to_json

NO_LINE_FILE: Final[str] = "No this line in file"


class Model:
    def __init__(self, path: str, path_comp: str):
        self.path = path
        self.path_comp = path_comp

        self.data: dict = load_json(self.path)
        self.data_comp: dict = load_json(self.path_comp)
        self.max_ind: int = -1

    def new(self, do: str) -> None:
        self.data.update({self.max_ind + 1: do})
        export_to_json(self.path, self.data)

    def delete(self, ind: int) -> str:
        if ind in self.data:
            del_value = self.data.pop(ind)

            values = self.data.values()
            self.data = {i: val for i, val in enumerate(values)}

            self.max_ind = len(values)

            export_to_json(self.path, self.data)
            return del_value
        return NO_LINE_FILE

    def go_to_line(self, ind: int) -> str:
        return self.data.get(ind, NO_LINE_FILE)

    @property
    def count(self) -> str:
        return f"{self.max_ind + 1} TODOS not completed"

    def complete(self, ind: int) -> str:
        if ind in self.data:
            time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            self.data_comp.update({time: self.data[ind]})
            export_to_json(self.path_comp, self.data_comp)
            return self.delete(ind)
        return NO_LINE_FILE

    @property
    def read_comp(self) -> Iterator[str]:
        for time, val in self.data_comp.items():
            yield click.style(f"[{time}] ", fg="red") + val

    @property
    def random(self) -> Any:
        return self.data[choice(list(self.data))]


class View(BasicView):
    def show(self, self_conroller):
        click.clear()
        self_conroller.model.data = load_json(self_conroller.model.path)
        try:
            self_conroller.model.max_ind = max(
                map(int, self_conroller.model.data.keys()))
        except TypeError:
            pass
        except ValueError:
            click.echo("Empty! [Press 'Ctrl'+'N' to create new TODO]")
        else:
            for i, val in enumerate(self_conroller.model.data.values()):
                click.echo(click.style(f"[{i}] ", fg="red") + val)

    def print_pause(self, arg: Any):
        click.clear()
        click.echo(arg)
        clear_input()
        click.pause()

    def print_lst(self, it):
        click.clear()
        for st in it:
            click.echo(st)
        clear_input()
        click.pause()


def update_view(foo: Callable):
    def wrap(*args):
        click.clear()
        clear_input()
        foo(*args)
        Controller.show(args[0])

    return wrap


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    @staticmethod
    def show(self):
        self.view.show(self)

    @update_view
    def complete(self):
        ind = click.prompt("Enter line index")
        self.view.print_pause(self.model.complete(ind))

    @update_view
    def delete(self):
        ind = click.prompt("Enter line to delete index")
        self.view.print_pause(self.model.delete(ind))

    @update_view
    def new(self):
        do = click.prompt(f"[{self.model.max_ind + 1}] TODO")
        self.model.new(do)

    @update_view
    def go_to_line(self):
        ind = click.prompt("Enter line index")
        self.view.print_pause(self.model.go_to_line(ind))

    @update_view
    def read_comp(self):
        self.view.print_lst(self.model.read_comp)

    @update_view
    def count(self):
        self.view.print_pause(self.model.count)

    @update_view
    def random(self):
        self.view.print_pause(self.model.random)


# def help_keys():
#     click.clear()
#     dic_keys: dict = {
#         "ctrl + r": "reload window",
#         "ctrl + n": "New TODO",
#         "ctrl + b": "Count not completed TODO's",
#         "ctrl + d": "Delete TODO",
#         "ctrl + g": "Print info on input line",
#         "ctrl + x": "Complete TODO",
#         "ctrl + w": "Print completed TODO's",
#         "ctrl + h": "Help",
#         "ctrl + c": "Abort",
#         "esc": "Exit"
#     }
#     for key, do in dic_keys.items():
#         click.echo(f"{key}:\t{do}")
#     clear_input()
#     click.pause()


def main(path: str, path_comp: str) -> None:
    controller = Controller(Model(path, path_comp), View())
    Controller.show(controller)
    dic: Dict[str, Callable] = {
        "ctrl + s": lambda: Controller.show(controller),
        "ctrl + n": controller.new,
        "ctrl + b": controller.count,
        "ctrl + d": controller.delete,
        "ctrl + g": controller.go_to_line,
        "ctrl + x": controller.complete,
        "ctrl + w": controller.read_comp,
        "ctrl + r": controller.random
    }
    add_hotkeys(dic)
