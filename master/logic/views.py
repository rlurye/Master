import flask
from flask import redirect, render_template, request, session, url_for, send_from_directory
from master import app
from master.logic.core import *
import itertools

nap = []
mnap = []

@app.route('/', methods=['GET', 'POST'])
def index():
    disciplines(nap,mnap)
    return render_template('index.html', user=None, matter = mnap, others = nap)

@app.route('/t/<path:path>', methods=['GET', 'POST'])
def gettable(path):
    print(path[:-1])
    if path == 'all':
        name = gen_table_all(mnap, nap)
        return redirect(url_for('static', filename='tables/' + name))
    for i in itertools.chain(mnap, nap):
        if 'code' in i:
            if i['code'] == path[:-1]:
                name = gen_table(i, path)
                return redirect(url_for('static', filename='tables/' + name))
    return render_template('index.html', user=None, matter=mnap, others=nap)