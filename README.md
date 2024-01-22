# Sync Spell Checking Dictionary Between Obsidian and VSCode

As someone who frequently uses both VSCode and Obsidian, I find it crucial to synchronize the spell checking dictionaries of both applications. This avoids the redundant task of adding the same word to each app's dictionary.

Initially, I assumed that linking the dictionary files of both apps would be straightforward, given that they are text files containing one word per line. However, I discovered that Obsidian's built-in spell checker has specific criteria for its dictionary file:

- The words must be arranged in alphabetical order.
- Words in uppercase should be listed before lowercase ones.
- The final line should be a checksum of all the words.

Failing to adhere to these requirements results in Obsidian's spell checker malfunctioning. To address this, I devised a solution using watchman and python. The process is as follows:

- Use watchman to monitor the spell checking dictionary files in both Obsidian and VSCode.
- When a modification is detected in one of the dictionary files, trigger a python script ([sync-dict.py]) that generates the dictionary file for the other application.
- The python script terminates if it finds that the entries in both dictionaries are identical, preventing an endless loop of triggers.

## watchman setup

First we need to create trigger config files for both vscode and obsidian dictionary folder.

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

[sync-dict.py]: https://github.com/hoishing/sync-obsidian-vscode-dict/blob/main/sync-dict.py
