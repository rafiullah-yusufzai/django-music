# Probearbeit – Django Music

## Die Aufgabe

Baue eine Webseite, die es Nutzern ermöglicht, ihr aktuelles Lieblingslied online darzustellen.  
Das aktuelle Lied wird über eine öffentliche Profilseite dargestellt und kann pro Nutzer in einem Login-Bereich geändert werden.  
Die Webseite soll mobil und auf dem Desktop funktionieren (responsive).  
Eine Auswahl an Liedern wird vom System bereitgestellt.  
Neue Nutzer werden über den Django-Admin oder die Kommandozeile angelegt.

### Der Code

* Halte dich an die gängigen Coding-Standards der verwendeten Sprachen.
* Verwende englische Begriffe für Namen im Code (Variablen, Klassen, Methoden, ...).
* Verwende Django und Bootstrap 5 – nutze weitere Bibliotheken/Tools, falls sie dir die Arbeit erleichtern.

### Der Aufbau

#### Startseite (/)

Die Startseite zeigt das Login-Formular und die fünf beliebtesten Lieder auf der Seite.

#### Öffentliche Profilseite (/u/:user-slug:/)

Die öffentliche Profilseite zeigt das aktuelle Lieblingslied und soll nach folgendem Muster aufgebaut sein:\
![image](./assets/frontend.png)

#### Login-Bereich (/profile/)

Im Bereich hinter dem Login kann der Nutzer seinen Namen ändern und das aktuelle Lieblingslied auswählen.

### Die Models

Die folgenden Models sollen für die Grundstruktur verwendet werden, können aber nach Bedarf erweitert werden:

* Standard-Django-User-Model mit einem Profil-Model _oder_ ein eigenes User-Model basierend auf `AbstractUser`
* Models für: Lied, Album, Künstler
* Falls nötig, weitere Models eigenständig erfassen.
* Passende Relationen der Models müssen selbst erarbeitet werden.

## Stretch Goals

Eine Auswahl an möglichen Erweiterungen (ohne Gewichtung):

### Lieblingslied aufhübschen

* Verschwommene Version des Albumcovers im Hintergrund der Seite
* Primär-/Sekundärfarben (z. B. für Lied- und Künstlername) automatisch aus dem Albumcover generieren

### Mehr Informationen beim Lieblingslied

* „Der Nutzer liebt diesen Song seit 1 Tag und 4 Stunden.“
* „x weitere Nutzer lieben diesen Song.“

### Profilsuche

* Eine Suchfunktion für Nutzer-Profile auf der Startseite

### Lieder hinzufügen

* Eine Möglichkeit für angemeldete Nutzer, neue Songs/Alben/Künstler vorzuschlagen oder anzulegen

### Nutzer-Registrierung

* Nutzer können sich selbstständig auf der Seite registrieren.
* Registrierungsformular

### API

* Endpunkte für Lieder, Alben und Künstler
* Authentifizierung für API-Anfragen
* eigenes Lieblingslied festlegen