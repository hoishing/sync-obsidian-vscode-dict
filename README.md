# Sync Spell Checking Dictionary Between Obsidian and VSCode

As a heavy user of both VSCode and Obsidian, keeping the spell checking dictionary in sync between two apps is essential to avoid duplicated effort of adding the same word in both apps.

I originally think its just a simple task by symbolic linking two dictionary files, as both are pure text with one word per line.

Later I found that Obsidian built-in spell checker has some specific requirements for its dictionary file:

- it need to be sorted alphabetically
- upper case words come first
- last line must be a checksum of all words

If we don't follow these rules the spell checker in Obsidian won't work, so I come up with a `watchman` + `python`  solution to tackle the problem. Logic as follow:

- watch both Obsidian and VSCode spell checking dictionary file with `watchman`
- trigger a python script(`sync-dict.py`) to create dictionary file of the other app when one of the dict file is modified.
- the python script will exit if both dictionaries entries are the same, avoid infinite trigger

## watchman setup

First we need to create trigger config file for both the vscode and obsidian dictionary folder.

- Obsidian trigger config

```json
[
  "trigger",
  "/path/to/Library/Application\ Support/obsidian",
  {
    "name": "sync-to-google",
    "expression": ["pcre", ".*Dictionary\\.txt$"],
    "command": [
      "/path/to/sync-dict.py",
      "to_code"
    ]
  }
]
```

- VSCode trigger config

```json
[
  "trigger",
  "/path/to/vscode/dict/folder",
  {
    "name": "sync-to-obsidian",
    "expression": ["pcre", ".*dictionary\\.txt$"],
    "command": [
      "/path/to/sync-dict.py",
      "to_obsidian"
    ]
  }
]
```

Then install `watchman` CLI and watch the specific folders.

```shell
# install watchman
brew install watchman

# obsidian setup
cd ~/Library/Application\ Support/obsidian/
watchman watch .
watchman -j < /path/to/obsidian/trigger/config

# vscode setup
cd /path/to/vscode/dict/folder
watchman watch .
watchman -j < /path/to/vscode/trigger/config
```

Note that macOS may ask for folder access permission on the first run, also watchman will add a login item for starting the watch daemon during login.

After that all set, adding word in Obsidian will trigger the update of VSCode dict, and vice versa 🎉
