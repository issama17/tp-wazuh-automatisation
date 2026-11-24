# TP – Automatisation et enrichissement des alertes Wazuh

<p align="center">
  <b>Université Abdelmalek Essaâdi • École Supérieure de Technologie de Tétouan</b><br>
  <i>Département Informatique • DUT Cybersécurité et audit des systèmes d'information (2026–2027)</i><br>
  <b>Module : Introduction au SOC et supervision</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Wazuh-v4.x-007EC6?logo=wazuh" alt="Wazuh">
  <img src="https://img.shields.io/badge/AbuseIPDB-v2_API-orange" alt="AbuseIPDB">
  <img src="https://img.shields.io/badge/Status-Completed-success" alt="Status">
</p>

---

## 📌 À propos du projet

Ce projet constitue les travaux pratiques complets du module **"Introduction au SOC et supervision"**. Il implémente un pipeline complet de détection, parsing, agrégation temporelle, enrichissement via Threat Intelligence (AbuseIPDB) et notification d'alertes de sécurité Wazuh.

Il comprend également l'extraction en temps réel d'alertes SSH depuis un **Wazuh Manager** de production, le traitement des attaques provenant d'une machine **Kali Linux**, ainsi que le déploiement d'une **Active Response semi-automatique** (Human-in-the-loop) pour l'audit et l'endiguement.

📄 **Lien direct vers le rapport de TP officiel (PDF) :**  
👉 **[Rapport_TP_Wazuh_Automatisation_Issam_ECHAHBOUNI.pdf](Rapport_TP_Wazuh_Automatisation_Issam_ECHAHBOUNI.pdf)** *(10 pages détaillées avec toutes les captures et justifications)*

---

## 🏗️ Architecture du Laboratoire Multi-Systèmes

Le laboratoire reproduit une architecture SOC réaliste interconnectée :

```text
┌───────────────────────┐                    ┌──────────────────────────────────┐
│   Machine Kali Linux  │──(Attaque SSH)────▶│       Agent AWS Lightsail        │
│    129.159.197.13     │                    │  Ubuntu 22.04 | Port SSH: 22222  │
└───────────────────────┘                    │ IP: 13.39.3.250 / 100.120.55.48  │
                                             └────────────────┬─────────────────┘
                                                              │
                                                        (Wazuh Agent)
                                                              ▼
┌───────────────────────┐                    ┌──────────────────────────────────┐
│    Poste Windows      │◀──(Extraction)─────│          Wazuh Manager           │
│     (Analyste SOC)    │                    │     VM Linux CentOS / RHEL       │
│  Pipeline Python 3    │                    │ IP: 192.168.200.17 / 100.64.38.76│
│ + Rapport CSV / JSON  │                    │ + Active Response (custom-ar)    │
└───────────────────────┘                    └──────────────────────────────────┘
```

---

## 📁 Structure du Projet

```text
tp_wazuh_starter/
├── active_response/
│   └── custom-ar-audit.py   # Script Active Response Python (déployé sur le Manager Wazuh)
├── img/                     # Captures d'écran et preuves d'exécution en laboratoire
│   ├── capture1_execution_console.jpg
│   ├── capture2_webhook_reception.png
│   ├── capture3_rapport_excel.jpg
│   ├── capture4_manager_live_alerts_ssh.jpg
│   ├── capture5_abuseipdb_enrichment.jpg
│   ├── capture6_live_alerts_execution.jpg
│   └── capture7_active_response_audit_log.png
├── reports/                 # Rapports horodatés d'audit générés (CSV et JSON)
├── alerts_sample.json       # Dataset de simulation d'alertes Wazuh (format JSON array)
├── alerts_sample.ndjson     # Même dataset au format NDJSON (streaming ligne par ligne)
├── live_alerts_ssh.json     # 50 alertes réelles extraites en direct du Wazuh Manager
├── live_alerts.json         # Copie du flux réel pour validation de robustesse
├── parser.py                # Chargement (JSON/NDJSON) et extraction résiliente (.get)
├── aggregator.py            # Regroupement par IP source et fenêtre temporelle glissante
├── enricher.py              # Enrichissement Mock ou API réelle AbuseIPDB (avec cache & IP privées)
├── reporter.py              # Export des synthèses d'audit horodatées (.csv et .json)
├── notifier.py              # Affichage console formaté et notification Webhook (HTTP POST)
├── main.py                  # Point d'entrée CLI (arguments et orchestration du pipeline)
├── create_report.py         # Moteur de génération automatique du rapport PDF final
├── rapport_tp_wazuh.html    # Version web du rapport d'audit
├── Rapport_TP_Wazuh_Automatisation_Issam_ECHAHBOUNI.pdf # Rapport académique final (10 pages)
├── requirements.txt         # Dépendances Python
├── .env.example             # Modèle de configuration pour la clé AbuseIPDB
└── README.md                # Documentation complète du projet
```

