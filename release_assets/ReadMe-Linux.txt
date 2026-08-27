EDOPro HD Cards Downloader for Linux
========================

What it does
------------
Downloads the missing HD card artwork for EDOPro (ProjectIgnis), so your
cards look sharp instead of blurry. Rush Duel, anime, GOAT, Pre-Errata and
alternate artworks are all covered, plus the playmat art for Field Spells.

How to use it
-------------
1. Unzip the download.
2. Double-click EDOPro-HD-Sync (and choose "Run"), or run ./EDOPro-HD-Sync
   from a terminal.
3. It finds your ProjectIgnis folder and shows it in the window. If it got
   the wrong one, press "Change..." and pick the right folder.
4. Tick what you want, then press Start.

That's it. There is nothing to install, and the download contains only this
app and this ReadMe. You can put the app wherever you like; its small settings,
retry caches, and optional reports live in your normal per-user config folder.

If your file manager will not run it, mark it executable first:
  chmod +x EDOPro-HD-Sync

Helpful notes
-------------
- The app takes a second or two to start. That is normal: it unpacks itself
  each time so it can stay a single file.
- Only missing artwork is downloaded, so repeat runs are quick. Tick
  "Re-download everything" for a full refresh.
- "Only cards from my decks" is much faster on a fresh install - it grabs
  just the cards in your saved decks.
- "Show coverage" tells you how much artwork you have without downloading.
- The app tells you when a new version is out. Download it from
  https://github.com/cntrl-alt-lenny/EDOPro-HD-Cards-Downloader/releases and replace
  this file with the new one.
- Works on Steam Deck (Desktop Mode), Ubuntu, Fedora, Arch, etc. -
  anything x86_64 Linux.

Quick sanity check
------------------
From a terminal in this folder you can also run:

./EDOPro-HD-Sync --health-check

That runs a quick offline check to verify the tool is working correctly.
