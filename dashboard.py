# Written by Timothy Mtonga
# This is the main thread for the application
# !/usr/bin/python
import os
import json, ast
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="views", static_folder="assets")


# Root page for the dashboard
@app.route("/")
def index():
    file_names = get_current_image_names()

    try:
        with open("config/app.config") as json_file:
            settings = json.load(json_file)
        with open("config/metabase_exports.json") as grouping:
            image_sets = json.load(grouping)
    finally:
        pass

    return render_template("index.html", image_list=file_names, config=settings,
                            screens=ast.literal_eval(json.dumps(image_sets)))


# Configuration page for the dashboard
@app.route("/config", methods=["POST", "GET"])
def config():
    settings = {}
    try:
        with open("config/app.config") as json_file:
            settings = json.load(json_file)
    finally:
        pass

    if request.method == "POST":
        with open("config/app.config", 'w') as config_file:
            json.dump(request.form, config_file)
            config_file.close()

    return render_template("config.html", config=settings)


# Function to get list of images for display
def get_current_image_names():
    options = []
    try:
        lst = os.listdir("assets/images/screenshots/")
    except OSError:
        pass  # ignore errors
    else:
        for name in lst:
            options.append(name)

    return options


if __name__ == "__main__":
    app.run()
