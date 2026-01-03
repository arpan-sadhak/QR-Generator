from flask import Flask, render_template, request, send_file
import qrcode
import os, time

app = Flask(__name__)

QR_PATH = os.path.join("static", "qr.png")


@app.route("/", methods=["GET", "POST"])
def index():
    qr_time = None

    if request.method == "POST":
        text = request.form.get("text")

        if text:
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=4
            )
            qr.add_data(text)
            qr.make(fit=True)
            print("....")

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(QR_PATH)

            qr_time = int(time.time())  # cache-busting

    return render_template("index.html", qr_time=qr_time)

@app.route("/download")
def download():
    return send_file(QR_PATH, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
