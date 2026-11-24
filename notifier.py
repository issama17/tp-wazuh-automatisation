"""
Notifications console et webhook.
"""

from typing import Any
import requests


def notify_console(summary: list[dict[str, Any]], threshold: int = 5) -> None:
    """Affiche les IP dont le nombre d'événements dépasse le seuil."""
    critical = [s for s in summary if s.get("count", 0) >= threshold]

    if not critical:
        print(f"\n[INFO] Aucune IP au-dessus du seuil ({threshold}).")
        return

    has_enrichment = any("reputation" in item for item in critical)

    print(f"\n=== {len(critical)} IP(s) suspecte(s) – seuil ≥ {threshold} ===")
    if has_enrichment:
        print(f"{'IP source':<18} {'Count':>5}  {'Sev':>3}  {'Réputation':<12} {'Score':>5}  Hôtes")
        print("-" * 75)
        for item in critical:
            hosts = ", ".join(item.get("hosts") or []) or "-"
            rep = item.get("reputation", "-")
            score = item.get("score", "-")
            print(
                f"{item.get('src_ip', '?'):<18} "
                f"{item.get('count', 0):>5}  "
                f"{item.get('max_severity', 0):>3}  "
                f"{rep:<12} "
                f"{str(score):>5}  "
                f"{hosts}"
            )
    else:
        print(f"{'IP source':<20} {'Count':>6}  {'Sev max':>7}  Hôtes")
        print("-" * 70)
        for item in critical:
            hosts = ", ".join(item.get("hosts") or []) or "-"
            print(
                f"{item.get('src_ip', '?'):<20} "
                f"{item.get('count', 0):>6}  "
                f"{item.get('max_severity', 0):>7}  "
                f"{hosts}"
            )
    print()


def notify_webhook(
    summary: list[dict[str, Any]],
    webhook_url: str,
    threshold: int = 5,
) -> None:
    """
    Envoie un POST JSON vers l'URL de test (webhook.site, RequestBin, Slack, etc.).
    """
    critical = [s for s in summary if s.get("count", 0) >= threshold]
    if not critical:
        print("[INFO] Rien à envoyer au webhook.")
        return

    payload = {
        "source": "tp-wazuh-automatisation",
        "threshold": threshold,
        "count_ips": len(critical),
        "ips": [
            {
                "ip": i.get("src_ip"),
                "count": i.get("count"),
                "max_severity": i.get("max_severity"),
                "reputation": i.get("reputation"),
                "score": i.get("score"),
                "country": i.get("country"),
                "hosts": i.get("hosts"),
                "rules": i.get("rules"),
                "period": i.get("period"),
            }
            for i in critical[:25]  # limite de sécurité
        ],
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=12)
        resp.raise_for_status()
        print(f"[OK] Webhook envoyé → {webhook_url} (status {resp.status_code})")
    except requests.RequestException as exc:
        print(f"[ERREUR] Échec envoi webhook : {exc}")
