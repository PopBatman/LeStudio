"""Crée une configuration locale privée, sans écraser une configuration existante."""

import os
from pathlib import Path
import secrets
import sys
import tempfile


def main():
    target = Path(__file__).resolve().parents[1] / ".env"
    with tempfile.NamedTemporaryFile(mode="w", dir=target.parent, prefix=".env.") as temp:
        for key in ("DJANGO_SECRET_KEY", "STUDIO_DB_PASSWORD", "POSTGRES_PASSWORD"):
            temp.write(f"{key}={secrets.token_urlsafe(48)}\n")
        temp.flush()
        os.fsync(temp.fileno())
        try:
            os.link(temp.name, target)
        except FileExistsError:
            if target.is_symlink() or not target.is_file():
                sys.exit("Le chemin .env doit désigner un fichier ordinaire.")
            print("Le fichier .env existe déjà.")
        else:
            print("Configuration locale créée dans .env (mode 0600).")


if __name__ == "__main__":
    main()
