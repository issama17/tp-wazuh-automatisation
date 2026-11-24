#!/usr/bin/env python3
"""
Script Wazuh Active Response personnalisé (Partie F - Optionnelle)
Emplacement recommandé sur le Manager ou l'Agent :
  /var/ossec/active-response/bin/custom-ar-audit.py

Rôle :
  1. Lit les données de l'alerte transmises par Wazuh via sys.stdin (format JSON v1).
  2. Extrait l'IP source, l'agent cible, et l'identifiant de règle.
  3. Applique une logique de décision de sécurité (ex. règle 5712 brute force SSH).
  4. Écrit dans un fichier d'audit local (/var/ossec/logs/active-response-audit.log) pour une traçabilité totale.
  5. Enregistre une recommandation de blocage (mode semi-automatique sécurisé).
"""

import sys
import json
import os
from datetime import datetime, timezone

LOG_FILE = "/var/ossec/logs/active-response-audit.log"
# En environnement Windows ou lab de test local si /var/ossec n'existe pas :
if not os.path.exists("/var/ossec/logs"):
    LOG_FILE = "active-response-audit.log"


def write_audit(message: str):
    """Écrit une ligne horodatée dans le journal d'audit."""
    now = datetime.now(timezone.utc).isoformat()
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        sys.stderr.write(f"Erreur d'écriture audit : {e}\n")


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            write_audit("[WARN] Entrée standard vide reçue.")
            return

        data = json.loads(raw_input)
        command = data.get("command", "add")
        parameters = data.get("parameters", {})
        alert = parameters.get("alert", {})

        rule = alert.get("rule", {})
        rule_id = str(rule.get("id", "unknown"))
        rule_level = rule.get("level", 0)
        rule_desc = rule.get("description", "")

        agent = alert.get("agent", {})
        agent_name = agent.get("name", "unknown")
        agent_id = agent.get("id", "unknown")

        alert_data = alert.get("data", {})
        srcip = (
            alert_data.get("srcip")
            or alert_data.get("src_ip")
            or alert.get("srcip")
        )

        # Log de l'événement reçu
        write_audit(
            f"[AR-TRIGGER] Commande={command} | Règle={rule_id} (Niveau {rule_level}) | "
            f"Agent={agent_name} ({agent_id}) | IP Source={srcip or 'N/A'} | Description={rule_desc}"
        )

        # Logique de sécurité : Règle SSH Brute Force (5712) ou sévérité élevée
        if rule_id in ["5712", "5710"] or rule_level >= 10:
            if srcip:
                # Mode semi-automatique : logging + recommandation de blocage
                action_msg = (
                    f"[SEMI-AUTO DECISION] ALERTE BRUTE FORCE VALIDÉE pour l'IP {srcip} "
                    f"sur l'hôte {agent_name}. Recommandation d'endiguement : "
                    f"iptables -I INPUT -s {srcip} -j DROP (En attente de validation analyste SOC)"
                )
                write_audit(action_msg)
            else:
                write_audit(f"[INFO] Règle {rule_id} détectée sans IP source exploitable.")
        else:
            write_audit(f"[INFO] Événement traité (hors politique de blocage immédiat).")

        # Réponse protocole Wazuh AR
        response = {
            "version": 1,
            "origin": {"name": "custom-ar-audit", "module": "active-response"},
            "command": command,
            "parameters": {"status": "success"}
        }
        print(json.dumps(response))

    except Exception as exc:
        write_audit(f"[ERROR] Exception dans custom-ar-audit : {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
