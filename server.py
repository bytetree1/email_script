from flask import Flask, request, send_file, jsonify
from encrypt import encrypt_pdf
import os

app = Flask(__name__)

MASTER_PDF = "Playbook.pdf"

OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "Byte Tree PDF Server Running"


@app.route("/encrypt", methods=["POST"])
def encrypt():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    filename = email.replace("@","_").replace(".","_") + ".pdf"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    encrypt_pdf(
        MASTER_PDF,
        output_path,
        password,
        name,
        email
    )

    return send_file(
        output_path,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)