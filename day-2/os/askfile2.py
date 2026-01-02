import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import textwrap


# ============================================================
# Helper functions
# ============================================================

def clear():
    """
    Clear the terminal screen (Windows or Unix-like systems).
    """
    os.system("cls" if os.name == "nt" else "clear")


def wrap(text, width=40, indent=0, space=0):
    """
    Wrap long text into multiple lines with optional indentation.
    Used to nicely display long paths.
    """
    prefix = "\t" * indent + " " * space
    return ("\n" + prefix).join(textwrap.wrap(text, width))


def shorten(text, length, dots=3):
    """
    Shorten a string and add dots if it exceeds a given length.
    """
    return text if len(text) <= length else text[: length - dots] + "." * dots


def pad(text, width):
    """
    Pad text with spaces on the right to align columns.
    """
    return text + " " * max(0, width - len(text))


def unitsize(size: float) -> str:
    """
    Convert a byte size into a human-readable string.
    Example: 1024 -> 1.00 KB
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"


# ============================================================
# Models / data structures
# ============================================================

class SelectMode(Enum):
    """
    Selection mode for the path selector.
    """
    FILE = "file"
    DIR = "dir"


@dataclass
class Entry:
    """
    Represents a file or directory entry in the current directory.
    """
    path: Path
    is_dir: bool
    stat: os.stat_result

    @property
    def name(self):
        """Full name including extension."""
        return self.path.name

    @property
    def stem(self):
        """Name without extension."""
        return self.path.stem

    @property
    def type_label(self):
        """Return 'dir' or file extension for display."""
        if self.is_dir:
            return "dir"
        return self.path.suffix[1:] or "file"


# ============================================================
# UI rendering
# ============================================================

def render_directory(cur_path: Path, title: str) -> list[Entry]:
    """
    Render the directory listing UI and return Entry objects
    for all files and directories in the current path.
    """
    width = 77
    clear()

    header = (
        "=" * width
        + "\n"
        + f"{title.center(width)}"
        + "\n"
        + "=" * width
    )

    print(header)
    print(f"current directory : {cur_path.name}")
    print(f"path             : {wrap(str(cur_path), 58, indent=2, space=3)}\n")

    print("Index | Name                    | Type | Size       | Last Modified")
    print("-" * width)

    entries: list[Entry] = []
    total_size = 0

    # Sort directories first, then files, alphabetically
    for idx, p in enumerate(
        sorted(cur_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())),
        start=1,
    ):
        entry = Entry(p, p.is_dir(), p.stat())
        entries.append(entry)

        size = " " * 10 if entry.is_dir else unitsize(entry.stat.st_size)
        total_size += entry.stat.st_size

        print(
            f"{shorten(str(idx),5):5} | "
            f"{pad(shorten(entry.stem, 22),22)} | "
            f"{pad(entry.type_label,4)} | "
            f"{pad(size,10)} | "
            f"{datetime.fromtimestamp(entry.stat.st_mtime)}"
        )

    print(f"\ntotal size : {unitsize(total_size)}")
    return entries


# ============================================================
# Core selection logic
# ============================================================

def ask_path(mode: SelectMode) -> Path | None:
    """
    Interactive path selector.
    - FILE mode: select a file
    - DIR mode: select a directory
    """
    cur_path = Path.cwd()

    while True:
        entries = render_directory(
            cur_path,
            f"select a {mode.value}"
        )

        # Prompt message depends on selection mode
        message = {
            "file": 'type "..", ".", index or name (":q" to quit): ',
            "dir":  'type ":sel <index, or name of directory> to select (":q" to quit): '
        }

        raw = input(f"\n{message[mode.value]}").strip()

        # ----------------------------------------------------
        # Command parsing
        # ----------------------------------------------------
        select = False
        token = raw.split()

        if raw.startswith(":"):
            cmd = token[0][1:].lower()

            if cmd in ("q", "quit", "exit"):
                return None

            if cmd in ("sel", "select"):
                select = True
                raw = raw[len(token[0]):].strip()

            if raw.startswith(":: "):
                raw = raw[3:].strip()

        # ----------------------------------------------------
        # Index-based selection
        # ----------------------------------------------------
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(entries):
                entry = entries[idx]
                if entry.is_dir:
                    if mode == SelectMode.DIR:
                        return entry.path
                    cur_path = entry.path
                elif mode == SelectMode.FILE:
                    return entry.path
            continue

        # ----------------------------------------------------
        # Navigation (current / parent directory)
        # ----------------------------------------------------
        if raw in (".", ".."):
            cur_path = (cur_path / raw).resolve()
            continue

        # ----------------------------------------------------
        # Name-based selection
        # ----------------------------------------------------
        for entry in entries:
            if raw in (entry.name, entry.stem):
                if entry.is_dir:
                    if mode == SelectMode.DIR:
                        if select:
                            return entry.path
                    cur_path = entry.path
                elif mode == SelectMode.FILE:
                    return entry.path
                break


# ============================================================
# Program entry point
# ============================================================

if __name__ == "__main__":
    path = ask_path(SelectMode.DIR)
    print("\nselected_path:", path)