---

## 🚀 Installation et Démarrage Rapide

### 1. Prérequis
Python **3.8 ou supérieur** est requis.

```bash
# Cloner le dépôt
git clone https://github.com/issama17/tp-wazuh-automatisation.git
cd tp-wazuh-automatisation

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration optionnelle d'AbuseIPDB
Pour activer la Threat Intelligence réelle :
```bash
cp .env.example .env
# Renseignez votre clé gratuite dans .env :
# ABUSEIPDB_KEY=votre_cle_api_ici
```

---

## 💻 Exemples d'Exécution

### A. Exécution standard sur le dataset simulé (Enrichissement mock, fenêtre 60 min, seuil 5)
```bash
python main.py -i alerts_sample.json -w 60 -t 5
```

### B. Prise en charge transparente du format NDJSON
```bash
python main.py -i alerts_sample.ndjson -w 60 -t 5
```

### C. Enrichissement réel via l'API AbuseIPDB
```bash
python main.py -i alerts_sample.json --enrich abuseipdb
```

### D. Envoi de notification Webhook vers un SOAR / Webhook.site
```bash
python main.py -i alerts_sample.json -w 60 -t 5 --webhook https://webhook.site/votre-uuid
```
*(Option `--dry-run` disponible pour tester sans requête réseau réelle).*

### E. Analyse des alertes réelles extraites de production
```bash
python main.py -i live_alerts_ssh.json -w 60 -t 3
```

---

## ⚙️ Options en Ligne de Commande

| Option | Type | Valeur par défaut | Description |
|---|---|---|---|
| `-i`, `--input` | `str` | *(Requis)* | Fichier d'alertes Wazuh (`.json` ou `.ndjson`) |
| `-w`, `--window` | `int` | `60` | Durée de la fenêtre temporelle en minutes |
| `-t`, `--threshold` | `int` | `5` | Seuil minimal d'événements pour qualifier une IP de suspecte |
| `--enrich` | `choice` | `mock` | Mode d'enrichissement (`mock`, `abuseipdb`, `none`) |
| `--webhook` | `str` | `None` | URL du webhook de destination pour le payload JSON |
| `--dry-run` | `flag` | `False` | Simule l'envoi webhook sans appel HTTP externe |

---

## 🛡️ Partie F : Active Response Wazuh (Bonus)

Un script d'Active Response personnalisé (`custom-ar-audit.py`) a été déployé sur le **Manager Wazuh** (`/var/ossec/active-response/bin/custom-ar-audit.py`) :

1. **Fonctionnement :**
   * Wazuh déclenche le script lors des attaques par force brute SSH (Règles 5710 et 5712).
   * Le script consomme le JSON de l'alerte sur `stdin`.
   * Il enregistre un journal structuré dans `/var/ossec/logs/active-response-audit.log`.
   * Il génère une recommandation d'endiguement pare-feu (`iptables -I INPUT -s <IP> -j DROP`) en mode **semi-automatique** (Human-in-the-loop).

2. **Configuration dans `/var/ossec/etc/ossec.conf` :**
   ```xml
   <command>
     <name>custom-ar-audit</name>
     <executable>custom-ar-audit.py</executable>
     <timeout_allowed>no</timeout_allowed>
   </command>

   <active-response>
     <command>custom-ar-audit</command>
     <location>server</location>
     <rules_id>5710,5712</rules_id>
   </active-response>
   ```

---

## 🧠 Réponses aux Questions de Réflexion (Section 13)

### 1. Pourquoi l’enrichissement (asset + user + IOC) change-t-il la priorité d’une alerte ?
Une alerte brute isolée (ex. un échec SSH ou une alerte IDS de niveau moyen) ne reflète que le signal technique élémentaire. L'enrichissement lui confère son contexte métier et opérationnel :
- **Asset (criticité de la machine) :** Un scan ou un échec de connexion sur un serveur de test ou un pot de miel n'a pas le même impact que sur un contrôleur de domaine (Active Directory) ou une base de données de production contenant des données sensibles.
- **User (privilèges du compte) :** Une anomalie sur un compte non privilégié est moins critique qu'une tentative visant un compte `root`, `Domain Admin` ou un compte de service sensible.
- **IOC (Threat Intelligence / Réputation) :** Savoir que l'IP source appartient à un nœud de sortie Tor, un VPN anonymiseur ou présente un score d'abus de 100 % sur AbuseIPDB transforme instantanément un faible signal en incident prioritaire (P1/P2), évitant la fatigue d'alerte sur des sources anodines.

### 2. Quels risques y a-t-il à bloquer automatiquement une IP à partir d’un simple compteur ?
Le blocage automatique basé uniquement sur un seuil quantitatif ($N \ge 5$) présente des risques majeurs :
1. **Déni de service induit (Self-DoS / Spoofing) :** Un attaquant peut usurper (IP spoofing en UDP/DNS) l'adresse d'un serveur légitime critique (passerelle par défaut, serveur DNS, serveur de mises à jour, proxy) pour pousser l'Active Response à bannir un composant vital.
2. **Impact sur des utilisateurs légitimes (NAT / CGNAT) :** Dans un réseau d'entreprise, une université ou une connexion mobile (4G/5G), des centaines d'utilisateurs partagent la même IP publique de sortie. Si un seul utilisateur oublie son mot de passe ou réalise des tests, bannir l'IP publique coupe l'accès à l'ensemble des collaborateurs.
3. **Scanners légitimes :** Les audits de sécurité internes et scanners de vulnérabilité autorisés (ex. Nessus, Qualys) risquent d'être bannis de façon intempestive.

### 3. Comment distinguerez-vous un scan légitime (vulnérabilité management) d’une attaque réelle ?
- **Source connue et planifiée :** Vérification de l'IP source contre une liste blanche (whitelist) des outils d'audit internes (adresses réservées de la sonde Qualys/Nessus) et correspondance avec un calendrier d'audit ou un ticket de changement (RFC).
- **User-Agent et signatures :** Les scanners d'audit affichent généralement un User-Agent transparent ou utilisent des en-têtes d'identification négociés.
- **Vecteur et comportement :** Un scan de vulnérabilité balaie un large spectre de ports et d'URLs de façon systématique sans chercher à exploiter activement les failles découvertes ni à déposer des charges utiles (droppers, web shells) ou à maintenir une persistance, contrairement à une attaque réelle qui enchaîne reconnaissance, exploitation ciblée et exfiltration.

### 4. Que se passe-t-il si l’API d’enrichissement (AbuseIPDB, MISP…) est indisponible ?
Si l'API externe subit une panne de réseau, une erreur HTTP 5xx ou un dépassement de quota (rate limiting / HTTP 429) :
1. **Risque de blocage du pipeline (Timeout) :** Sans gestion des timeouts courts (`timeout=5-8s`), le script ou le moteur SOAR peut se figer et accumuler un retard critique dans le traitement des flux d'alertes en temps réel.
2. **Perte de qualification :** L'alerte risque de ne pas être priorisée ou d'être abandonnée.
3. **Solutions architecturales implémentées :**
   - Mise en place d'un mécanisme de secours (**Graceful Fallback**) vers une heuristique locale ou un enrichissement mock.
   - Utilisation d'un **cache local** pour conserver les réputations déjà connues pendant plusieurs heures.
   - Mode asynchrone / file d'attente (MQ / Celery) afin que l'indisponibilité de l'enrichissement ne bloque pas la journalisation et l'ingestion des alertes brutes.

### 5. Où placeriez-vous la validation humaine dans votre pipeline (auto / semi-auto / manuel) ?
Le positionnement de la validation humaine dépend de la criticité de l'action et du niveau de confiance du signal :
- **Totalement Automatique :** Pour les actions passives et non destructives : collecte des alertes, parsing, agrégation, enrichissement externe (AbuseIPDB), corrélation avec l'inventaire, notification des analystes (Slack/Teams/Webhook) et création automatique d'un ticket d'incident (Jira/TheHive).
- **Semi-Automatique (Recommandé pour la remédiation) :** Pour les actions d'endiguement à fort impact (bannissement d'une IP sur le pare-feu, isolation d'un poste Windows hôte, désactivation d'un compte utilisateur). Le pipeline prépare le contexte complet, génère la recommandation d'action et propose un bouton "Valider / Bloquer" à l'analyste SOC.
- **Manuel :** Pour les décisions hautement stratégiques nécessitant une compréhension métier approfondie : coupure d'un service critique de production, restauration complète d'un serveur ou communication externe d'incident de sécurité (CSIRT/ANSSI/Direction).

---

## 📊 Synthèse : Limites de l'automatisation en environnement SOC

Bien que l'automatisation permette de réduire drastiquement le bruit (ex. passer de 96 alertes brutes à 6 groupes d'adresses suspectes en quelques millisecondes), les limites fondamentales observées sont :

1. **La rigidité des seuils statiques :** Un seuil fixe ne détecte pas les attaques lentes et distribuées (*low-and-slow*) tout en pénalisant des erreurs humaines bénignes.
2. **La dépendance envers les services tiers :** Dépendance critique envers la connectivité et les quotas des API de Threat Intelligence.
3. **Le manque de contexte métier intrinsèque :** Seule une corrélation avec un inventaire d'actifs maintenu et une validation humaine permettent d'éviter les faux positifs dévastateurs.

---

## 👤 Auteur

* **Issam ECHAHBOUNI**  
* DUT Cybersécurité et audit des systèmes d'information  
* École Supérieure de Technologie de Tétouan — Université Abdelmalek Essaâdi (2026–2027)  
* Module : **Introduction au SOC et supervision**
