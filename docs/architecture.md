# Architecture

Harbor Catalog API keeps HTTP or CLI code away from the rules. The path is HTTP client → Routers → Catalog service → SQLite.

See `images/architecture.svg`.
