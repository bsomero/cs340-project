from flask import Flask, render_template, json
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
@app.route('/index')
def root():
    return render_template("index.j2")

@app.route('/listings')
def Listings():
    query = "SELECT * FROM Listings;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("listings.j2", Listings=results)

@app.route('/realtors')
def Realtors():
    query = "SELECT * FROM Realtors;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("realtors.j2", Realtors=results)

@app.route('/buyers')
def Buyers():
    query = "SELECT * FROM Buyers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("buyers.j2", Buyers=results)

@app.route('/sellers')
def Sellers():
    query = "SELECT * FROM Sellers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("sellers.j2", Sellers=results)

@app.route('/realtors-buyers')
def RealtorsBuyers():
    query = "SELECT * FROM RealtorsBuyers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("realtors-buyers.j2", RealtorsBuyers=results)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1115))
    app.run(host='0.0.0.0',port=port, debug=True)