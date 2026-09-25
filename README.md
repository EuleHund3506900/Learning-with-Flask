 # Learning with Flask

Eine Flask-Webanwendung zum Speichern der Fortschritte bei den Lerninhalte aus der [Learning Repository](https://github.com/bh2005/Learning) von bh2005.

## Voraussetzungen

Für die lokale Entwicklung werden benötigt:

- Python 3.13
- Git
- eine funktionierende Python-Installation mit `venv`

Prüfe die Installationen mit:

```bash
python3.13 --version
git --version
```

## Installation

1. Repository klonen und in das Projektverzeichnis wechseln:

	```bash
	git clone <REPOSITORY-URL>
	cd learning
	```

2. Lerninhalte lokal klonen

    ```bash
    cd local_data
    git clone https://github.com/bh2005/Learning.git
    cd ..

3. Virtuelle Umgebung mit Python 3.13 erstellen:

	```bash
	python3.13 -m venv .venv
	source .venv/bin/activate
	```

	Unter Windows wird die virtuelle Umgebung mit folgendem Befehl aktiviert:

	```powershell
	.venv\Scripts\Activate.ps1
	```

4. Abhängigkeiten installieren:

	```bash
	python -m pip install --upgrade pip
	python -m pip install -r requirments.txt
	```

	Die Datei heißt im aktuellen Projekt bewusst `requirments.txt`.

## Anwendung starten

Nach der Aktivierung der virtuellen Umgebung kann die Anwendung gestartet werden:

```bash
./bin/python3 server.py
```

Die Anwendung ist anschließend unter <http://127.0.0.1:5000> erreichbar. Beim direkten Start wird die SQLite-Datenbank unter `database/development.db` initialisiert.

## Funktionen

- Anzeige der Startseite und der verfügbaren Lerninhalte
- Auflistung von Kursen, Ordnern und Markdown-Dateien
- Navigation durch die Ordnerstruktur des Verzeichnisses `local_data/Learning`
- Konvertierung und Darstellung von Markdown-Dateien als HTML
- Benutzerregistrierung mit Name, E-Mail-Adresse und bcrypt-gehashtem Passwort
- Login mit Prüfung der Zugangsdaten
- Profilansicht als Grundlage für zukünftige benutzerspezifische Funktionen
- Entwicklungsroute zum Testen der Markdown-Konvertierung

## Projektstruktur

```text
server.py                 Flask-Einstiegspunkt
blueprints/               Anwendungs-, Authentifizierungs- und Dev-Routen
database/                 SQLite-Initialisierung und Datenbankschema
templates/                HTML-Templates
static/                   CSS, JavaScript und Fonts
local_data/Learning/      Eingebundene Lerninhalte
data/                     Beispieldateien
```

## TODO

- [ ] SQLite-Speicher für Lernfortschritte, erledigte Lektionen und Kursstatus
- [ ] Authentifizierte Sessions mit JWT
- [ ] Geschützte Routen und Zugriffskontrolle für Benutzerbereiche
- [ ] Persistente Profil- und Benutzereinstellungen
- [ ] Fortschritt in der Oberfläche anzeigen und aktualisieren
- [ ] Tests für Authentifizierung, Datenbankzugriffe und zentrale Routen
- [ ] Produktionskonfiguration mit sicherem Secret Key und deaktiviertem Debug-Modus





