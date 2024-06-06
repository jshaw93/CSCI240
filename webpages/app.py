#!/usr/bin/python3
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import mysql.connector
import asyncio
# import time
import requests
import datetime
import threading
from gevent.pywsgi import WSGIServer

load_dotenv()

app = Flask(__name__, '/')


async def update_data():
    global priceData
    print("Starting")
    for _ in range(2000000000):
        try:
            now = datetime.datetime.utcnow()-datetime.timedelta(hours=6)
            priceData = latest()
            print(f'PRICES UPDATED {now.strftime(r"%m/%d %H:%M")}')
        except requests.ConnectionError:
            pass
        await asyncio.sleep(300)


LIMIT = 150
priceData = {}

@app.route('/items', methods=['GET'])
def table():
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    cursor = db.cursor()
    query = ("select * from Item order by ItemID;")
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('items.html', items=items)


@app.route('/', methods=['GET'])
def recipes():
    nature = getLowPrice(561)
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    cursor = db.cursor()
    statement = 'select * from Recipe where SkillName!="barrows" order by RecipeID;'
    cursor.execute(statement)
    recipes = cursor.fetchall()
    newRecipes = []
    for recipe in recipes:
        recipe = list(recipe)
        recipeID = recipe[1]
        recipeAmt = recipe[3]
        cursor.execute(f'select * from ItemRecipe where ItemRecipeID={recipe[4]}')
        ingredients = cursor.fetchall()
        sells = getProfit(recipeID, recipeAmt, ingredients)
        for i in sells:
            recipe.append(i)
        alchquery = ('select Alch from Item where ItemID=%s')
        cursor.execute(alchquery, (recipeID, ))
        alch = cursor.fetchone()[0] - nature - sells[2]
        recipe.append(alch)
        recipe.append(recipeID)
        recipe = tuple(recipe)
        newRecipes.append(recipe)
        
    return render_template('recipes.html', recipes=newRecipes)


@app.route('/ingredients', methods=['GET'])
def ingredients():
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    cursor = db.cursor()
    recipename = request.args.get('recipename')
    ingid = request.args.get('id')
    statement = '''select ir.ItemRecipeID, ir.ItemID, ir.Quantity, i.ItemName from ItemRecipe ir
    inner join Item i on ir.ItemID=i.ItemID
    where ir.ItemRecipeID=%s;'''
    cursor.execute(statement, (ingid, ))
    items = cursor.fetchall()
    newItems = []
    for item in items:
        item = list(item)
        price = getLowPrice(item[1])
        item.append(price)
        item = tuple(item)
        newItems.append(item)
    cursor.close()
    db.close()
    return render_template('ingredients.html', ingredients=newItems, ingid=ingid, recipename=recipename)


@app.route('/barrows', methods=['GET', 'POST'])
def barrows():
    lvl = request.args.get('lvl')
    if lvl is None:
        lvl = 1
    elif not lvl.isdigit():
        return f"{lvl} is an invalid input, please input a whole number between 1-99"
    elif 1 > int(lvl) > 99:
        return f"{lvl} is an invalid input, please input a whole number between 1-99"
    else:
        lvl = int(lvl)
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    cursor = db.cursor()
    query = ('select * from Recipe where SkillName="barrows"')
    cursor.execute(query)
    recipes = cursor.fetchall()
    barrowsRecipes = []
    for recipe in recipes:
        recipe = list(recipe)
        query = ('select * from ItemRecipe where ItemRecipeID=%s')
        cursor.execute(query, (recipe[0], ))
        ingredients = cursor.fetchall()
        brokenid = ingredients[1][1]
        basegold = ingredients[0][2]
        goldcost = int(basegold * (1 - lvl / 200))
        brokencost = getLowPrice(brokenid)
        recipe.append(goldcost)
        recipe.append(brokencost)
        recipe.append(getHighPrice(recipe[1]))
        recipe.append(getName(brokenid, cursor))
        profit = getHighPrice(recipe[1]) - goldcost - brokencost
        recipe.append(profit)
        recipe[5] = lvl
        recipe.append(brokenid)
        recipe = tuple(recipe)
        barrowsRecipes.append(recipe)
    return render_template('barrows.html', recipes=barrowsRecipes, lvl=lvl)


@app.route("/flips", methods=["GET"])
def flips():
    items = []
    db = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        database=os.getenv('DB')
    )
    cursor = db.cursor()
    query = ('select * from Item')
    cursor.execute(query)
    itemResult = cursor.fetchall()
    for item in itemResult:
        # Structure (name, low, high, margin, alch, id, membs)
        itemID = item[0]
        low, high = getBothPrice(itemID)
        if low is None or high is None:
            continue
        alch = item[2]
        name = item[3]
        if '3rd age' in name:
            continue
        membs = item[1]
        membs = "Yes" if membs == 1 else "No"
        margin = round((high - low) - high * 0.1) - 1
        alchProfit = alch - low
        geLimit = item[4] if item[4] is not None else -1
        items.append((name, low, high, margin, alch, itemID, membs, alchProfit, geLimit))
    return render_template('flips.html', items=items)


def latest():
    """

    :return: JSON Data from OSRS Wiki 'latest' API endpoint
    """
    url = 'https://prices.runescape.wiki/api/v1/osrs/latest'
    headers = {
        'User-Agent': '@_.lore OS Combinations website - 1 per 5m'
    }
    data = requests.get(url, headers=headers).json()
    return data


def asyncLoop():
    loop = asyncio.new_event_loop()
    tasks = []
    tasks.append(loop.create_task(update_data()))
    loop.run_until_complete(asyncio.wait(tasks))


def getProfit(recipeID, recipeAmt, ingredients):
    recipeSell = None
    recipeCost = 0
    sellAt = 0
    for ing in ingredients:
        ingID = ing[1]
        if ingID == -2:
            recipeCost += ing[2]
            continue
        try:
            l = getLowPrice(ing[1])
            if l is None:
                recipeCost += 0
            else:
                recipeCost += l * ing[2]
        except KeyError:
            pass
    try:
        recipeSell = recipeAmt * int(priceData['data'][str(recipeID)]['high']) - recipeCost
        recipeSell = round(recipeSell - (recipeSell * 0.01)) - 1
        sellAt = int(priceData['data'][str(recipeID)]['high'])
    except KeyError:
        pass
    return (recipeSell, sellAt, recipeCost)


def getLowPrice(itemID):
    cost = None
    try:
        cost = int(priceData['data'][str(itemID)]['low'])
    except KeyError:
        pass
    return cost


def getHighPrice(itemID):
    sell = None
    try:
        sell = int(priceData['data'][str(itemID)]['high'])
    except KeyError:
        pass
    return sell


def getBothPrice(itemID):
    priceLow = None
    priceHigh = None
    try:
        priceLow = int(priceData['data'][str(itemID)]['low'])
        priceHigh = int(priceData['data'][str(itemID)]['high'])
    except KeyError:
        pass
    return (priceLow, priceHigh)


def getName(itemID, cursor):
    query = ('select ItemName from Item where ItemID=%s')
    cursor.execute(query, (itemID, ))
    name = cursor.fetchone()
    return name[0]


if __name__ == '__main__':
    threads = []
    t = threading.Thread(target=asyncLoop)
    threads.append(t)
    for i in threads:
        i.start()
    # app.run(debug=False, host='0.0.0.0', port=5000)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
