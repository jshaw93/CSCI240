from flask import Flask, render_template, request, redirect
import json, os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = Flask(__name__)

with open('recipes.json', 'r') as myFile:
    recipesRaw = json.load(myFile)

@app.route('/update', methods=['GET'])
def update():
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    changeid = request.args.get('id')
    itemid = request.args.get('itemid')
    membs = "1" if request.args.get('itemmembs') == 'on' else "0"
    alch = request.args.get('itemalch')
    compile = (itemid, membs, alch)
    insertcheck = '' in compile
    if id == '':
        return "Error, id not specified"
    elif not insertcheck and request.args.get('update') == 'true':
        cursor = db.cursor()
        cursor.execute('update Item set ItemID=%s, Membs=%s, Alch=%s where ItemID=%s;', (itemid, membs, alch, itemid))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    cursor = db.cursor()
    cursor.execute('select * from Item where ItemID=%s;', (changeid, ))
    item = cursor.fetchone()
    print(item)
    cursor.close()
    db.close()
    return render_template('index.html', itemid = item[0], itemmembs=item[1], itemalch = item[2])

@app.route('/', methods=['GET'])
def table():
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    cursor = db.cursor()
    itemid = request.args.get('itemid')
    membs = "1" if request.args.get('itemmembs') == 'on' else "0"
    alch = request.args.get('itemalch')
    compile = (itemid, membs, alch)
    insertcheck = '' in compile
    if request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        cursor.execute('delete from Item where ItemID=%s;', (deleteID, ))
        db.commit()
    elif not insertcheck and request.args.get('insert') == 'true':
        insert = """insert into Item
        values (%s, %s, %s);"""
        cursor.execute(insert, compile)
        db.commit()
    query = ("select * from Item")
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('static.html', items=items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
