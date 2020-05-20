from flask import request, g
from flask import Flask, jsonify, render_template, redirect, url_for
from models import Base, Item, Category


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import json

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/')
def displayAll():
    cs = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('main.html', cs = cs, items = items)

@app.route('/catalog.json')
def giveJson():
    cs = session.query(Category).all()
    result = {
        'Categories': []
    }
    for c in cs:
        # result['Categories'].append(c.serialize)
        items = session.query(Item).filter_by(category_id = c.id).all()
        for i in items:
            c_serialize =  c.serialize
            c_serialize['Items'].insert(0, i.serialize)
        result['Categories'].insert(0, c_serialize)

    return jsonify(result)

@app.route('/catalog/<string:category>/<string:title>')
def displayItem(category, title):
    i = getItem(title)
    if not i:
        return "No item found"
    return render_template('displayIitem.html', i = i)

@app.route('/catalog/<string:category>/items')
def displayCategory(category):
    c = session.query(Category).filter_by(name = category).first()
    cid = c.id
    items = session.query(Item).filter_by(category_id = cid).all()
    return render_template('displayCategory.html', items = items, c = c)


@app.route('/catalog/<string:title>/edit', methods = ['GET', 'POST'])
def editItem(title):
    if request.method == 'GET':
        i = getItem(title)
        cs = session.query(Category).all()
        return render_template('editItem.html', i = i, cs = cs)
    elif request.method == 'POST':
        i = getItem(title)
        if request.form['Title']:
            i.name = request.form['Title']
        if request.form['Description']:
            i.description = request.form['Description']
        if request.form['Category']:
            i.category_id = request.form['Category']
        session.add(i)
        session.commit()
        return redirect(url_for('displayAll'))

@app.route('/catalog/<string:title>/delete', methods = ['GET', 'POST'])
def deleteItem(title):
    i = getItem(title)
    if request.method == 'GET':
        return render_template('deleteItem.html', i = i)
    elif request.method == 'POST':
        session.delete(i)
        session.commit()
        return redirect(url_for('displayAll'))


def getItem(title):
    i = session.query(Item).filter_by(name = title).first()
    ctemp = session.query(Category).filter_by(id = i.category_id).first()
    if ctemp:
        i.category_id = ctemp.name
    return i
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)