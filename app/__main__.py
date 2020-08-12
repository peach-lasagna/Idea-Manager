import click

from idea_manager import idea_main, todo_main

schema_json_path = "./db/idea_schema.json"
data_json_path = "./db/idea.json"
completed_json_path = "./db/idea_comp.json"
todo_path = "./db/todo.json"
todo_comp_path = "./db/todo_comp.json"


@click.group()
def cli():
    """Tools for planning."""
    pass


# cls_idea = IdeaView(
#     IdeaModel(data_json_path, schema_json_path,
#               completed_json_path)
# )


# @cli.command(name="new", help="Create new idea")
# @click.argument("idea")
# def new_idea(idea: str) -> None:
#     cls_idea.new_idea(idea)


# @cli.command(name="read", help="Read idea")
# @click.argument("idea")
# def read_idea(idea: str) -> None:
#     cls_idea.read_idea(idea)


# @cli.command(name="list", help="List of ideas")
# def idea_list() -> None:
#     cls_idea.list_idea()


# @cli.command(name="remove", help="Remove idea")
# @click.argument("idea")
# @click.confirmation_option(prompt="Are you sure you want to drop this idea?")
# def remove_idea(idea: str) -> None:
#     cls_idea.rem_idea(idea)


# @cli.command(name="complete", help="Complete idea")
# @click.argument("idea")
# def complete_idea(idea: str) -> None:
#     cls_idea.comp_idea(idea)


# @cli.command(name="read_comp", help="Read complete idea")
# @click.argument("idea")
# def read_comp_idea(idea: str) -> None:
#     cls_idea.read_comp_idea(idea)


# @cli.command(name="list_comp", help="List of complete ideas")
# def comp_idea_list() -> None:
#     cls_idea.comp_idea_list()


@cli.command(name="idea", help="Idea manager")
def idea():
    idea_main()


@cli.command(name="todo", help="Todo manager")
def todo() -> None:
    todo_main(todo_path, todo_comp_path)


if __name__ == "__main__":
    try:
        cli()
    except click.exceptions.Abort:
        pass
    except EOFError:
        pass
