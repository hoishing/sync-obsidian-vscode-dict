#!/usr/bin/python3
"""sync vscode cspell dictionary with obsidian dictionary"""

import hashlib
import logging
from pathlib import Path

base_folder = "/Users/kng/Documents/settings/sync_dict"
code_dict = Path(f"{base_folder}/dictionary.txt")
obsidian_dict = Path(
    "/Users/kng/Library/Application Support/obsidian/Custom Dictionary.txt"
)

logging.basicConfig(
    level=logging.INFO,  # minimum severity level: DEBUG < INFO < WARNING < ERROR < CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=f"{base_folder}/sync_dict.log",
    filemode="a",  # a: append; w: overwrite
)


def is_identical() -> bool:
    """check if vscode and obsidian dictionaries are identical"""
    code_set = set(code_dict.read_text().splitlines())
    obsidian_set = set(obsidian_dict.read_text().splitlines()[:-1])
    return code_set == obsidian_set


def is_code_dict_newer() -> bool:
    """check if vscode dictionary is newer than obsidian dictionary"""
    code_mtime = code_dict.stat().st_mtime_ns
    obsidian_mtime = obsidian_dict.stat().st_mtime_ns
    return code_mtime > obsidian_mtime


def to_obsidian() -> None:
    """process vscode dict to obsidian"""
    code_lines = code_dict.read_text().splitlines()
    sorted_lines = sorted(code_lines, key=lambda line: (not line[0].isupper(), line))
    sorted_txt = "\n".join(sorted_lines)
    checksum = hashlib.md5(sorted_txt.encode()).hexdigest()
    obsidian_dict_content = sorted_txt + "checksum_v1 = " + checksum
    obsidian_dict.write_text(obsidian_dict_content)

    logging.info("to_obsidian")


def to_vscode() -> None:
    """copy obsidian dict to vscode after removing checksum"""
    obsidian_lines = obsidian_dict.read_text().splitlines()[:-1]
    code_dict.write_text("\n".join(obsidian_lines))

    logging.info("to_vscode")


if __name__ == "__main__":
    logging.debug("start")
    if not is_identical():
        if is_code_dict_newer():
            to_obsidian()
        else:
            to_vscode()
    logging.debug("end")
