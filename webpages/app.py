#!/usr/bin/python3
from flask import Flask, render_template, request, redirect
import json, os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = Flask(__name__)

LIMIT = 15

@app.route('/updateitem', methods=['GET'])
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
    search = request.args.get('search') == 'true'
    membs = "1" if request.args.get('itemmembs') == 'on' else "0"
    alch = request.args.get('itemalch')
    itemname = None if request.args.get('itemname') == '' else request.args.get('itemname')
    compile = (itemid, membs, alch)
    insertcheck = '' in compile
    if request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        cursor.execute('delete from Item where ItemID=%s;', (deleteID, ))
        db.commit()
    elif not insertcheck and request.args.get('insert') == 'true':
        insert = """insert into Item
        values (%s, %s, %s, %s);"""
        cursor.execute(insert, (itemid, membs, alch, itemname))
        db.commit()
    elif itemid != '' and search:
        cursor.execute('select * from Item where ItemID=%s;', (itemid, ))
        items = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('static.html', items=items)
    query = ("select * from Item order by ItemID limit %s;")
    cursor.execute(query, (LIMIT, ))
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('static.html', items=items)


@app.route('/recipes', methods=['GET'])
def recipes():
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    cursor = db.cursor()
    itemid = request.args.get('id')
    if itemid is not None and request.args.get('delete') != 'true':
        statement = 'select * from Recipe where ItemCreatedID=%s;'
        cursor.execute(statement, (itemid, ))
        recipes = cursor.fetchall()
        return render_template('recipes.html', recipes=recipes)
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        cursor.execute('delete from Recipe where RecipeID=%s;', (deleteID, ))
        db.commit()
    statement = 'select * from Recipe order by RecipeID limit %s;'
    cursor.execute(statement, (LIMIT, ))
    recipes = cursor.fetchall()
    return render_template('recipes.html', recipes=recipes)

       
@app.route('/updaterecipe', methods=['GET'])
def updaterecipe():
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    changeid = request.args.get('id')
    recid = request.args.get('recid')
    recname = request.args.get('recname')
    recitemid = request.args.get('recitemid')
    recprod = request.args.get('recprod')
    recingid = request.args.get('recingid')
    reclvl = request.args.get('reclvl')
    reccat = request.args.get('reccat')
    compile = (recid, recitemid, recname, recprod, recingid, reclvl, reccat)
    updatecheck = '' in compile
    cats = ["item sets", "crafting", "smithing", "farming", "herblore", "decanting",
               "magic", "cooking", "misc", "fletching", "construction"]
    if changeid == '':
        return "Error, id not specified"
    elif not updatecheck and request.args.get('update') == 'true':
        if reccat.lower() not in cats:
            return 'Error, category does not exist.  Please chose from this list: "item sets", "crafting", "smithing", "farming", "herblore", "decanting", "magic", "cooking", "misc", "fletching", "construction"'
        statement = 'update Recipe set RecipeID=%s, ItemCreatedID=%s, RecipeName=%s, AmtProduced=%s, ItemRecipeID=%s, SkillLvl=%s, SkillName=%s where RecipeID=%s;'
        cursor = db.cursor()
        cursor.execute(statement, (recid, recitemid, recname, recprod, recingid, reclvl, reccat, recid))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/recipes')
    cursor = db.cursor()
    cursor.execute('select * from Recipe where RecipeID=%s;', (changeid, ))
    item = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('updaterecipe.html', recipename=item[2], recid=item[0], itemid=item[1], produced=item[3], ingid=item[4], lvl=item[5], cat=item[6])


@app.route('/ingredients', methods=['GET'])
def ingredients():
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    cursor = db.cursor()
    ingid = request.args.get('id')
    insertid = request.args.get('ingid')
    iid = request.args.get('itemid')
    quantity= request.args.get('quantity')
    compile = (insertid, iid, quantity)
    insertcheck = '' in compile
    if request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        print(deleteID, iid)
        cursor.execute('delete from ItemRecipe where ItemRecipeID=%s and ItemID=%s;', (deleteID, iid))
        db.commit()
    elif request.args.get('insert') == 'true' and not insertcheck:
        statement = 'insert into ItemRecipe values (%s, %s, %s);'
        cursor.execute(statement, compile)
        db.commit()
    statement = '''select ir.ItemRecipeID, ir.ItemID, ir.Quantity, i.ItemName from ItemRecipe ir
    inner join Item i on ir.ItemID=i.ItemID
    where ir.ItemRecipeID=%s;'''
    cursor.execute(statement, (ingid, ))
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('ingredients.html', ingredients=items, ingid=ingid)


@app.route('/updateingredient', methods=['GET'])
def updateingredient():
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    changeid = request.args.get('id')
    itemid = request.args.get('iid')
    changeitemid = request.args.get('ciid')
    ingquant = request.args.get('ingquant')
    compile = (changeid, itemid, ingquant, changeid)
    updatecheck = '' in compile
    if changeid == '':
        return "Error, id not specified"
    elif not updatecheck and request.args.get('update') == 'true':
        cursor = db.cursor()
        cursor.execute('update ItemRecipe set ItemRecipeID=%s, ItemID=%s, Quantity=%s where ItemRecipeID=%s and ItemID=%s;', (changeid, itemid, ingquant, changeid, changeitemid))
        db.commit()
        cursor.close()
        db.close()
        return redirect(f'/ingredients?id={changeid}')
    cursor = db.cursor()
    cursor.execute('select * from ItemRecipe where ItemRecipeID=%s and ItemID=%s;', (changeid, itemid))
    data = cursor.fetchone()
    print(data)
    cursor.close()
    db.close()
    return render_template('updateingredient.html', ingid=data[0], itemid=data[1], ingquant=data[2])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
