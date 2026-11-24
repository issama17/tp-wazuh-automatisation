"""
Export des rapports synthétiques CSV et JSON.
Prend en compte l'enrichissement (réputation, score, pays, etc.) si disponible.
"""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def export_report(
    summary: list[dict[str, Any]],
    out_dir: str = "reports",
) -> tuple[str, str]:
    """
    Écrit un rapport JSON + CSV dans out_dir.
    Retourne (chemin_json, chemin_csv).
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    # --- JSON ---
    json_path = Path(out_dir) / f"alert_summary_{ts}.json"
    json_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # --- CSV ---
    csv_path = Path(out_dir) / f"alert_summary_{ts}.csv"

    # Détection dynamique des colonnes selon la présence d'enrichissement
    base_fields = ["src_ip", "period", "count", "max_severity", "hosts", "rules"]
    enrichment_fields = ["reputation", "score", "country", "total_reports"]

    fieldnames = list(base_fields)
    for ef in enrichment_fields:
        if any(ef in row for row in summary):
            fieldnames.append(ef)

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary:
            row_dict = {
                "src_ip": row.get("src_ip", ""),
                "period": row.get("period", ""),
                "count": row.get("count", 0),
                "max_severity": row.get("max_severity", 0),
                "hosts": ";".join(row.get("hosts") or []),
                "rules": ";".join(row.get("rules") or []),
            }
            for ef in enrichment_fields:
                if ef in fieldnames:
                    row_dict[ef] = row.get(ef, "")
            writer.writerow(row_dict)

    return str(json_path), str(csv_path)
