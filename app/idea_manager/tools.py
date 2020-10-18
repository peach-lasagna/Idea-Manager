import json
from msvcrt import getch, kbhit
from typing import Dict, Callable

import keyboard


def add_hotkeys(hotkeys: Dict[str, Callable]) -> None:
    """Add hotkeys to programm.

    Args:
        hotkeys (Dict[str, Callable]): Dict with key to
    """
    for key, func in hotkeys.items():
        keyboard.add_hotkey(key, func)
    keyboard.wait("esc")


def clear_input():
    """Clear input."""
    while kbhit():
        getch()


def export_to_json(path: str, data: dict) -> None:
    """Export data to .json format file.

    Args:
        path (str): path to file.json
        data (dict): data to export

    """
    with open(path, "w", encoding="utf-8") as wri:
        json.dump(data, wri, indent=2)


def load_json(path: str) -> dict:
    """Get json schema to format from file.

    Args:
        path(str): path to json.

    Returns:
        (dict): db.

    """
    with open(path, encoding="utf-8") as file:
        return json.load(file)
