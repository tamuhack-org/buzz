# THbot

Create the required `.env` file
```sh
cp .env.example .env # macOS/Linux

copy .env.example .env # Windows
```

Make sure you have `uv` installed (instructions found [here](https://docs.astral.sh/uv/getting-started/installation/)), then run
```sh
uv venv .venv
uv sync

source .venv/bin/activate # macOS/Linux

.\.venv\Scripts\activate # Windows
```

Default server is https://127.0.0.1:8000

Docs are http://127.0.0.1:8000/docs
