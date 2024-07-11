from flask import Flask, render_template, request, redirect, url_for, session
import random
import json

app = Flask(__name__)
app.secret_key = b"=(7\x06't\xf7.*Z\x9c9\x19B\x15\xae\x13\xae\xd1\x10:\xff\x90\x02"


def load_khodams():
    with open("khodams.json", "r") as f:
        return json.load(f)


# Fungsi untuk menulis khodams ke file JSON
def save_khodams(khodams):
    with open("khodams.json", "w") as f:
        json.dump(khodams, f, indent=4)


@app.route("/")
def home():
    return redirect(url_for("cek_khodam"))


@app.route("/cek-khodam", methods=["GET", "POST"])
def cek_khodam():
    khodams = load_khodams()
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            random_word = random.choice(khodams)

            session["query"] = query
            session["random_word"] = random_word
        return redirect(url_for("cek_khodam_hasil"))
    return render_template("cek_khodam.html")


@app.route("/cek-khodam/hasil", methods=["GET", "POST"])
def cek_khodam_hasil():
    query = session.get("query")
    random_word = session.get("random_word", "-")
    return render_template("hasil.html", random_word=random_word, query=query)


@app.route("/tambah-khodam", methods=["POST"])
def tambah_khodam():
    khodams = load_khodams()
    khodam_baru = request.form.get("query_khodam")
    if khodam_baru:
        khodams.append(khodam_baru)
        save_khodams(khodams)
    return redirect(url_for("cek_khodam_hasil"))


if __name__ == "__main__":
    app.run(debug=True)
