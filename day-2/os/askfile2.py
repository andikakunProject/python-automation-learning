import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import textwrap


# ============================================================
# Helpers
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def wrap(text, width=40, indent=0, space=0):
    prefix = "\t" * indent + " " * space
    return ("\n" + prefix).join(textwrap.wrap(text, width))


def shorten(text, length, dots=3):
    return text if len(text) <= length else text[: length - dots] + "." * dots


def pad(text, width):
    return text + " " * max(0, width - len(text))


def unitsize(size: float) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"


# ============================================================
# Models
# ============================================================

class SelectMode(Enum):
    FILE = "file"
    DIR = "dir"


@dataclass
class Entry:
    path: Path
    is_dir: bool
    stat: os.stat_result

    @property
    def name(self):
        return self.path.name

    @property
    def stem(self):
        return self.path.stem

    @property
    def type_label(self):
        return "dir" if self.is_dir else (self.path.suffix[1:] or "file")


# ============================================================
# Rendering
# ============================================================

def get_entries(cur_path: Path, ext: tuple[str] | None) -> list[Entry]:
    """
    Read directory and return filtered Entry list.
    Directories are always included.
    """
    entries: list[Entry] = []

    for p in sorted(cur_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        try:
            stat = p.stat()
        except PermissionError:
            continue

        entry = Entry(p, p.is_dir(), stat)

        if ext is None or entry.is_dir or entry.type_label in ext:
            entries.append(entry)

    return entries


def render_directory(cur_path: Path, title: str, entries: list[Entry]):
    width = 77
    clear()

    print("=" * width)
    print(title.center(width))
    print("=" * width)

    print(f"current directory : {cur_path.name}")
    print(f"path              : {wrap(str(cur_path), 58, indent=2, space=3)}\n")

    print("Index | Name                    | Type | Size       | Last Modified")
    print("-" * width)

    total_size = 0

    for idx, entry in enumerate(entries, start=1):
        size = " " * 10 if entry.is_dir else unitsize(entry.stat.st_size)
        if not entry.is_dir:
            total_size += entry.stat.st_size

        print(
            f"{idx:5} | "
            f"{pad(shorten(entry.stem, 22),22)}  | "
            f"{pad(entry.type_label,4)} | "
            f"{pad(size,10)} | "
            f"{datetime.fromtimestamp(entry.stat.st_mtime)}"
        )

    print(f"\ntotal file size : {unitsize(total_size)}")


# ============================================================
# Core logic
# ============================================================

def ask_path(mode: SelectMode, ext: tuple[str] | None = None) -> Path | None:
    """
    Interactive filesystem selector.

    Commands:
      :q / :quit / :exit     -> quit
      :sel <target>          -> explicitly select directory
      :: <name>              -> escape literal names
    """

    if mode.value == 'dir':
        ext = None
    
    cur_path = Path.cwd()
    ext = None if ext is None else tuple([e.lower() for e in ext])

    while True:
        entries = get_entries(cur_path, ext)
        render_directory(cur_path, f"select a {mode.value}", entries)

        prompt = (
            'type "..", ".", index or name (":q" to quit): '
            if mode is SelectMode.FILE
            else 'type ":sel <index or name>" to select directory (":q" to quit): '
        )

        print(f'select a {(str(ext) + " file" if ext else " any file") if mode.value is "file" else "directory"}')

        raw = input(f"\n{prompt}").strip()
        select = False

        # ---- escape literal names
        if raw.startswith(":: "):
            raw = raw[3:].strip()

        # ---- command parsing
        elif raw.startswith(":"):
            parts = raw[1:].split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if cmd in ("q", "quit", "exit"):
                return None

            if cmd in ("sel", "select"):
                select = True
                raw = arg

        # ---- navigation
        if raw in (".", ".."):
            cur_path = (cur_path / raw).resolve()
            if select:
                return cur_path
            continue

        # ---- index selection
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(entries):
                entry = entries[idx]
                if entry.is_dir:
                    if mode is SelectMode.DIR and select:
                        return entry.path
                    cur_path = entry.path
                elif mode is SelectMode.FILE:
                    return entry.path
            continue

        # ---- name selection
        for entry in entries:
            if raw in (entry.name, entry.stem):
                if entry.is_dir:
                    if mode is SelectMode.DIR and select:
                        return entry.path
                    cur_path = entry.path
                elif mode is SelectMode.FILE:
                    return entry.path
                break


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    path = ask_path(SelectMode.DIR, ("py", "txt"))
    print("\nselected_path:", path)
