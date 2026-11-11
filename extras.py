"""Install the optional artwork and sound files shipped with the downloader."""

import hashlib
import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

ASSETS = Path(__file__).resolve().parent / "assets" / "extras"


def install(edopro_path: str, config_path: str, group: str) -> None:
    """Keep a copy of replaced files and publish each replacement atomically."""
    root = Path(edopro_path).resolve()
    backup_root = Path(config_path).resolve().parent / "extras-backups"
    install_id = hashlib.sha256(os.fsencode(root)).hexdigest()[:16]
    sources = sorted((ASSETS / group).rglob("*"))
    files = [source for source in sources if source.is_file()]
    if not files:
        raise FileNotFoundError(f"The optional {group} files are missing from this build.")

    for source in files:
        relative = source.relative_to(ASSETS)
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.parent.resolve().is_relative_to(root):
            raise OSError(f"Cannot install outside the selected EDOPro folder: {relative}")

        content = source.read_bytes()
        if destination.is_file():
            previous = destination.read_bytes()
            if previous == content:
                continue
            revision = hashlib.sha256(previous).hexdigest()[:16]
            backup = backup_root / install_id / revision / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                shutil.copy2(destination, backup)

        staged = None
        try:
            with NamedTemporaryFile(dir=destination.parent, delete=False) as temporary:
                staged = Path(temporary.name)
                temporary.write(content)
            staged.chmod(0o644)
            staged.replace(destination)
        finally:
            if staged is not None:
                staged.unlink(missing_ok=True)
