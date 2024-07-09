from flask import Flask,render_template,redirect,request
from flask_bootstrap import Bootstrap4
import sqlite3

mapbase_url= "https://www.google.com/maps/search/?api=1&query="


app=Flask(__name__)
app.secret_key="Resturants"
bootstrap=Bootstrap4(app)

def display_db():
    conn=sqlite3.connect("instance/resturants.db")
    cur= conn.cursor()
    cur.execute("SELECT * FROM restaurants")
    rows=cur.fetchall()
    return rows

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/resturants")
def resturants():
    resturants=display_db()
    return render_template("resturants.html",resturants=resturants)

@app.route("/add",methods=["POST","GET"])
def add():
    if request.method=="POST":
        name=request.form["cafename"]
        typ=request.form["type"]
        address=request.form["address"]
        ad=f"{mapbase_url}{address.replace(" ","+")}"
        rating= request.form["rating"]
        review=request.form["review"]
        price=request.form["price"]
        phone=request.form["phone"]
        conn=sqlite3.connect("instance/resturants.db")
        cur=conn.cursor()
        cur.execute('''
        INSERT INTO restaurants (name,type,address,ratings,reviews,price_range,phone_number)
        VALUES (?, ?, ?, ?, ?, ?,?)
        ''',(name,typ,ad,rating,review,price,phone ))
        conn.commit()
        conn.close()
        return redirect("/resturants")
    else:
        return render_template("add.html")


@app.route("/update/<int:id>",methods=["POST","GET"])
def update(id):
    conn=sqlite3.connect("instance/resturants.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM restaurants WHERE id = ?", (id,))
    resturant=cur.fetchone()
    if request.method=="POST":
        name=request.form["cafename"]
        typ=request.form["type"]
        address=request.form["address"]
        ad=f"{mapbase_url}{address.replace(" ","+")}"
        rating= request.form["rating"]
        review=request.form["review"]
        price=request.form["price"]
        phone=request.form["phone"]
        cur.execute('''
        UPDATE restaurants SET name=?,type=?,address=?,ratings=?,reviews=?,price_range=?,phone_number=? WHERE id=?
        ''',(name,typ,ad,rating,review,price,phone,id ))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/resturants")
    else:
        url= resturant[3]
        index=url.find("query=")
        address=url[index+len("query="):].replace("+"," ")
            
            
        return render_template("update.html",resturant=resturant,address=address)

@app.route("/delete/<int:id>",methods=["POST","GET"])
def delete(id):
    conn=sqlite3.connect("instance/resturants.db")
    cur=conn.cursor()
    cur.execute('''
            DELETE FROM restaurants
            WHERE id = ?''',
    (id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/resturants")

@app.route("/about")
def about():
    return render_template("about.html")
if __name__=="__main__":
    app.run(debug=True)