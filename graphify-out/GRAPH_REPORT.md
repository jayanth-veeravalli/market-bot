# Graph Report - .  (2026-05-15)

## Corpus Check
- Corpus is ~3,583 words - fits in a single context window. You may not need a graph.

## Summary
- 74 nodes · 79 edges · 16 communities (11 shown, 5 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.84)
- Token cost: 9,800 input · 2,200 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Bot Core & Design Constraints|Bot Core & Design Constraints]]
- [[_COMMUNITY_Dev Container Setup|Dev Container Setup]]
- [[_COMMUNITY_Watchlist Command & Service|Watchlist Command & Service]]
- [[_COMMUNITY_Options Data Models|Options Data Models]]
- [[_COMMUNITY_Bot Init & Command Registry|Bot Init & Command Registry]]
- [[_COMMUNITY_Premiums Command Handler|Premiums Command Handler]]
- [[_COMMUNITY_Docs & Sync Strategy|Docs & Sync Strategy]]
- [[_COMMUNITY_Database Migration Config|Database Migration Config]]
- [[_COMMUNITY_Tickers Schema Migration|Tickers Schema Migration]]
- [[_COMMUNITY_Claude Code Permissions|Claude Code Permissions]]
- [[_COMMUNITY_Deployment & CICD|Deployment & CI/CD]]
- [[_COMMUNITY_Help Command|Help Command]]

## God Nodes (most connected - your core abstractions)
1. `_fetch_puts()` - 7 edges
2. `fetch_puts_for_ticker()` - 6 edges
3. `Bot` - 5 edges
4. `PutOption` - 5 edges
5. `OptionsResult` - 5 edges
6. `_send_result()` - 5 edges
7. `_table_messages()` - 4 edges
8. `format_result()` - 4 edges
9. `premiums_fetch()` - 3 edges
10. `_format_row()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Discord slash command sync strategy — guild sync for local, global for prod` --references--> `README — Market Research Bot documentation`  [INFERRED]
  bot.py → README.md
- `upgrade()` --shares_data_with--> `add_ticker()`  [INFERRED]
  migrations/versions/333947cbfb58_create_tickers_table.py → services/watchlist.py
- `Bot` --references--> `watchlist_group — /watchlist command group`  [EXTRACTED]
  bot.py → commands/watchlist.py
- `Bot` --references--> `premiums_group — /premiums command group`  [EXTRACTED]
  bot.py → commands/premiums.py
- `_fetch_puts()` --references--> `PutOption`  [EXTRACTED]
  services/alpaca.py → models/options.py

## Hyperedges (group relationships)
- **Premiums request flow — Discord to Alpaca to Discord response** — commands_premiums_premiums_fetch, commands_premiums_send_result, services_alpaca_fetch_puts_for_ticker, services_formatter_format_result [EXTRACTED 1.00]
- **Watchlist CRUD — command layer to psycopg DB operations** — commands_watchlist_watchlist_add, commands_watchlist_watchlist_remove, commands_watchlist_watchlist_fetch, services_watchlist_add_ticker, services_watchlist_remove_ticker, services_watchlist_get_tickers [EXTRACTED 1.00]
- **Deployment pipeline — setup, GitHub Actions, systemd service** — deploy_setup_sh, workflows_deploy_deploy_to_gcp, devcontainer_devcontainer_json [INFERRED 0.85]

## Communities (16 total, 5 thin omitted)

### Community 0 - "Bot Core & Design Constraints"
Cohesion: 0.23
Nodes (11): Eastern timezone enforcement — critical for correct Friday expiry logic, Alpaca indicative feed — estimated options data for research not execution, Strike range 20–30% below spot — deep OTM put selection strategy, Bot — Discord Client, main.py — Entry Point, _fetch_puts(), fetch_puts_for_ticker(), _get_current_price() (+3 more)

### Community 1 - "Dev Container Setup"
Cohesion: 0.18
Nodes (10): customizations, vscode, dockerComposeFile, name, postCreateCommand, remoteUser, service, extensions (+2 more)

### Community 2 - "Watchlist Command & Service"
Cohesion: 0.31
Nodes (7): watchlist_add(), watchlist_fetch(), watchlist_remove(), add_ticker(), fetch_all(), get_tickers(), remove_ticker()

### Community 3 - "Options Data Models"
Cohesion: 0.36
Nodes (7): BaseModel, OptionsResult, PutOption, format_result(), _format_row(), MAX_ROWS_PER_MSG — Discord message chunk size (15 rows), _table_messages()

### Community 4 - "Bot Init & Command Registry"
Cohesion: 0.33
Nodes (3): premiums_group — /premiums command group, watchlist_group — /watchlist command group, Bot

### Community 5 - "Premiums Command Handler"
Cohesion: 0.83
Nodes (3): premiums_fetch(), premiums_stock(), _send_result()

### Community 6 - "Docs & Sync Strategy"
Cohesion: 0.5
Nodes (4): Discord slash command sync strategy — guild sync for local, global for prod, Bot.on_ready — slash command sync, CLAUDE.md — Claude Code project instructions, README — Market Research Bot documentation

## Knowledge Gaps
- **21 isolated node(s):** `create_tickers_table  Revision ID: 333947cbfb58 Revises:  Create Date: 2026-05-1`, `PATH`, `allow`, `name`, `dockerComposeFile` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_send_result()` connect `Premiums Command Handler` to `Bot Core & Design Constraints`, `Options Data Models`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `premiums_fetch()` connect `Premiums Command Handler` to `Watchlist Command & Service`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `get_tickers()` connect `Watchlist Command & Service` to `Premiums Command Handler`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **What connects `create_tickers_table  Revision ID: 333947cbfb58 Revises:  Create Date: 2026-05-1`, `PATH`, `allow` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._