from os import environ as env

import click
from dotenv import find_dotenv, load_dotenv

from idea_manager import Ideas, todo_main

load_dotenv(find_dotenv())

cls_idea = Ideas(
    env["data_json_path"], env["schema_json_path"], env["completed_json_path"]
)


@click.group()
def cli():
    pass


@cli.command(name="new", help="Create new idea")
@click.argument("idea")
def new_idea(idea: str) -> None:
    cls_idea.write_idea(idea)


@cli.command(name="read", help="Read idea")
@click.argument("idea")
def read_idea(idea: str) -> None:
    for st in cls_idea.read_idea(idea):
        click.echo(st)


@cli.command(name="list", help="List of ideas")
def idea_list() -> None:
    for st in cls_idea.list_idea():
        click.echo("[ ] " + st)


@cli.command(name="remove", help="Remove idea")
@click.argument("idea")
@click.confirmation_option(prompt="Are you sure you want to drop this idea?")
def remove_idea(idea: str) -> None:
    click.echo(cls_idea.rem_idea(idea))


@cli.command(name="complete", help="Complete idea")
@click.argument("idea")
def complete_idea(idea: str) -> None:
    click.echo(cls_idea.comp_idea(idea))


@cli.command(name="read_comp", help="Read complete idea")
@click.argument("idea")
def read_comp_idea(idea: str) -> None:
    for st in cls_idea.read_idea(idea, cls_idea.completed):
        click.echo(st)


@cli.command(name="list_comp", help="List of complete ideas")
def comp_idea_list() -> None:
    for st in cls_idea.list_idea():
        click.echo("[ ] " + st)


@cli.command(name="todo", help="Todo list")
def todo() -> None:
    todo_main(env["todo_path"], env["todo_comp_path"])


if __name__ == "__main__":
    cli()
