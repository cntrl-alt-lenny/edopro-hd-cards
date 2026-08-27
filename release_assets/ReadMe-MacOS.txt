EDOPro HD Cards Downloader for macOS
========================

How to use it
-------------
1. Unzip the download (double-click the .zip in Finder).
2. Open the "EDOPro HD Sync" folder and double-click EDOPro HD Sync
3. Tick what you want in the window that opens, then press Start.

The app finds your EDOPro folder on its own and shows it at the top of
the window. Press "Change..." if it picked the wrong one.

If macOS asks the very first time
---------------------------------
Because the app came from the web, macOS may refuse to open it the first
time. RIGHT-CLICK "EDOPro HD Sync" and choose "Open", then "Open" again.
After that it opens normally with a double-click.

If macOS still refuses, open System Settings > Privacy & Security,
scroll down, and click "Open Anyway" next to EDOPro HD Sync.

Helpful notes
-------------
- Everything happens in one window: tick what you want (field art,
  only your decks, textures, repair), press Start, and watch the progress.
- Nothing is installed. The download contains one app and this ReadMe. You can
  put the app anywhere; its small settings, retry caches, and optional reports
  live in ~/Library/Application Support/EDOPro HD Sync instead of beside the
  app, so it also works from protected folders.
- The published app is built for Intel Macs and runs on Apple Silicon through
  Rosetta.
- Only missing artwork is downloaded, so repeat runs are fast. Tick
  "Re-download everything" in the window for a full refresh.
- "Show coverage" tells you how much artwork you have without downloading.
- Rush Duel, anime, GOAT, Pre-Errata, and alternate artworks are all
  covered, plus the playmat art for Field Spells.
- When a newer version is out, the app tells you - download it from the
  Releases page and replace this one.

Quick sanity check
------------------
Advanced users can run a quick offline self-test in Terminal:

  "EDOPro HD Sync.app/Contents/MacOS/EDOPro-HD-Sync" --health-check
