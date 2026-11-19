# Agent instructions — Airlines RefData Analytics Platform

## Methodology

This repo uses **Superpowers** (vendored under [`superpowers/`](superpowers/)).

**Run milestones one after another.** For each milestone:

1. Brainstorm → design doc → human approval  
2. Writing-plans  
3. Git worktree / feature branch  
4. Execute plan (TDD)  
5. Code review  
6. Finish branch / PR  
7. Only then start the next milestone  

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for milestones, epics, features, and stories.

## Hard constraints (until lifted)

- **No AWS stack creates / no paid AWS provisioning** during M0–M5
- Local-first: MySQL, Debezium, Kafka, RabbitMQ, Airflow, MinIO (or equivalent), portals
- Prefer paths under `CICD/Local/`, `Middleware/`, `Portals/`

## Install Superpowers in Cursor

This repo enables the plugin via [`.cursor/settings.json`](.cursor/settings.json):

```json
{
  "plugins": {
    "superpowers": {
      "enabled": true
    }
  }
}
```

If the marketplace plugin is missing locally, also run in Agent chat:

```text
/add-plugin superpowers
```

Keep the vendored [`superpowers/`](superpowers/) tree for pinned skills. ARFD board wrappers live under [`.cursor/skills/`](.cursor/skills/) (`arfd-story-start`, …).
