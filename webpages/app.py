from flask import Flask, render_template, url_for, request, redirect
import json

app = Flask(__name__)

with open('recipes.json', 'r') as myFile:
    recipesRaw = json.load(myFile)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['recipename']
        recipeid = request.form['recipeid']
        amount = request.form['recipeamount']
        level = request.form['recipelevel']
        skill = request.form['recipeskill']
        recipesRaw.update({name: {
            "recipeid": recipeid,
            "amount": amount,
            "level": level,
            "skill": skill
        }})
        with open('recipes.json', 'w') as myFile:
            json.dump(recipesRaw, myFile, indent=4)
        return redirect('/table')
    else:
        return render_template('index.html')

@app.route('/table')
def table():
    return render_template('static.html', recipes=recipesRaw)

if __name__ == '__main__':\
    app.run(debug=True, host='192.168.1.44', port=5000)
