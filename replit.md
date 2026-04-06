# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.

## Chess Analysis (Python)

A standalone Python module for analyzing chess game data from PGN files.

**Location:** `chess-analysis/`

**Structure:**
- `parser.py` — Reads PGN files and extracts raw game data using python-chess
- `processing.py` — Classifies opening moves and responses; adds decade column
- `analytics.py` — Computes win rates, draw rates, frequency, and avg score per group
- `main.py` — Entry point: loads, processes, prints sample, and exports CSVs
- `data/` — Place `.pgn` files here
- `output/` — Generated CSVs written here

**Run:**
```
pip install -r requirements.txt
python main.py
```

**Key functions (API-ready):**
- `load_games(path)` → raw DataFrame
- `process_games(df)` → cleaned/categorized DataFrame
- `compute_metrics(df, group_by="decade")` → aggregated metrics DataFrame
- `filter_data(df, start_year, end_year, white_move=None)` → filtered DataFrame
- `export_csv(df, output_path)` → writes CSV, returns path
- `prepare_for_visualization(df, group_by)` → dict ready for JSON serialization
