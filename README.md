2. Dokumentation für das Entwicklerteam (README)
2.1 Titel & Beschreibung
the NBA house ist eine Webanwendung, die NBA-Teamroster und Spielerstatistiken über die nba_api-Bibliothek abruft und in einer Flask-Applikation darstellt.
2.2 Installation & Setup
Voraussetzungen:
• Python 3.9 oder neuer
• pip (Python-Paketmanager)
Schritt 1 – Repository klonen:
git clone https://github.com/dein-username/nba-house.git
cd nba-house
Schritt 2 – Abhängigkeiten installieren:
pip install flask flask-cors nba_api
Schritt 3 – Applikation starten:
python app.py
Die Anwendung ist danach unter http://127.0.0.1:5000 erreichbar.
2.3 Projektstruktur
Datei / Ordner Beschreibung
app.py Flask-Backend: Routen, API-Endpunkte, Server-Logik
templates/index.html Startseite – Raster aller 30 NBA-Team-Logos
templates/team.html Teamseite – Roster mit Position und Eintrittsjahr
templates/player.html Spielerseite – Karriere, Saisons, Spiellog
static/style.css Globales Stylesheet für alle Seiten
 
2.4 API-Endpunkte
Endpunkt Methode Beschreibung
/ GET Startseite – Team-Logo-Raster
/team/<team_id> GET Teamseite für das gewählte Team
/team/<team_id>/player/<player_id> GET Spielerseite für den gewählten Spieler
/api/search?q= GET Suche nach Spieler per Name
/api/player/<id>/info GET Basisinfos eines Spielers (Team, Position, etc.)
/api/player/<id>/career GET Saisonweise Karrierestatistiken
/api/player/<id>/gamelog GET Letzten 20 Spiele der aktuellen Saison
/api/team/<id>/info GET Basisinfos eines Teams (Name, Kürzel, Stadt)
/api/team/<id>/roster GET Aktueller Roster mit Eintrittsjahr
 
2.5 Abhängigkeiten
• flask – Web-Framework für Python
• flask-cors – CORS-Unterstützung für die Flask-API
• nba_api – Inoffizielle Python-Bibliothek für NBA-Statistiken (stats.nba.com)
 
2.6 Bekannte Einschränkungen
• Die NBA API hat ein Rate-Limit: Zu viele Anfragen in kurzer Zeit führen zu Timeouts.
• Die Teamseite lädt langsamer, da pro Spieler eine separate API-Anfrage für das Eintrittsjahr gestellt wird.
• Spieler ohne NBA-CDN-Headshot werden ohne Bild angezeigt.
 
