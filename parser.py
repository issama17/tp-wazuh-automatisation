"""
Chargement et extraction des champs clés des alertes Wazuh.
"""

import json
from pathlib import Path
from typing import Any


def load_alerts(filepath: str) -> list[dict]:
    """
    Charge un fichier d'alertes Wazuh.
    Supporte :
      - un tableau JSON classique  [ {...}, {...} ]
      - du NDJSON (une alerte JSON par ligne)
      - un seul objet JSON
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []

    # Tentative array / objet unique
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
    except json.JSONDecodeError:
        pass

    # Fallback NDJSON
    alerts = []
    for line_no, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            alerts.append(json.loads(line))
        except json.JSONDecodeError as exc:
            print(f"[WARN] Ligne {line_no} ignorée (JSON invalide) : {exc}")
    return alerts


def extract_fields(alert: dict) -> dict[str, Any]:
    """
    Extrait les champs utiles pour l'agrégation et le reporting.
    Utilise .get() partout pour rester robuste face aux alertes incomplètes.
    """
    rule = alert.get("rule") or {}
    agent = alert.get("agent") or {}
    data = alert.get("data") or {}

    # Certaines versions / règles mettent l'IP dans des emplacements différents
    src_ip = (
        data.get("srcip")
        or data.get("src_ip")
        or data.get("srcip")
        or alert.get("srcip")
    )
    src_user = data.get("srcuser") or data.get("src_user") or data.get("dstuser")

    return {
        "timestamp": alert.get("timestamp"),
        "rule_id": rule.get("id"),
        "severity": rule.get("level"),
        "description": rule.get("description"),
        "host": agent.get("name"),
        "agent_ip": agent.get("ip"),
        "src_ip": src_ip,
        "src_user": src_user,
    }
