# Buzz
A discord bot to be used in TAMUhack! 

Discord integration for [helpr](https://github.com/tamuhack-org/helpr), kept in sync with helpr's ticket state.

- Posts new tickets in the mentor channel and pings the mentor role
- Mentors can claim, unclaim and resolve tickets from the message buttons
- Actions made on helpr update the Discord message too (and vice versa)
- Canceled tickets are deleted and the claimant is DMed
- Linking Discord on helpr gives the mentor role; `/checkout` command removes it

## Discord setup
- Create the bot at the [developer portal](https://discord.com/developers/applications) (no privileged intents needed)
- Invite with scopes `bot` + `applications.commands` and permissions:
  - Manage Roles
- Move buzz's role above the mentor role (Server Settings > Roles), or it can't grant/remove it
- Give buzz access to the mentor channel
- Allow mentors to use `/checkout` (Server Settings > Integrations > buzz), it's admin-only by default and restrict to mentor channel if needed

## Bot setup
Create the required `.env` file (and populate it)
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
