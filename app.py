#!/usr/bin/env python3
"""
Shopping list web app.

Add, check off, and delete items in a simple list. Items persist to a
Supabase (Postgres) table so the list survives across restarts and devices.

Single-command usage: `python3 app.py`, then open http://127.0.0.1:5000/
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

app = Flask(__name__)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "shopping_items"


def load_items():
    res = supabase.table(TABLE).select("id, text, checked").order("id").execute()
    return res.data


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

    res = (
        supabase.table(TABLE)
        .insert({"text": text, "checked": False})
        .execute()
    )
    return jsonify(res.data[0]), 201


@app.route("/api/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    payload = request.get_json(silent=True) or {}
    updates = {}
    if "checked" in payload:
        updates["checked"] = bool(payload["checked"])
    if "text" in payload:
        updates["text"] = payload["text"]

    if not updates:
        return jsonify({"error": "nothing to update"}), 400

    res = (
        supabase.table(TABLE)
        .update(updates)
        .eq("id", item_id)
        .execute()
    )
    if not res.data:
        return jsonify({"error": "item not found"}), 404
    return jsonify(res.data[0])


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    res = supabase.table(TABLE).delete().eq("id", item_id).execute()
    if not res.data:
        return jsonify({"error": "item not found"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
