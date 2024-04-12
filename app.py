import os
import json
import qrcode as qr
from PIL import Image
from flask import Flask, flash, render_template as render, request, redirect, send_file
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
        fill_color = fill or 'black'
        if back_color == "#000000":
            back_color = 'white'

        code = qr.QRCode(version=1, box_size=box_size, border=border)
        code.add_data(address)
        code.make(fit=True)
        img = code.make_image(fill_color=fill_color, back_color=back_color, colorized = True)

        if imgcenter:
            logo = Image.open(imgcenter).resize((75,75), Image.LANCZOS)
            offset = ((img.size[0] - 75) // 2, (img.size[1] - 75) // 2)
            img.paste(logo, offset, mask=logo.split()[3] if logo.mode == 'RGBA' else None)

        image = "static/images/" + fileName + ".png"
        img.save(image)

        send_file(image, as_attachment=True)
        flash("El Qr se creo y se descargo muy bien!!")
        return redirect('/')

    return render("index.html", title="Home", form=form, imgList=imgList)


@app.route('/delete_history')
def delete_history():
    for file in os.listdir("static/images/"):
        if file.endswith('.png'):
            os.remove("static/images/" + file)
    flash("La historia fue eliminada satisfactoriamente!!")
    
    return redirect('/')


if __name__ == '__main__':
    #app.run(debug=True, host="172.16.170.128", port=8080)
    app.run(debug=True, host="localhost", port=5000)
    
