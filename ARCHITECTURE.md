# Architecture

Harbor Catalog is a single-process HTTP API. Routers validate input and call services. Services own the rules and are the only layer that commits a session. Models stay persistence-only.

Available stock is `on_hand - reserved`. A reserve call refuses the request when available stock is lower than the quantity, and it does not partially reserve. Receive only increases `on_hand`.

SQLite is the default so the service can run with no extra database. The session factory is stored on `app.state`, which lets tests build a second app against `sqlite://` without touching the development file.

Startup creates tables and, unless disabled, seeds two categories and two products when the database is empty.
