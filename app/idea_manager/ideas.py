from typing import Dict, Callable, Iterator, Optional

import click

from idea_manager.tools import load_json, add_hotkeys, export_to_json
from idea_manager.exceptions import NotFoundIdeaError


class IdeaModel:
    """Class to operations with db."""

    def __init__(self, data_path: str, schema_path: str, completed_path: str):
        self.data_path = data_path
        self.schema_path = schema_path
        self.completed_path = completed_path

        self.data: dict = load_json(self.data_path)
        self.schema: dict = load_json(self.schema_path)
        self.completed: dict = load_json(self.completed_path)

    def export_data(self):
        export_to_json(self.data_path, self.data)

    def input_data(self, inp_func: Callable = click.prompt) -> dict:
        for key, val in self.schema.items():
            new_value = inp_func(f"{key}", val)

            if new_value:
                if type(val) != str:
                    new_value = eval(str(new_value))
                self.schema[key] = new_value
        return self.schema

    def read_idea(self, name: str, data: Optional[dict] = None) -> Iterator[str]:
        if data is None:
            data = self.data

        if name not in data:
            raise NotFoundIdeaError("No this idea in file!")

        for key, val in data[name].items():
            yield f"{key}:\t{val}"

    def list_idea(self, data: Optional[dict] = None) -> Iterator[str]:
        if data is None:
            data = self.data

        if not data:
            raise NotFoundIdeaError("No ideas yet!")

        yield from data

    def write_idea(self, name: str) -> None:
        self.data.update({name: self.input_data()})
        self.export_data()

    def rem_idea(self, name: str) -> str:
        if name in self.data:
            del self.data[name]
            self.export_data()
            return "Complete!"
        return "No this idea in list."

    def comp_idea(self, name: str) -> str:
        if name in self.data:
            dic = self.data.pop(name)
            self.export_data()

            self.completed.update({name: dic})
            export_to_json(self.completed_path, self.completed)
            return "Complete!"
        return "No this idea in list."


def try_exc(foo: Callable, exc=NotFoundIdeaError):
    def wrap(*args):
        try:
            foo(*args)
        except exc as e:
            click.echo(e.text)
    return wrap


class IdeaView(BasicView):
    # def __init__(self, model: IdeaModel):
    #     self.model = model

    # @try_exc
    # def read_idea(self, idea: str):
    #     for st in self.model.read_idea(idea):
    #         click.echo(st)

    # @try_exc
    # def list_idea(self):
    #     for st in self.model.list_idea():
    #         click.echo("[ ]\t" + st)

    # def rem_idea(self, idea: str):
    #     click.echo(self.model.rem_idea(idea))

    # def comp_idea(self, idea: str) -> None:
    #     click.echo(self.model.comp_idea(idea))

    # @try_exc
    # def read_comp_idea(self, idea: str):
    #     for st in self.model.read_idea(idea, self.model.completed):
    #         click.echo(st)

    # @try_exc
    # def comp_idea_list(self):
    #     for st in self.model.list_idea(self.model.completed):
    #         click.echo("[+] " + st)

    # def new_idea(self, idea: str):
    #     if idea in self.model.data and not click.confirm(
    #             "This idea already in list. Rewrite?"):
    #         return
    #     self.model.write_idea(idea)


class Controller:
    def __init__(self, model: IdeaModel, view: IdeaView) -> None:
        self.model = model
        self.view = view

    def show(self):
        pass

    def new(self):
        pass

    def count():
        pass


def main(data_json_path: str, schema_json_path: str, completed_json_path: str):
    model = IdeaModel(data_json_path, schema_json_path, completed_json_path)
    controller = Controller(model, IdeaView())

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
