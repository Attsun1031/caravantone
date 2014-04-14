# -*- coding: utf-8 -*-

from flask import Flask
import view

app = Flask(__name__)
view.configure(app)

if __name__ == "__main__":
    app.run(host='192.168.56.101')
