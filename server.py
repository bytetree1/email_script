from flask import Flask, request, jsonify
from encrypt import encrypt_pdf
import os
import base64
import traceback

app = Flask(__name__)

MASTER_PDF = "Playbook.pdf"
OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "Byte Tree PDF Server Running"


@app.route("/encrypt", methods=["POST"])
def encrypt():
    try:
        # Read JSON
        data = request.get_json(force=True)

        print("Received JSON:", data)

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        filename = email.replace("@", "_").replace(".", "_") + ".pdf"
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        print("Generating PDF...")

        encrypt_pdf(
            MASTER_PDF,
            output_path,
            password,
            name,
            email
        )

        print("Encoding PDF...")

        with open(output_path, "rb") as pdf_file:
            pdf_data = base64.b64encode(pdf_file.read()).decode("utf-8")

        print("Done!")

        return jsonify({
            "success": True,
            "filename": filename,
            "pdf": pdf_data
        })

    except Exception as e:
        print(traceback.format_exc())

        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
