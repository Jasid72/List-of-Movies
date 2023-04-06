import mysql.connector
from flask import Flask, render_template, redirect, url_for
from bs4 import BeautifulSoup
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
bootstrap = Bootstrap(app)


mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="root1234",
    database="university"
)

mycursor = mydb.cursor()
query = "SELECT * FROM movies"
mycursor.execute(query)


myresult = mycursor.fetchall()

for x in myresult:
  print(x)


@app.route("/")
def home():
        if not myresult:
                return render_template("Example.html")
        else:
            return render_template("Example.html", name=x[0],
                                   dates=x[2],
                                   rating=x[4],
                                   review=x[6],
                                   overview=x[3])


class Update(FlaskForm):
    rating = StringField("Enter Rating: ", validators=[DataRequired()])
    review = StringField("Enter Review: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    rating = None
    review = None
    form = Update()
    if form.validate_on_submit():
        rating = float(form.rating.data)
        review = form.review.data
        form.rating.data = ''
        form.review.data = ''
        update_query = f"Update movies set rating = '{rating}', review= '{review}' where id= '1'"
        mycursor.execute(update_query)
        mydb.commit()
        return render_template("Example.html", name=x[0],
                           dates=x[1],
                           rating=x[4],
                           review=x[6],
                           overview=x[2])
    return render_template("edit2.html", rating=rating, review=review, form=form, movie_title=myresult[1])


@app.route("/Delete", methods=['GET', 'POST'])
def delete():
    del_query = "TRUNCATE TABLE movies"
    mycursor.execute(del_query)
    mydb.commit()
    return render_template("Example.html")


class NameForm(FlaskForm):
    name = StringField("Movie Title: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = NameForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        return render_template("Example.html")
    return render_template("add2.html", name=name, form=form)


if __name__ == '__main__':
    app.run(debug=True)





