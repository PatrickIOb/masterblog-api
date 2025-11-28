# Masterblog API mit Flask

Eine minimalistische Flask-API zur Verwaltung von Blogposts, inklusive Sortierfunktion (ascending/descending) über Query-Parameter. Perfekt geeignet als Lernprojekt oder Basis für größere Webanwendungen.

## Features

* Einfache REST-API mit Flask
* Endpunkt zum Abrufen aller Posts
* Sortierung nach Feld (`title` oder `content`) und Richtung (`asc` oder `desc`)
* Saubere Strukturierung für Erweiterbarkeit

## Projektstruktur

```bash
masterblog-api/
├── app.py
├── posts.py
├── README.md
└── requirements.txt
```

## Installation

```bash
# Repository klonen
git clone https://github.com/deinname/masterblog-api.git
cd masterblog-api

# Virtuelle Umgebung erstellen (optional)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

## Starten der API

```bash
flask run --host=0.0.0.0 --port=5002
```

Die API ist dann erreichbar unter:

```
http://localhost:5002/api/posts
```

## Beispiel-Route

### GET `/api/posts`

Gibt alle Posts zurück. Optional kann sortiert werden.

#### Query-Parameter

* `sort=title|content`
* `direction=asc|desc`

#### Beispiele

```bash
# Sortierung nach Titel absteigend
http://localhost:5002/api/posts?sort=title&direction=desc

# Sortierung nach Content aufsteigend
http://localhost:5002/api/posts?sort=content&direction=asc
```

## Beispielhafte API-Antwort

```json
[
    {
        "id": 1,
        "title": "Blog Title",
        "content": "Some text"
    }
]
```

## Codeausschnitt – Sortierlogik

```python
sort_field = request.args.get("sort")
sort_direction = request.args.get("direction")

if not sort_field and not sort_direction:
    return jsonify(POSTS), 200

if sort_field not in ["title", "content"]:
    return jsonify({"error": "Invalid sort field"}), 400

reverse = sort_direction == "desc"
sorted_posts = sorted(POSTS, key=lambda post: post.get(sort_field, ""), reverse=reverse)
return jsonify(sorted_posts), 200
```

## Lizenz

MIT License – frei zur Nutzung, Modifikation und Verteilung.
