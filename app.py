from flask import Flask, render_template, request, redirect
import datetime
from pymongo import MongoClient



def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://andrew:Gogogo20!@cluster0.sbxem.mongodb.net/test")

    app.db = client.microblog


    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            entry_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert({"content": entry_content,
                                   "date": entry_date})
            return redirect("/")
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_date)
    return app

