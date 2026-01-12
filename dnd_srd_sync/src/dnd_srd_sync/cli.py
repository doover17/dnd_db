"""Command-line interface for dnd_srd_sync."""

from __future__ import annotations

import argparse

from rich.console import Console

from dnd_srd_sync.api.client import SrdClient
from dnd_srd_sync.config import Settings
from dnd_srd_sync.db.engine import get_engine, init_db
from dnd_srd_sync.etl.extract import extract_index

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync D&D SRD data into a database.")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database schema.")
    parser.add_argument("--show-index", action="store_true", help="Fetch and display the API index.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    settings = Settings.from_env()

    if args.init_db:
        engine = get_engine(settings)
        init_db(engine)
        console.print("Database initialized.")

    if args.show_index:
        client = SrdClient.from_settings(settings)
        index = extract_index(client)
        console.print(index)

    if not args.init_db and not args.show_index:
        parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
