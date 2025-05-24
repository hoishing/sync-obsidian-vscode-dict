# Sync Spell-Checker Dictionary Between Obsidian and VSCode

 Given that both VSCode and Obsidian spell-checker dictionary are text files, linking them should be straightforward. Later I found that its much more complicated then I thought.

## The Problem

Obsidian's built-in spell checker has special requirement for its dictionary file:

- The words must be arranged in alphabetical order, with the uppercase come before the lowercase ones.
- The final line should be a checksum of all the words.
- VSCode cspell dictionary has no special requirements, but won't need a checksum at the end of file.

## The Idea

- need a mechanism to watch both dictionary files
- when one file change, trigger the update of other one
- conform to both obsidian and vscode dictionary file format during update
- avoid infinite update cycles, as one file change will trigger the update of the other

## The Solution

- use macOS built-in launchd to watch for file changes
- them run a python script to:
    - create new dictionary files when when the other updated
    - conform to required dictionary file format
    - append / remove checksum if needed
    - stop the update cycle when both dictionaries are the same
    - create logs for each update cycle

## How

- put `sync2obsidian.plist` in `~/Library/LaunchAgents` to add a login service for files monitoring
- `chmod 666` to both dictionary files
- `chmod +x sync_dict.py`
- grant *full disk access* to the system python `/usr/bin/python3`
- change your own path in `sync_dict.py` and `sync2obsidian.plist`

After that all set, adding word in Obsidian will trigger the update of VSCode dict, and vice versa 🎉

## Questions?

Open a [github issue] or ping me on [LinkedIn]

[github issue]: https://github.com/hoishing/sync-obsidian-vscode-dict/issues
[LinkedIn]: https://www.linkedin.com/in/kng2
