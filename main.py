from flask import Flask, render_template, request, make_response
from aes import AESComponent
import logging

app = Flask(__name__)


def open_and_read(fName):
    return fName.stream.read()


@app.route("/")
def form():
    return render_template("index.html")


@app.route("/submitted", methods=["POST"])
def submitted_form():
    inputfile = open_and_read(request.files["inputfile"])
    keyfile = open_and_read(request.files["keyfile"])
    filename = request.form["outputfile"]
    keysize = int(request.form["size"])
    mode = request.form["mode"]
    nk = {128: 4, 256: 8}
    nr = {128: 10, 256: 14}

    component = None
    if mode == "encrypt":
        import encrypt
        component = encrypt.AESEncryptor()
    if mode == "decrypt":
        import decrypt
        component = decrypt.AESDecryptor()

    output = component.aes(bytearray(inputfile), AESComponent.expand_key(
        keyfile, nk[keysize], nr[keysize]), nr[keysize], False)
    resp_file = bytes(output)
    response = make_response(resp_file)
    response.headers["Content-Disposition"] = "attachment; filename=" + filename
    return response


@app.errorhandler(400)
def user_error(e):
    logging.exception('An error occurred during a request.')
    return "Something went wrong", 400


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80)
