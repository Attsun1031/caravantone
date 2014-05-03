# -*- coding: utf-8 -*-

from flask import Flask
import caravantone.view as view

dev_host = '192.168.33.10'
app = Flask(__name__)
view.configure(app)
app.config['DB_URI'] = 'mysql://caravantone:caravantone@{}/caravantone?charset=utf8&use_unicode=0'.format(dev_host)

if __name__ == "__main__":
    app.debug = True
    app.run(host=dev_host)
