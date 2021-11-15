from flask import Flask, render_template, json, request
import os
import database.db_connector as db
from database.db_connector import execute_query, connect_to_database

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
@app.route('/index')
def root():
    return render_template("index.j2")

@app.route('/listings', methods=['GET', 'POST'])
def Listings():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Listings;"
        cursor = execute_query(db_connection, query)
        results = cursor.fetchall()
        return render_template("listings.j2", Listings=results)
        
    elif request.method == 'POST':
        Price = request.form['price_input']
        StreetAddress = request.form['address_input']
        City = request.form['city_input']
        State = request.form['state_input']
        ZipCode = request.form['zip_input']
        Description = request.form['description_input']
        AnimalsAllowed = request.form['animals']
        BedCount = request.form['beds_input']
        BathCount = request.form['baths_input']
        SquareFeet = request.form['squarefeet_input']
        ListingDate = request.form['date_input']
        StoryCount = request.form['stories_input']
        Garage = request.form['garage']
        RentOrSale = request.form['rentsale']
        RealtorID = request.form['realtor_input']
        BuyerID = request.form['buyer_input']
        SellerID = request.form['seller_input']
        query = "INSERT INTO Listings (Price, StreetAddress, City, State, ZipCode, Description, AnimalsAllowed, BedCount, BathCount, SquareFeet, ListingDate, StoryCount, Garage, RentOrSale, RealtorID, BuyerID, SellerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (Price, StreetAddress, City, State, ZipCode, Description, AnimalsAllowed, BedCount, BathCount, SquareFeet, ListingDate, StoryCount, Garage, RentOrSale, RealtorID, BuyerID, SellerID)
        execute_query(db_connection, query, data)

        query2 = "SELECT * FROM Listings;"
        cursor = execute_query(db_connection, query2)
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