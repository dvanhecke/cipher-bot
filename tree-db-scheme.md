trees:

| Column        | Type             | Description                                 |
| ------------- | ---------------- | ------------------------------------------- |
| `server_id`   | TEXT PRIMARY KEY | Discord server ID                           |
| `height`      | INTEGER          | Current height of the tree                  |
| `level`       | INTEGER          | Tree’s level (can increase as height grows) |
| `last_growth` | TEXT             | ISO timestamp of last growth                |
| `name`        | TEXT             | Tree’s name (customizable)                  |
| `background`  | TEXT             | Tree’s background/skin                      |

users:

| Column      | Type    | Description                     |
| ----------- | ------- | ------------------------------- |
| `user_id`   | TEXT    | Discord user ID                 |
| `server_id` | TEXT    | Discord server ID (foreign key) |
| `points`    | INTEGER | Points earned by the user       |

growth_logs:

| Column      | Type                              | Description                              |
| ----------- | --------------------------------- | ---------------------------------------- |
| `id`        | INTEGER PRIMARY KEY AUTOINCREMENT | Unique log ID                            |
| `server_id` | TEXT                              | Discord server ID                        |
| `timestamp` | TEXT                              | When growth occurred                     |
| `change`    | INTEGER                           | How much the tree grew (e.g., +1 height) |


relationships:

```
trees.server_id  ──┐
                   │
                   ├── users.server_id  (one-to-many)
                   │
                   └── growth_logs.server_id (one-to-many)
```

ERdiagram:

```mermaid
---
title: treebot.db
---
erDiagram
    TREES {
        TEXT server_id PK "Discord server ID"
        INTEGER height "Current height of the tree"
        INTEGER level "Tree's level"
        TEXT last_growth "ISO timestamp of last growth"
        TEXT name "Tree's name"
        TEXT background "Tree's background/skin"
    }

    USERS {
        TEXT user_id "Discord user ID"
        TEXT server_id FK "Discord server ID"
        INTEGER points "Points earned by the user"
    }

    GROWTH_LOGS {
        INTEGER id PK "Unique log ID"
        TEXT server_id FK "Discord server ID"
        TEXT timestamp "When growth occurred"
        INTEGER change "Growth amount (+1 height, etc.)"
    }

    TREES ||--o{ USERS : "has"
    TREES ||--o{ GROWTH_LOGS : "logs"
```
