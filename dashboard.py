# Written by Timothy Mtonga
# This is the main thread for the application
# !/usr/bin/python
import os
from flask import Flask, render_template

app = Flask(__name__, template_folder="views", static_folder="assets")


@app.route("/")
def index():
    file_names = get_current_image_names()
    return render_template("index.html", image_list=file_names)


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
