import os
import json
import uuid
import zipfile
import shutil
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

ADMIN_PIN = os.environ.get("ADMIN_PIN", "1234")
DATA_FILE = "games.json"
GAMES_DIR = os.path.join(os.getcwd(), "uploaded_games")

os.makedirs(GAMES_DIR, exist_ok=True)

if not os.path.exists(DATA_FILE):
    initial_games = [
        {
            "id": "preset-1",
            "title": "Neon Brick Breaker",
            "category": "Arcade",
            "tech": "HTML5 / JS",
            "plays": 240,
            "type": "embed",
            "folder": ""
        }
    ]
    with open(DATA_FILE, "w") as f:
        json.dump(initial_games, f, indent=2)

def load_games():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_games(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/api/games", methods=["GET"])
def get_games():
    return jsonify(load_games())

@app.route("/api/games/upload", methods=["POST"])
def upload_game():
    pin = request.headers.get("X-Admin-Pin") or request.form.get("pin") or (request.json and request.json.get("pin"))
    if pin != ADMIN_PIN:
        return jsonify({"success": False, "error": "Invalid Admin PIN!"}), 403

    title = request.form.get("title") or "Untitled Game"
    category = request.form.get("category") or "Arcade"
    tech = request.form.get("tech") or "HTML5 / JS"
    
    game_id = str(uuid.uuid4())[:8]
    game_folder = os.path.join(GAMES_DIR, game_id)
    os.makedirs(game_folder, exist_ok=True)

    if "file" in request.files:
        uploaded_file = request.files["file"]
        filename = uploaded_file.filename.lower()
        filepath = os.path.join(game_folder, uploaded_file.filename)
        uploaded_file.save(filepath)

        if filename.endswith(".zip"):
            with zipfile.ZipFile(filepath, "r") as zip_ref:
                zip_ref.extractall(game_folder)
            os.remove(filepath)

    elif request.is_json:
        data = request.json
        title = data.get("title", title)
        category = data.get("category", category)
        tech = data.get("tech", tech)
        html_code = data.get("code", "")
        with open(os.path.join(game_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_code)

    games = load_games()
    new_game = {
        "id": game_id,
        "title": title,
        "category": category,
        "tech": tech,
        "plays": 0,
        "type": "hosted",
        "folder": game_id
    }
    games.append(new_game)
    save_games(games)

    return jsonify({"success": True, "game": new_game})

@app.route("/games/<game_id>/", defaults={"path": "index.html"})
@app.route("/games/<game_id>/<path:path>")
def serve_uploaded_game(game_id, path):
    game_path = os.path.join(GAMES_DIR, game_id)
    return send_from_directory(game_path, path)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
