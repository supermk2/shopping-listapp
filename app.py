#!/usr/bin/env python3
"""
Shopping list web app.

Add, check off, and delete items in a simple list. Items persist to a
JSON file on disk so the list survives across restarts.

Single-command usage: `python3 app.py`, then open http://127.0.0.1:5000/
"""

import json
import os

from flask import Flask, jsonify, render_template, request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "shopping_list.json")

app = Flask(__name__)


def load_items():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def next_id(items):
    return max((item["id"] for item in items), default=0) + 1


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/items", methods=["GET"])
def list_items():
    return jsonify(load_items())


@app.route("/api/items", methods=["POST"])
def add_item():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400

    items = load_items()
    item = {"id": next_id(items), "text": text, "checked": False}
    items.append(item)
    save_items(items)
    return jsonify(item), 201


@app.route("/api/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    payload = request.get_json(silent=True) or {}
    items = load_items()
    for item in items:
        if item["id"] == item_id:
            if "checked" in payload:
                item["checked"] = bool(payload["checked"])
            save_items(items)
            return jsonify(item)
    return jsonify({"error": "item not found"}), 404


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    items = load_items()
    remaining = [item for item in items if item["id"] != item_id]
    if len(remaining) == len(items):
        return jsonify({"error": "item not found"}), 404
    save_items(remaining)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
