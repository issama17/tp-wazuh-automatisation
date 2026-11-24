import base64
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright
import pypdf

def get_base64_image(image_path: str) -> str:
    path = Path(image_path)
    suffix = path.suffix.lower().replace('.', '')
    mime = 'jpeg' if suffix in ['jpg', 'jpeg'] else 'png'
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:image/{mime};base64,{data}"

img1_b64 = get_base64_image("img/capture1_execution_console.jpg")
img2_b64 = get_base64_image("img/capture2_webhook_reception.png")
img3_b64 = get_base64_image("img/capture3_rapport_excel.jpg")
img4_b64 = get_base64_image("img/capture4_manager_live_alerts_ssh.jpg")
img5_b64 = get_base64_image("img/capture5_abuseipdb_enrichment.jpg")
img6_b64 = get_base64_image("img/capture6_live_alerts_execution.jpg")
img7_b64 = get_base64_image("img/capture7_active_response_audit_log.png")

html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Compte rendu de TP – Automatisation et enrichissement des alertes Wazuh</title>
    <style>
        @page {{
            size: A4;
            margin: 14mm 14mm 15mm 14mm;
            @bottom-right {{
                content: counter(page);
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 8.5pt;
                color: #7f8c8d;
            }}
            @bottom-left {{
                content: "EST Tétouan • DUT Cybersécurité | Module : Introduction au SOC et supervision";
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 8pt;
                color: #7f8c8d;
            }}
        }}

        @page :first {{
            margin: 0;
            @bottom-right {{ content: none; }}
            @bottom-left {{ content: none; }}
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
            color: #2c3e50;
            line-height: 1.45;
            font-size: 9.5pt;
            margin: 0;
            padding: 0;
        }}

        .page-break {{
            page-break-before: always;
        }}

        /* PAGE DE GARDE */
        .cover-page {{
            padding: 45px 50px 40px 50px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
            background: #ffffff;
        }}

        .univ-header {{
            text-align: center;
            border-bottom: 2.5px solid #1a5276;
            padding-bottom: 15px;
        }}

        .univ-name {{
            font-size: 14.5pt;
            font-weight: 700;
            color: #1a5276;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}

        .school-name {{
            font-size: 12pt;
            font-weight: 600;
            color: #34495e;
            margin-top: 3px;
        }}

        .dept-name {{
            font-size: 10pt;
            color: #7f8c8d;
            font-weight: 500;
            margin-top: 3px;
        }}

        .cover-body {{
            margin: auto 0;
            text-align: center;
        }}

        .doc-badge {{
            display: inline-block;
            background-color: #e74c3c;
            color: #ffffff;
            font-size: 10.5pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding: 5px 16px;
            border-radius: 4px;
            margin-bottom: 18px;
        }}

        .cover-title-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #eef2f5 100%);
            border: 1px solid #d5dbdb;
            border-left: 7px solid #1a5276;
            border-radius: 6px;
            padding: 30px 22px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        }}

        .main-title {{
            font-size: 20.5pt;
            font-weight: 800;
            color: #1a5276;
            margin: 0 0 10px 0;
            line-height: 1.25;
            letter-spacing: -0.3px;
        }}

        .sub-title {{
            font-size: 11pt;
            color: #4a6572;
            font-weight: 600;
            margin: 0;
        }}

        .pipeline-tags {{
            margin-top: 20px;
        }}

        .tag {{
            display: inline-block;
            background: #1a5276;
            color: white;
            font-size: 8.5pt;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 14px;
            margin: 2px 3px;
        }}

        .cover-footer {{
            border-top: 1.5px solid #d5dbdb;
            padding-top: 18px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}

        .author-box {{
            text-align: left;
        }}

        .author-label {{
            font-size: 8.5pt;
            color: #7f8c8d;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}

        .author-name {{
            font-size: 13pt;
            font-weight: 700;
            color: #1a5276;
            margin: 3px 0 1px 0;
        }}

        .author-desc {{
            font-size: 9pt;
            color: #5d6d7e;
        }}

        .meta-box {{
            text-align: right;
            font-size: 9.5pt;
        }}

        .meta-line {{
            margin: 2px 0;
        }}

        /* SECTIONS DE CONTENU */
        h1 {{
            color: #1a5276;
            font-size: 12.5pt;
            border-bottom: 2px solid #2980b9;
            padding-bottom: 4px;
            margin-top: 14px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            page-break-after: avoid;
        }}

        h2 {{
            color: #2c3e50;
            font-size: 10.5pt;
            margin-top: 10px;
            margin-bottom: 4px;
            border-left: 3.5px solid #3498db;
            padding-left: 7px;
            page-break-after: avoid;
        }}

        h3 {{
            color: #34495e;
            font-size: 9.5pt;
            margin-top: 8px;
            margin-bottom: 3px;
            font-weight: 700;
            page-break-after: avoid;
        }}

        p {{
            margin: 4px 0;
            text-align: justify;
        }}

        ul, ol {{
            margin: 3px 0 5px 0;
            padding-left: 18px;
        }}

        li {{
            margin-bottom: 2px;
        }}

        /* TABLEAUX */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 7px 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #bdc3c7;
            padding: 4px 6px;
            text-align: left;
        }}

        th {{
            background-color: #1a5276;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 7.5pt;
            letter-spacing: 0.4px;
        }}

        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        /* CALLOUTS */
        .callout {{
            background-color: #eaf2f8;
            border-left: 4px solid #2980b9;
            padding: 6px 10px;
            margin: 6px 0;
            border-radius: 0 4px 4px 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }}

        .callout-title {{
            font-weight: 700;
            color: #1a5276;
            margin-bottom: 2px;
        }}

        /* CAPTURES */
        .figure-container {{
            margin: 8px 0;
            text-align: center;
            page-break-inside: avoid;
        }}

        .figure-container img {{
            max-width: 96%;
            max-height: 200px;
            width: auto;
            border: 1px solid #ccd1d9;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        }}

        .figure-caption {{
            font-size: 8pt;
            color: #5d6d7e;
            font-weight: 600;
            margin-top: 3px;
            font-style: italic;
        }}

        /* CODE BLOCK */
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 6px 9px;
            border-radius: 4px;
            font-size: 7.5pt;
            font-family: 'Consolas', monospace;
            overflow-x: auto;
            margin: 5px 0;
            line-height: 1.3;
            page-break-inside: avoid;
        }}

        code.inline {{
            background-color: #eaeded;
            color: #c0392b;
            padding: 1px 3px;
            border-radius: 3px;
            font-size: 8pt;
            font-family: 'Consolas', monospace;
        }}

        /* QUESTIONS REPONSES */
        .qa-block {{
            margin-bottom: 6px;
            background-color: #ffffff;
            border: 1px solid #e0e4e7;
            border-left: 3.5px solid #1a5276;
            border-radius: 3px;
            padding: 6px 10px;
            page-break-inside: avoid;
        }}

        .qa-question {{
            font-weight: 700;
            color: #1a5276;
            margin-bottom: 2px;
            font-size: 9pt;
        }}

        .qa-answer {{
            font-size: 8.5pt;
            color: #34495e;
            text-align: justify;
        }}

        .qa-answer ul {{
            margin: 2px 0;
            padding-left: 16px;
        }}

        .toc-item {{
            display: flex;
            justify-content: space-between;
            padding: 3px 0;
            border-bottom: 1px dotted #bdc3c7;
            font-size: 9pt;
        }}

        .toc-title {{
            font-weight: 600;
            color: #1a5276;
        }}

        .toc-dots {{
            flex-grow: 1;
            border-bottom: 1px dotted #95a5a6;
            margin: 0 8px 3px 8px;
        }}
    </style>
</head>
<body>

    <!-- PAGE 1 : COUVERTURE -->
    <div class="cover-page">
        <div class="univ-header">
            <div class="univ-name">Université Abdelmalek Essaâdi</div>
            <div class="school-name">École Supérieure de Technologie de Tétouan</div>
            <div class="dept-name">Département Informatique • DUT Cybersécurité et audit des systèmes d'information</div>
        </div>

        <div class="cover-body">
            <div class="doc-badge">Compte rendu de travaux pratiques</div>
            <div class="cover-title-card">
                <h1 class="main-title">Automatisation et Enrichissement<br>des Alertes Wazuh</h1>
                <p class="sub-title">Pipeline SOC : Détection • Extraction • Agrégation temporelle • Enrichissement • Notification • Active Response</p>
                <div class="pipeline-tags">
                    <span class="tag">Wazuh SIEM</span>
                    <span class="tag">Python Automation</span>
                    <span class="tag">AbuseIPDB Threat Intel</span>
                    <span class="tag">Webhook Integration</span>
                    <span class="tag">Active Response Custom</span>
                    <span class="tag">Tailscale Cloud Mesh</span>
                </div>
            </div>
        </div>

        <div class="cover-footer">
            <div class="author-box">
                <div class="author-label">Réalisé par :</div>
                <div class="author-name">Issam ECHAHBOUNI</div>
                <div class="author-desc">Filière : DUT Cybersécurité et audit des SI</div>
            </div>
            <div class="meta-box">
                <div class="meta-line"><strong>Année Universitaire :</strong> 2026 – 2027</div>
                <div class="meta-line"><strong>Module :</strong> Introduction au SOC et supervision</div>
                <div class="meta-line"><strong>Date :</strong> 24 novembre 2026</div>
            </div>
        </div>
    </div>

    <!-- PAGE 2 : SOMMAIRE & INTRODUCTION -->
    <div class="page-break"></div>

    <h1>Table des matières</h1>
    <div style="margin: 8px 0 14px 0;">
        <div class="toc-item"><span class="toc-title">1. Introduction et Environnement de Travail Multi-Systèmes</span><span class="toc-dots"></span><span>Page 2</span></div>
        <div class="toc-item"><span class="toc-title">2. Partie A – Préparation du Jeu d'Alertes et Stratégie SOC</span><span class="toc-dots"></span><span>Page 3</span></div>
        <div class="toc-item"><span class="toc-title">3. Partie B – Conception et Architecture Modulaire du Script Python</span><span class="toc-dots"></span><span>Page 4</span></div>
        <div class="toc-item"><span class="toc-title">4. Partie C – Résultats d'Exécution, Rapports et Preuves</span><span class="toc-dots"></span><span>Page 5</span></div>
        <div class="toc-item"><span class="toc-title">5. Partie D & E – Enrichissement Réel AbuseIPDB et Alertes en Direct</span><span class="toc-dots"></span><span>Page 7</span></div>
        <div class="toc-item"><span class="toc-title">6. Partie F – Active Response Personnalisée (Optionnel / Avancé)</span><span class="toc-dots"></span><span>Page 8</span></div>
        <div class="toc-item"><span class="toc-title">7. Questions de Réflexion Approfondies (Section 13)</span><span class="toc-dots"></span><span>Page 9</span></div>
        <div class="toc-item"><span class="toc-title">8. Synthèse sur les Limites de l'Automatisation et Conclusion</span><span class="toc-dots"></span><span>Page 10</span></div>
    </div>

    <h1>1. Introduction et Environnement de Travail</h1>
    
    <h2>1.1 Contexte et Objectifs Pédagogiques</h2>
    <p>
        Dans le cadre du module <strong>Introduction au SOC et supervision</strong>, la gestion brute des flux d'événements de sécurité produit une <strong>fatigue d'alerte</strong> (*alert fatigue*) qui compromet l'efficacité opérationnelle des analystes. Sans corrélation temporelle ni qualification de menace, chaque anomalie technique apparaît comme un signal isolé.
    </p>
    <p>
        Ce TP met en place un pipeline complet d'automatisation, d'agrégation temporelle et d'enrichissement en Python conçu pour :
    </p>
    <ul>
        <li>Ingérer les alertes de sécurité au format natif Wazuh (<code class="inline">alerts.json</code> en Array JSON ou NDJSON) ;</li>
        <li>Extraire et normaliser les champs fondamentaux (timestamp, règle, sévérité, hôte, IP source, utilisateur) ;</li>
        <li>Agréger les événements par adresse IP source et fenêtre temporelle glissante (ex. tranches de 60 minutes) ;</li>
        <li>Enrichir les entités suspectes avec un score de réputation (mode heuristique Mock ou Threat Intel réel <strong>AbuseIPDB</strong>) ;</li>
        <li>Produire des rapports synthétiques horodatés au double format CSV et JSON ;</li>
        <li>Diffuser des alertes en console et expédier un payload structuré via un <strong>webhook externe</strong> (HTTP POST) ;</li>
        <li>Déployer une réponse active (<strong>Active Response</strong>) personnalisée assurant traçabilité et endiguement semi-automatisé.</li>
    </ul>

    <h2>1.2 Architecture Multi-Systèmes du Lab</h2>
    <p>
        L'infrastructure opérationnelle s'appuie sur le lab déployé lors de nos travaux pratiques précédents :
    </p>
    <table>
        <thead>
            <tr>
                <th>Machine</th>
                <th>Rôle / Service</th>
                <th>Système d'exploitation</th>
                <th>Adresse IP (Tailscale / Réseau)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>wazuh-server</strong></td>
                <td>Manager Wazuh 4.14.9, Indexer, Dashboard</td>
                <td>Ubuntu Server (VM VirtualBox)</td>
                <td>100.64.38.76 / 192.168.200.17</td>
            </tr>
            <tr>
                <td><strong>AWS-Server</strong></td>
                <td>Agent supervisé (ID 001) – Serveur cloud applicatif</td>
                <td>Ubuntu 22.04 LTS (AWS Lightsail)</td>
                <td>100.120.55.48 (Public: 13.39.3.250)</td>
            </tr>
            <tr>
                <td><strong>windows-host</strong></td>
                <td>Agent supervisé (ID 002) – Poste client & Sysmon</td>
                <td>Windows 10 Pro (Poste hôte)</td>
                <td>100.95.52.73 / 192.168.3.200</td>
            </tr>
            <tr>
                <td><strong>kali-lab</strong></td>
                <td>Machine d'attaque (simulation brute force)</td>
                <td>Kali Linux (VM de test)</td>
                <td>129.159.197.13 / 100.121.101.97</td>
            </tr>
        </tbody>
    </table>

    <div class="callout">
        <div class="callout-title">Remarque d'architecture :</div>
        Les agents communiquent avec le manager via le réseau maillé chiffré <strong>Tailscale</strong>. Les ports de collecte 1514 et d'enrôlement 1515 ne sont jamais exposés directement sur l'Internet public.
    </div>

    <!-- PAGE 3 : PARTIE A -->
    <div class="page-break"></div>

    <h1>2. Partie A – Préparation du Jeu d'Alertes et Stratégie SOC</h1>

    <h2>2.1 Approche Méthodologique : Le Jeu de Données Élargi</h2>
    <p>
        Dans un lab isolé, le volume naturel d'alertes est insuffisant pour évaluer la pertinence d'une agrégation temporelle et d'un seuil critique. Suivant la directive de l'enseignant, nous avons conçu un jeu de données représentatif de <strong>96 alertes Wazuh</strong> (<code class="inline">alerts_sample.json</code> et <code class="inline">alerts_sample.ndjson</code>) injectant des scénarios réalistes :
    </p>

    <table>
        <thead>
            <tr>
                <th>Scénario / Origine</th>
                <th>IP Source</th>
                <th>Volume</th>
                <th>Règles Déclenchées</th>
                <th>Comportement SOC attendu</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Brute Force SSH Externe</strong></td>
                <td><code class="inline">185.220.101.5</code> (Nœud Tor)</td>
                <td>32 alertes</td>
                <td>5710, 5712 (Niveau 10)</td>
                <td>Réparti sur 2 fenêtres (14h et 15h). Qualifié en <strong>high_risk (Score 90 / 100)</strong>.</td>
            </tr>
            <tr>
                <td><strong>Scanner Web Applicatif</strong></td>
                <td><code class="inline">45.33.32.156</code></td>
                <td>18 alertes</td>
                <td>31101, 31103, 31106, 31533</td>
                <td>Traversée, SQLi, XSS contre le serveur web. Qualifié en <strong>suspicious</strong>.</td>
            </tr>
            <tr>
                <td><strong>Attaque Kali (Lab Tailscale)</strong></td>
                <td><code class="inline">100.121.101.97</code> (kali-lab)</td>
                <td>14 alertes</td>
                <td>5710, 5712, 5503</td>
                <td>Échecs SSH + PAM répétés ciblant <code class="inline">AWS-Server</code>. Qualifié en <strong>suspicious</strong>.</td>
            </tr>
            <tr>
                <td><strong>Botnet SSH / Détection C2</strong></td>
                <td><code class="inline">194.26.29.112</code></td>
                <td>14 alertes</td>
                <td>5710, 5712</td>
                <td>Tentatives avec utilisateur <code class="inline">miner</code> dans la fenêtre de 15h. <strong>suspicious</strong>.</td>
            </tr>
            <tr>
                <td><strong>Reconnaissance LAN interne</strong></td>
                <td><code class="inline">192.168.3.150</code></td>
                <td>7 alertes</td>
                <td>60106</td>
                <td>Balayage de ports rapide détecté par Sysmon sur <code class="inline">windows-host</code>.</td>
            </tr>
            <tr>
                <td><strong>Trafic Légitime / Erreur de saisie</strong></td>
                <td><code class="inline">100.95.52.73</code> (windows-host)</td>
                <td>2 alertes</td>
                <td>5710, 5715</td>
                <td>Volume inférieur au seuil de notification ($N &lt; 5$). Non alerté.</td>
            </tr>
            <tr>
                <td><strong>Événements sans IP (Robustesse)</strong></td>
                <td><em>Aucune IP (FIM & Process)</em></td>
                <td>6 alertes</td>
                <td>550, 553, 554, 92031, 92213</td>
                <td>Modifications FIM sur <code class="inline">/opt/app</code>. Valide la tolérance aux données partielles.</td>
            </tr>
        </tbody>
    </table>

    <h2>2.2 Liaison avec le Flux d'Alertes Réel du Manager Wazuh</h2>
    <p>
        Sur le manager <code class="inline">wazuh-server</code>, le fichier <code class="inline">/var/ossec/logs/alerts/alerts.json</code> stocke en continu les alertes en format NDJSON. La commande d'extraction suivante a permis d'isoler un flux d'authentification réel généré lors de nos simulations :
    </p>
    <pre># Extraction des alertes SSH réelles sur le Manager (wazuh-server)
sudo grep -E '"id":"571[0-2]"' /var/ossec/logs/alerts/alerts.json | tail -50 > ~/live_alerts_ssh.json</pre>

    <div class="figure-container">
        <img src="{img4_b64}" alt="Extraction des alertes réelles sur wazuh-server">
        <div class="figure-caption">Capture 1 : Extraction des 50 dernières alertes SSH réelles (règles 5710/5712) sur wazuh-server</div>
    </div>
    <p>
        Ce fichier extrait contient les tentatives réelles de l'utilisateur <code class="inline">fakeuser</code> depuis la machine Kali (<code class="inline">129.159.197.13</code>), démontrant la continuité entre la collecte système et le script d'automatisation.
    </p>

    <!-- PAGE 4 : PARTIE B -->
    <div class="page-break"></div>

    <h1>3. Partie B – Conception et Implémentation du Pipeline Python</h1>

    <h2>3.1 Architecture Modulaire du Projet</h2>
    <p>
        Le projet adopte une structure modulaire respectant les principes de responsabilité unique (SOLID) :
    </p>
    <pre>tp_wazuh_starter/
├── alerts_sample.json       # Dataset d'alertes (Format Array JSON classique)
├── alerts_sample.ndjson     # Dataset d'alertes (Format NDJSON / ligne par ligne)
├── live_alerts_ssh.json     # Flux réel d'alertes SSH extrait du Manager Wazuh
├── parser.py                # Ingestion multi-format et extraction sécurisée des champs
├── aggregator.py            # Agrégation temporelle par couple (IP source, bucket temporel)
├── enricher.py              # Qualification de réputation (Heuristique Mock + API AbuseIPDB)
├── reporter.py              # Export des rapports synthétiques horodatés (CSV et JSON)
├── notifier.py              # Affichage console formaté et émission du Webhook HTTP POST
├── main.py                  # Point d'entrée CLI et orchestration du workflow
├── active_response/         # Scripts de remédiation Active Response
│   └── custom-ar-audit.py   # Script de traçabilité et réponse active semi-automatique
└── reports/                 # Dossier recevant les rapports d'audit générés</pre>

    <h2>3.2 Rôle des Modules</h2>
    <ul>
        <li>
            <strong><code class="inline">parser.py</code> (Ingestion & Extraction) :</strong> 
            La fonction <code class="inline">load_alerts()</code> tente de décoder le fichier sous forme de tableau JSON. En cas d'échec (<code class="inline">JSONDecodeError</code>), elle lit le fichier ligne par ligne (NDJSON). La fonction <code class="inline">extract_fields()</code> utilise des méthodes <code class="inline">.get()</code> pour extraire en toute sécurité l'horodatage, l'ID de règle, la sévérité, l'hôte, et l'adresse IP source (<code class="inline">data.srcip</code>).
        </li>
        <li>
            <strong><code class="inline">aggregator.py</code> (Agrégation temporelle) :</strong> 
            Parse les timestamps ISO 8601 (gestion du suffixe 'Z' UTC) et regroupe les événements dans des créneaux temporels calculés par <code class="inline">minute = (ts.minute // window) * window</code>. Pour chaque bucket, le module calcule le nombre total d'événements, la sévérité maximale, et compile les listes uniques d'hôtes et de règles.
        </li>
        <li>
            <strong><code class="inline">enricher.py</code> (Enrichissement & Threat Intel) :</strong> 
            Intègre deux modes :
            <ul>
                <li><em>Mock :</em> Attribue un score déterministe ($N \ge 20 \rightarrow$ <strong>high_risk / score 90</strong>, $N \ge 5 \rightarrow$ <strong>suspicious / score 60</strong>, sinon <strong>low / score 20</strong>).</li>
                <li><em>AbuseIPDB :</em> Interroge l'API v2 avec clé d'environnement (<code class="inline">.env</code>), cache local en mémoire pour limiter les requêtes, détection des IP privées/locales pour éviter les erreurs d'appel, et repli automatique (*graceful fallback*) sur le mode mock si l'API est indisponible.</li>
            </ul>
        </li>
        <li>
            <strong><code class="inline">reporter.py</code> (Export d'audit) :</strong> 
            Écrit simultanément un rapport JSON structuré et un fichier CSV horodaté (<code class="inline">alert_summary_YYYYMMDD_HHMMSS</code>), avec détection automatique des colonnes d'enrichissement.
        </li>
        <li>
            <strong><code class="inline">notifier.py</code> (Diffusion) :</strong> 
            Affiche un tableau clair des adresses suspectes dépassant le seuil configuré et envoie une requête HTTP POST au service webhook spécifié avec un payload JSON compact.
        </li>
    </ul>

    <!-- PAGE 5 : PARTIE C - RESULTATS -->
    <div class="page-break"></div>

    <h1>4. Partie C – Résultats d'Exécution et Preuves</h1>

    <h2>4.1 Exécution Principale et Notification Console</h2>
    <p>
        L'exécution a été réalisée en PowerShell avec une fenêtre de 60 minutes, un seuil d'alerte de 5 événements, et l'URL du webhook de test généré sur <code class="inline">webhook.site</code> :
    </p>
    <pre>python main.py -i alerts_sample.json -w 60 -t 5 --webhook https://webhook.site/6dfe92b1-f2f3-47cf-a4a8-53711e751e69</pre>

    <div class="figure-container">
        <img src="{img1_b64}" alt="Sortie console du script Python">
        <div class="figure-caption">Capture 2 : Sortie console de main.py – Parsing, agrégation, enrichissement mock et notification console</div>
    </div>

    <p>
        <strong>Constats opérationnels :</strong> Sur <strong>96 alertes</strong>, 90 possèdent une adresse IP source (les 6 alertes FIM sans IP sont écartées gracieusement). Le partitionnement produit <strong>8 groupes IP/période</strong>, avec l'attaquant <code class="inline">185.220.101.5</code> présent sur deux fenêtres temporelles distinctes (14h00 et 15h00), confirmant la précision de l'agrégation.
    </p>

    <!-- PAGE 6 : EXCEL & WEBHOOK -->
    <div class="page-break"></div>

    <h2>4.2 Analyse du Rapport Synthétique CSV sous Excel</h2>
    <div class="figure-container">
        <img src="{img3_b64}" alt="Rapport CSV ouvert sous Excel">
        <div class="figure-caption">Capture 3 : Rapport CSV généré ouvert sous Microsoft Excel – Synthèse complète des 8 groupes</div>
    </div>
    <p>
        Le rapport tabulaire affiche l'ensemble des groupes d'adresses. Les IP en dessous du seuil (<code class="inline">198.51.100.23</code> avec 3 événements et <code class="inline">100.95.52.73</code> avec 2 événements) sont conservées avec le tag <code class="inline">low</code> pour archivage et traçabilité.
    </p>

    <h2>4.3 Validation de la Réception du Webhook Externe</h2>
    <div class="figure-container">
        <img src="{img2_b64}" alt="Réception du Webhook sur webhook.site">
        <div class="figure-caption">Capture 4 : Notification HTTP POST reçue sur webhook.site avec payload JSON enrichi</div>
    </div>
    <p>
        La requête a été enregistrée à 10:10:23 AM depuis notre connexion publique (Maroc Telecom, Tétouan), transportant le payload JSON contenant les 6 adresses critiques, leurs cibles et leurs niveaux de réputation.
    </p>

    <!-- PAGE 7 : PARTIE D & E - ABUSEIPDB & LIVE ALERTS -->
    <div class="page-break"></div>

    <h1>5. Partie D & E – Enrichissement Réel AbuseIPDB et Alertes Réelles</h1>

    <h2>5.1 Enrichissement Réel via l'API AbuseIPDB</h2>
    <p>
        Nous avons configuré une clé d'API AbuseIPDB v2 dans un fichier d'environnement <code class="inline">.env</code> et exécuté le script avec l'option <code class="inline">--enrich abuseipdb</code> :
    </p>
    <pre>python main.py -i alerts_sample.json --enrich abuseipdb</pre>

    <div class="figure-container">
        <img src="{img5_b64}" alt="Enrichissement AbuseIPDB réel">
        <div class="figure-caption">Capture 5 : Enrichissement réel via l'API AbuseIPDB – Attribution du score maximal 100 pour l'IP 185.220.101.5</div>
    </div>

    <p>
        <strong>Analyse de la Threat Intelligence :</strong>
    </p>
    <ul>
        <li>L'adresse publique <code class="inline">185.220.101.5</code> (nœud de sortie Tor) est interrogée en direct et reçoit un score d'abus réel de <strong>100 %</strong> sur AbuseIPDB, ce qui la classe immédiatement en <strong>high_risk</strong>.</li>
        <li>Les adresses privées du lab (<code class="inline">100.121.101.97</code> sur Tailscale et <code class="inline">192.168.3.150</code> sur LAN) sont filtrées par notre fonction <code class="inline">is_public_ip()</code>, évitant les erreurs HTTP 422 de l'API externe et qualifiées en mode heuristique sécurisé.</li>
    </ul>

    <h2>5.2 Traitement des Alertes Réelles du Manager (<code class="inline">live_alerts_ssh.json</code>)</h2>
    <p>
        Après extraction des logs réels du Manager (<code class="inline">live_alerts_ssh.json</code>), nous avons exécuté le script d'automatisation sur ce flux direct :
    </p>
    <pre>python main.py -i live_alerts_ssh.json -w 60 -t 3</pre>

    <div class="figure-container">
        <img src="{img6_b64}" alt="Exécution sur les alertes réelles en direct">
        <div class="figure-caption">Capture 6 : Analyse du flux d'alertes réelles live_alerts_ssh.json – Détection de la machine Kali (129.159.197.13)</div>
    </div>

    <p>
        Le script isole immédiatement l'adresse IP de notre machine d'attaque Kali (<code class="inline">129.159.197.13</code>) avec 12 échecs d'authentification sur <code class="inline">AWS-Server</code>, confirmant l'efficacité du pipeline sur des alertes de production.
    </p>

    <!-- PAGE 8 : PARTIE F - ACTIVE RESPONSE -->
    <div class="page-break"></div>

    <h1>6. Partie F – Active Response Personnalisée (Bonus)</h1>

    <h2>6.1 Déploiement et Déclenchement Automatique de l'Active Response</h2>
    <p>
        Nous avons déployé le script Python <code class="inline">custom-ar-audit.py</code> dans <code class="inline">/var/ossec/active-response/bin/</code> sur le Manager <code class="inline">wazuh-server</code> avec les permissions d'exécution appropriées (<code class="inline">chmod 755</code>), puis configuré la réponse active avec la balise <code class="inline">&lt;location&gt;server&lt;/location&gt;</code> pour les règles SSH 5710 et 5712 :
    </p>

    <div class="figure-container">
        <img src="{img7_b64}" alt="Journal d'audit Active Response en direct">
        <div class="figure-caption">Capture 7 : Déclenchement automatique de l'Active Response à 12:08:19 – Audit et décision semi-automatique sur l'attaque Kali</div>
    </div>

    <p>
        <strong>Validation de la chaîne de réponse active :</strong>
    </p>
    <ul>
        <li>Lors de la tentative SSH initiée depuis la machine Kali (<code class="inline">129.159.197.13</code>) vers <code class="inline">AWS-Server</code> à <strong>12:08:19 UTC</strong>, le Manager Wazuh a instantanément exécuté notre script personnalisé.</li>
        <li>L'entrée d'audit confirme l'extraction exacte des métadonnées (<code class="inline">Règle=5710</code>, <code class="inline">Agent=AWS-Server (001)</code>, <code class="inline">IP=129.159.197.13</code>) et consigne la recommandation d'endiguement pare-feu (<code class="inline">iptables -I INPUT -s 129.159.197.13 -j DROP</code>) en attente de validation SOC.</li>
    </ul>

    <!-- PAGE 9 : QUESTIONS DE REFLEXION -->
    <div class="page-break"></div>

    <h1>7. Questions de Réflexion Approfondies (Section 13)</h1>

    <div class="qa-block">
        <div class="qa-question">1. Pourquoi l’enrichissement (asset + user + IOC) change-t-il la priorité d’une alerte ?</div>
        <div class="qa-answer">
            Une alerte brute n'indique qu'un fait technique isolé. L'enrichissement lui apporte sa valeur contextuelle :
            <ul>
                <li><strong>Asset (Criticité de la cible) :</strong> Un échec SSH sur un honeypot de test est anodin (priorité P4), alors que la même alerte ciblant le serveur de base de données de production ou le contrôleur de domaine représente une urgence absolue (P1).</li>
                <li><strong>User (Privilèges du compte) :</strong> Cibler un utilisateur inconnu est souvent un bruit de fond, alors qu'une attaque répétée sur <code class="inline">root</code> ou un compte de service sensible dénote une tentative d'élévation ciblée.</li>
                <li><strong>IOC (Threat Intelligence) :</strong> Savoir que l'IP est un nœud de sortie Tor ou un serveur malveillant répertorié sur AbuseIPDB transforme instantanément une suspicion en incident confirmé.</li>
            </ul>
        </div>
    </div>

    <div class="qa-block">
        <div class="qa-question">2. Quels risques y a-t-il à bloquer automatiquement une IP à partir d’un simple compteur ?</div>
        <div class="qa-answer">
            Le blocage automatique basé sur un compteur statique ($N \ge 5$) présente trois dangers majeurs :
            <ul>
                <li><strong>Déni de service induit (Self-DoS par usurpation) :</strong> Un attaquant peut usurper (IP spoofing en UDP/DNS) l'adresse d'un serveur légitime (passerelle par défaut, serveur DNS d'entreprise, proxy) pour forcer le pare-feu à bloquer ses propres ressources vitales.</li>
                <li><strong>Impact sur les passerelles partagées (NAT / CGNAT) :</strong> Des centaines d'utilisateurs légitimes d'une entreprise, d'une université ou d'un réseau mobile partagent une unique IP publique. Bannir cette IP déconnecte l'ensemble des usagers.</li>
                <li><strong>Blocage d'outils d'audit légitimes :</strong> Les scanners de vulnérabilité internes (ex. Nessus, Qualys) génèrent d'importants volumes de requêtes et risquent d'être isolés par inadvertance.</li>
            </ul>
        </div>
    </div>

    <div class="qa-block">
        <div class="qa-question">3. Comment distinguerez-vous un scan légitime (vulnérabilité management) d’une attaque réelle ?</div>
        <div class="qa-answer">
            La distinction repose sur trois éléments d'analyse :
            <ul>
                <li><strong>Adresses déclarées et planification (Whitelisting) :</strong> Les audits internes sont exécutés depuis des adresses IP fixes déclarées au SOC et selon un calendrier prédéfini (fenêtres de maintenance).</li>
                <li><strong>Comportement post-découverte :</strong> Un scanner d'audit répertorie les bannières et vulnérabilités sans tenter d'injecter une charge utile active (web shell, dropper) ni d'établir une persistance, contrairement à une attaque réelle qui cherche à s'infiltrer et pivoter.</li>
                <li><strong>Signatures applicatives :</strong> Les outils homologués renseignent généralement un User-Agent ou des en-têtes HTTP spécifiques.</li>
            </ul>
        </div>
    </div>

    <div class="qa-block">
        <div class="qa-question">4. Que se passe-t-il si l’API d’enrichissement (AbuseIPDB, MISP…) est indisponible ?</div>
        <div class="qa-answer">
            Une panne réseau, une erreur 5xx ou un dépassement de quota (HTTP 429) peut figer le pipeline en cas de requêtes bloquantes. Pour y remédier, notre implémentation utilise un timeout strict (<code class="inline">timeout=8s</code>), un cache local évitant les requêtes redondantes, et un repli gracieux (*graceful fallback*) vers un score calculé en local (mode mock).
        </div>
    </div>

    <div class="qa-block">
        <div class="qa-question">5. Où placeriez-vous la validation humaine dans votre pipeline (auto / semi-auto / manuel) ?</div>
        <div class="qa-answer">
            <ul>
                <li><strong>Automatique :</strong> Ingestion, filtrage, agrégation, enrichissement et notification (Slack/Webhook) sans intervention humaine.</li>
                <li><strong>Semi-automatique (Recommandé pour l'endiguement) :</strong> Blocage IP, isolation d'hôte ou désactivation de compte via une validation en un clic soumise à l'analyste SOC avec le contexte préparé.</li>
                <li><strong>Manuel :</strong> Actions critiques irréversibles (coupure de services de production, restauration d'annuaire, communication de crise).</li>
            </ul>
        </div>
    </div>

    <!-- PAGE 10 : SYNTHESE ET CONCLUSION -->
    <div class="page-break"></div>

    <h1>8. Synthèse sur les Limites de l'Automatisation et Conclusion</h1>

    <h2>8.1 Limites Fondamentales Observées</h2>
    <p>
        L'automatisation permet de traiter d'importants volumes de logs en un temps record (passage de 96 alertes brutes à 6 entités suspectes en quelques millisecondes). Néanmoins, ce TP a mis en évidence trois limites fondamentales :
    </p>
    <ol>
        <li>
            <strong>Rigidité face aux attaques lentes et distribuées (*Low-and-Slow*) :</strong><br>
            Un seuil d'agrégation fixe (ex. 5 événements en 60 min) est inefficace contre un adversaire qui espace délibérément ses requêtes ou fait tourner ses adresses à travers un botnet.
        </li>
        <li>
            <strong>Dépendance critique envers les services de Threat Intelligence :</strong><br>
            L'enrichissement externe introduit des risques de latence, de dépassement de quota et de panne réseau, nécessitant une architecture résiliente avec cache et repli local.
        </li>
        <li>
            <strong>Absence de contexte métier :</strong><br>
            Un algorithme ne peut pas distinguer une opération de maintenance légitime d'une intrusion sans un référentiel d'inventaire continuellement mis à jour et un arbitrage humain.
        </li>
    </ol>

    <h2>8.2 Conclusion Générale</h2>
    <p>
        Ce travail pratique a permis de concrétiser le flux complet d'un pipeline de détection SOC : de l'ingestion d'événements multi-systèmes (Linux, Windows) jusqu'à la notification externe enrichie et la mise en place d'une réponse active sécurisée.
    </p>
    <p>
        Nous avons validé la robustesse du code face aux données incomplètes, la pertinence de l'agrégation temporelle pour synthétiser l'information utile, et l'apport décisif de la Threat Intelligence réelle avec AbuseIPDB. Ce projet démontre qu'un système automatisé performant doit combiner la puissance du traitement algorithmique avec la vigilance de l'analyste SOC, garantissant ainsi la résilience globale du système d'information.
    </p>

    <div style="margin-top: 60px; padding: 12px; border-top: 1.5px solid #1a5276; text-align: center; font-size: 8.5pt; color: #7f8c8d;">
        Rapport de Travaux Pratiques – DUT Cybersécurité et audit des systèmes d'information – EST Tétouan (2026–2027)
    </div>

</body>
</html>
"""

html_path = Path("rapport_tp_wazuh.html")
html_path.write_text(html_content, encoding="utf-8")
print("HTML mis a jour : rapport_tp_wazuh.html")

async def convert_html_to_pdf():
    pdf_path = "Rapport_TP_Wazuh_Automatisation_Issam_ECHAHBOUNI.pdf"
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge")
        page = await browser.new_page()
        await page.goto(f"file:///{html_path.resolve()}", wait_until="networkidle")
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "14mm",
                "bottom": "15mm",
                "left": "14mm",
                "right": "14mm"
            }
        )
        await browser.close()
    
    # Check page count
    reader = pypdf.PdfReader(pdf_path)
    print(f"Rapport PDF généré avec succès : {pdf_path} (Nombre total de pages : {len(reader.pages)})")
    for i, pg in enumerate(reader.pages):
        text = pg.extract_text()
        first_line = text.split('\n')[0] if text else '[EMPTY]'
        print(f"  Page {i+1} : length={len(text)}, 1ère ligne: {first_line[:55]}")

asyncio.run(convert_html_to_pdf())
