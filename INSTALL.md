# Installation (Development)

## Voraussetzungen

- Python 3.x
- Node.js / npm

## Setup

### 1. Virtualenv anlegen und aktivieren

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Python-Abhängigkeiten installieren

```bash
pip install -r web/requirements.txt
```

### 3. Node-Abhängigkeiten installieren

```bash
cd web
npm install
```

## Entwicklung

### Django-Entwicklungsserver starten

```bash
cd web
python manage.py runserver
```

Die Anwendung ist anschließend unter [http://localhost:8000](http://localhost:8000) erreichbar.

### Styles und JavaScript automatisch bauen

In einem separaten Terminal:

```bash
cd web
npm run watch
```

Damit werden Änderungen an den SCSS- und JS-Dateien automatisch erkannt und neu gebaut.
