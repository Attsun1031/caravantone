# -*- coding: utf-8 -*-
from flask import render_template
from .util import require_login


@require_login
def user_index(user):
    return render_template('my_page.html', user=user)


def configure(app):
    app.route("/user", methods=['GET'])(user_index)
