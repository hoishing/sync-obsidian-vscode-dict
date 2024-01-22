#!/usr/bin/env python3
"""
sync vscode cspell dictionary with obsidian dictionary
usage: python3 sync-dict.py to-code|to-obsidian
"""

import hashlib, sys

CODE_DICT = "/Users/shing/google/settings/watchman/dictionary.txt"
OBSIDIAN_DICT = (
    "/Users/shing/Library/Application Support/obsidian/Custom Dictionary.txt"
)


def is_identical() -> bool:
    """check if vscode and obsidian dictionaries are identical"""
    with open(CODE_DICT, "r") as file:
        code_set = set(file.readlines())
    with open(OBSIDIAN_DICT, "r") as file:
        obsidian_set = set(file.readlines()[:-1])
    return code_set == obsidian_set


def to_obsidian() -> None:
    """process vscode dict to obsidian"""
    if is_identical():
        return

    with open(CODE_DICT, "r") as file:
        lines = file.readlines()
        # sort alphabetically, but keep uppercase words first
        sorted_lines = sorted(lines, key=lambda line: (not line[0].isupper(), line))
        sorted_txt = "".join(sorted_lines)
        checksum = hashlib.md5(sorted_txt.encode()).hexdigest()
        obsidian_dict_text = sorted_txt + "checksum_v1 = " + checksum

    with open(OBSIDIAN_DICT, "w") as file:
        file.write(obsidian_dict_text)


def to_code() -> None:
    """copy obsidian dict to vscode after removing checksum"""
    if is_identical():
        return

    with open(OBSIDIAN_DICT, "r") as file:
        lines = file.readlines()
        # remove last line (checksum)
        obsidian_text = "".join(lines[:-1])

    with open(CODE_DICT, "w") as file:
        file.write(obsidian_text)


# get first argument
arg = sys.argv[1]

# call function with name of first argument
eval(f"{arg}()")
