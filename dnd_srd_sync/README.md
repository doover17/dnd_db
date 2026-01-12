# dnd_srd_sync

Sync tooling for importing D&D SRD data into a database.

## Setup

```bash
cd dnd_srd_sync
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

## Usage

Show CLI help:

```bash
python -m dnd_srd_sync --help
```

Initialize the database schema:

```bash
python -m dnd_srd_sync --init-db
```

Generate an Alembic migration and apply it:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

Fetch and display the API index:

```bash
python -m dnd_srd_sync --show-index
```
