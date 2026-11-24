"""
Agrégation des alertes par IP source et fenêtre temporelle.
"""

from collections import defaultdict
from datetime import datetime
from typing import Any


def _parse_ts(ts: str) -> datetime | None:
    """Parse un timestamp Wazuh (ISO 8601, souvent avec Z)."""
    if not ts:
        return None
    try:
        # Gestion du Z final (UTC)
        cleaned = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned)
    except ValueError:
        return None


def group_by_ip_and_period(
    events: list[dict],
    window_minutes: int = 60,
) -> list[dict[str, Any]]:
    """
    Regroupe les événements par (src_ip, bucket_temporel).

    Pour chaque groupe retourne :
      - src_ip
      - period (début de la fenêtre ISO)
      - count
      - max_severity
      - hosts (liste unique)
      - rules  (liste unique d'ids de règles)
    """
    if window_minutes < 1:
        raise ValueError("window_minutes doit être >= 1")

    groups: dict[tuple, list] = defaultdict(list)

    for ev in events:
        src_ip = ev.get("src_ip")
        ts = _parse_ts(ev.get("timestamp") or "")
        if not src_ip or ts is None:
            continue

        # Arrondi à la fenêtre (ex. 14:00–14:59 pour window=60)
        bucket = ts.replace(
            minute=(ts.minute // window_minutes) * window_minutes,
            second=0,
            microsecond=0,
        )
        key = (src_ip, bucket.isoformat())
        groups[key].append(ev)

    summary = []
    for (ip, period), items in groups.items():
        severities = [i.get("severity") or 0 for i in items]
        hosts = sorted({i["host"] for i in items if i.get("host")})
        rules = sorted({str(i["rule_id"]) for i in items if i.get("rule_id") is not None})

        summary.append({
            "src_ip": ip,
            "period": period,
            "count": len(items),
            "max_severity": max(severities) if severities else 0,
            "hosts": hosts,
            "rules": rules,
        })

    # Plus d'événements en premier
    return sorted(summary, key=lambda x: (-x["count"], x["src_ip"]))
