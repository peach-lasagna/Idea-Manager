import json
from typing import Iterator, Optional
from dataclasses import dataclass

import click


def load_json(path: str) -> dict:
    """Get json schema to format from file.

    Args:
        path(str): path to json.
    Returns:
        (dict): db.

    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


class Ideas:
    """Class to operations with db."""
    
    def __init__(self, data_path: str, schema_path: str, completed_path: str):
        self.data_path = data_path
        self.schema_path = schema_path
        self.completed_path = completed_path
        
        self.data: dict = load_json(self.data_path)
        self.schema: dict = load_json(self.schema_path)
        self.completed: dict = load_json(self.completed_path)

    def read_idea(self, block: str, data: Optional[dict] = None) -> Iterator[str]:
        """Read db from json.

        Args:
            block(str): idea name.
            data(Optional[dict]): db to check in.

        Returns:
            (Iterator[str]): str with key and value from db[block]

        """
        if data is None:
            data = self.data

        if block not in data:
            click.echo("No this idea in list!")
        else:
            for key, val in data[block].items():
                yield f"{key}: {val}"

    def list_idea(self, data: Optional[dict] = None) -> Iterator[str]:
        """Read ideas from .json.

        Args:
            data(Optional[dict]): dict with ideas.

        Returns:
            (Iterator[str]): str with key and value from db[block]

        """
        if data is None:
            data = self.data

        if not data:
            click.echo("No ideas yet!")

        yield from data

    def export_data(
        self, path: Optional[str] = None, data: Optional[dict] = None
    ) -> None:
        """Export data to .json file.

        Args:
            path(Optional[str]): path to json file.
            data(Optional[dict]): db to write.

        """
        if path is None:
            path = self.data_path
        if data is None:
            data = self.data

        with open(path, "w", encoding="utf-8") as wri:
            json.dump(data, wri, indent=2)

    def write_idea(self, name: str,) -> None:
        """Update db in .json file.

        Args:
            name(str): name to idea.

        """

        def input_data() -> Optional[dict]:
            """Input idea.

            Returns:
                (dict): completed db.

            """
            if name in self.data and not click.confirm(
                "This idea already in list. Rewrite?"
            ):
                return

            for key, val in self.schema.items():
                new_value = click.prompt(f"{key}", val)
                if new_value:
                    if type(val) != str:
                        new_value = eval(new_value)
                    self.schema[key] = new_value
            return self.schema

        if inp := input_data():
            self.data.update({name: inp})
        self.export_data()

    def rem_idea(self, name: str) -> str:
        """Remove idea from db.

        Args:
            name(str): name of idea.

        Returns:
            (str): Result of operation.

        """
        if name in self.data:
            del self.data[name]
            self.export_data()
            return "Complete!"
        else:
            return "No this idea in list."

    def comp_idea(self, name: str) -> str:
        if name not in self.data:
            return "No this idea in list."
        else:
            dic = self.data.pop(name)
            self.export_data()
            self.completed.update({name: dic})
            self.export_data(self.completed_path, self.completed)
            return "Complete!"
