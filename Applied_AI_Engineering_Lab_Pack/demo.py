"""Read-only synthetic demo; no model, network, or paid service."""
import json
from pathlib import Path
from solutions.core import database, property_open_counts, retrieve, token_cost # type: ignore

with database() as conn:
    print("Open requests:", property_open_counts(conn))
docs=json.loads((Path(__file__).parent/"data/documents.json").read_text())
print("Organization A tap search:", retrieve("leaking tap",docs,"A")) # type: ignore
print("Illustrative token cost:", token_cost(1000,200,"1","4"))
print("This is deterministic reference code, not a live AI demonstration.")
