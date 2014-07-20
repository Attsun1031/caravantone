# -*- coding: utf-8 -*-
from flask import render_template
from .util import require_login
from caravantone import app


@app.route("/user", methods=['GET'])
@require_login
def user_index(user):
    return render_template('my_page.html', user=user)
