"""
Module d'enrichissement des alertes agrégées.
Prend en charge :
  1. Enrichissement Mock (sans API externe, toujours disponible)
  2. Enrichissement réel via AbuseIPDB (avec cache, gestion des rate limits et filtrage IP privée)
"""

import os
import ipaddress
from typing import Any
import requests
from dotenv import load_dotenv

# Charge les variables d'environnement depuis un fichier .env si présent
load_dotenv()

# Cache mémoire pour éviter d'appeler l'API plusieurs fois pour la même IP
_ABUSEIPDB_CACHE: dict[str, dict] = {}


def is_public_ip(ip_str: str) -> bool:
    """Vérifie si une adresse IP est une adresse publique routable sur Internet."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_global
    except ValueError:
        return False


def enrich_mock(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Ajoute un score de réputation fictif et un tag basé sur le volume d'alertes.
    - count >= 20 : high_risk (score 90)
    - count >= 5  : suspicious (score 60)
    - sinon       : low (score 20)
    """
    for item in summary:
        count = item.get("count", 0)
        if count >= 20:
            item["reputation"] = "high_risk"
            item["score"] = 90
        elif count >= 5:
            item["reputation"] = "suspicious"
            item["score"] = 60
        else:
            item["reputation"] = "low"
            item["score"] = 20
        item["enriched"] = True
    return summary


def check_abuseipdb(ip: str, api_key: str | None = None) -> dict[str, Any]:
    """
    Interroge l'API v2 d'AbuseIPDB pour une adresse IP publique donnée.
    Utilise un cache local pour respecter les quotas de l'offre gratuite.
    """
    if ip in _ABUSEIPDB_CACHE:
        return _ABUSEIPDB_CACHE[ip]

    # Vérification si l'IP est privée / interne (Tailscale, LAN, Loopback)
    if not is_public_ip(ip):
        res = {
            "abuse_score": 0,
            "country": "LAN/VPN",
            "total_reports": 0,
            "note": "Adresse IP privée ou non routable publiquement"
        }
        _ABUSEIPDB_CACHE[ip] = res
        return res

    key = api_key or os.getenv("ABUSEIPDB_KEY")
    if not key:
        return {"error": "no_key"}

    url = "https://api.abuseipdb.com/api/v2/check"
    params = {"ipAddress": ip, "maxAgeInDays": 90}
    headers = {"Key": key, "Accept": "application/json"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=8)
        if r.status_code == 200:
            data = r.json().get("data", {})
            res = {
                "abuse_score": data.get("abuseConfidenceScore", 0),
                "country": data.get("countryCode", "??"),
                "total_reports": data.get("totalReports", 0),
            }
            _ABUSEIPDB_CACHE[ip] = res
            return res
        return {"error": f"HTTP {r.status_code}"}
    except requests.RequestException as exc:
        return {"error": str(exc)}


def enrich_abuseipdb(
    summary: list[dict[str, Any]],
    api_key: str | None = None,
) -> list[dict[str, Any]]:
    """
    Enrichit chaque IP du résumé avec les données réelles d'AbuseIPDB.
    En l'absence de clé API valide, bascule automatiquement sur l'enrichissement mock.
    """
    key = api_key or os.getenv("ABUSEIPDB_KEY")
    if not key:
        print("[WARN] Aucune clé ABUSEIPDB_KEY trouvée dans l'environnement ou le fichier .env.")
        print("[INFO] Bascule automatique sur l'enrichissement mock heuristique.")
        return enrich_mock(summary)

    for item in summary:
        ip = item.get("src_ip")
        if not ip:
            continue

        info = check_abuseipdb(ip, key)
        if "error" not in info:
            score = info.get("abuse_score", 0)
            item["score"] = score
            item["country"] = info.get("country", "??")
            item["total_reports"] = info.get("total_reports", 0)

            # Si c'est une IP interne (ex. Tailscale ou LAN), on utilise le volume interne pour qualifier
            if not is_public_ip(ip):
                count = item.get("count", 0)
                item["reputation"] = "high_risk" if count >= 20 else ("suspicious" if count >= 5 else "low")
                item["score"] = 90 if count >= 20 else (60 if count >= 5 else 20)
            else:
                # Qualification basée sur le score d'abus AbuseIPDB réel
                if score >= 80:
                    item["reputation"] = "high_risk"
                elif score >= 20:
                    item["reputation"] = "suspicious"
                else:
                    item["reputation"] = "low"
            item["enriched"] = True
        else:
            # Fallback mock pour cet item en cas d'erreur API
            count = item.get("count", 0)
            item["reputation"] = "high_risk" if count >= 20 else ("suspicious" if count >= 5 else "low")
            item["score"] = 90 if count >= 20 else (60 if count >= 5 else 20)
            item["enriched"] = True
            item["api_error"] = info["error"]

    return summary
