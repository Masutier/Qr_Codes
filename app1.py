import os
import json
import qrcode as qr
from PIL import Image
from flask import Flask, flash, render_template as render, redirect, request
from forms import QrCodeForm

# evaluacion
with open("static/json/qrcode.json") as config_file:
    sec_config = json.load(config_file)

PEOPLE_FOLDER = os.path.join('static/images/')

app = Flask(__name__, static_url_path='/static')
app.secret_key = sec_config['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


@app.route('/', methods=['GET', 'POST'])
def home():
    form = QrCodeForm()
    imgList = []
    qrlist = os.listdir("static/images/")

    for i in qrlist:
        imgList.append(os.path.join(app.config['UPLOAD_FOLDER'], i))

    if request.method == "POST":
        address = request.form.get("address")
        fileName = request.form.get("fileName")
        box_size = request.form.get("box_size")
        border = request.form.get("border")
        fill = request.form.get("fill")
        back_color = request.form.get("back_color")
        imgcenter = request.files.get("imgcenter")

        box_size = box_size or 10
        border = border or 3
        fill = fill or 'black'
        back_color = back_color or 'white'

        code = qr.QRCode(version=1, box_size=box_size, border=border)
        code.add_data(address)
        code.make(fit=True)
        img = code.make_image(fill=fill, back_color=back_color, colorized = True)

        if imgcenter:
            logo = Image.open(imgcenter).resize((75,75), Image.LANCZOS)
            offset = ((img.size[0] - 75) // 2, (img.size[1] - 75) // 2)
            img.paste(logo, offset, mask=logo.split()[3] if logo.mode == 'RGBA' else None)

        img.save("static/images/" + fileName + ".png")

    return render("index.html", title="Home", form=form, imgList=imgList)


if __name__ == '__main__':
    #app.run(debug=True, host="172.16.170.128", port=8080)
    app.run(debug=True, host="localhost", port=5000)
    
