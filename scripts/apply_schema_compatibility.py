"""Aplica ajustes de compatibilidad para bases legadas fuera del runtime normal."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine
from config.schema_compatibility import ensure_schema_compatibility


def main() -> None:
    actions = ensure_schema_compatibility(engine)
    if not actions:
        print("No schema compatibility changes were required.")
        return

    print("Applied schema compatibility changes:")
    for action in actions:
        print(f"- {action}")


if __name__ == "__main__":
    main()