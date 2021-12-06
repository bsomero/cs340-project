from flask import Flask, render_template, json, request, redirect
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

    #  Display all listings
    if request.method == 'GET':
        query = "SELECT * FROM Listings;"
        cursor = execute_query(db_connection, query)
        results = cursor.fetchall()

        # Data stored as a number in the database is displayed as a string
        for result in results:
            if result["Garage"] == 1:
                result["Garage"] = "Attached"
            if result["Garage"] == 2:
                result["Garage"] = "Detached"
            if result["Garage"] == 0:
                result["Garage"] = "None"
            if result["RentOrSale"] == 0:
                result["RentOrSale"] = "Rent"
            if result["RentOrSale"] == 1:
                result["RentOrSale"] = "Sale"
            if result["AnimalsAllowed"] == 0:
                result["AnimalsAllowed"] = "No"
            if result["AnimalsAllowed"] == 1:
                result["AnimalsAllowed"] = "Yes"

        # Populate dropdown menus
        query2 = "SELECT FirstName, RealtorID FROM Realtors"
        cursor2 = execute_query(db_connection, query2)
        results2 = cursor2.fetchall()

        query3 = "SELECT FirstName, BuyerID FROM Buyers"
        cursor3 = execute_query(db_connection, query3)
        results3 = cursor3.fetchall()

        query4 = "SELECT FirstName, SellerID FROM Sellers"
        cursor4 = execute_query(db_connection, query4)
        results4 = cursor4.fetchall()
        return render_template("listings.j2", context={'Listings':results, 'Realtors':results2, 'Buyers':results3, 'Sellers':results4})
        
    # Add a new listing
    elif request.method == 'POST' and "add_button" in request.form:
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

        # Convert strings to numbers
        if Garage == "attached":
            Garage = 1
        elif Garage == "detached":
            Garage = 2
        else:
            Garage = 0

        if AnimalsAllowed == "yes":
            AnimalsAllowed = 1
        else:
            AnimalsAllowed = 0

        if RentOrSale == "rent":
            RentOrSale = 0
        else:
            RentOrSale = 1
    
        if RealtorID == "":
            RealtorID = None
        if BuyerID == "":
            BuyerID = None
        
        query = "INSERT INTO Listings (Price, StreetAddress, City, State, ZipCode, Description, AnimalsAllowed, BedCount, BathCount, SquareFeet, ListingDate, StoryCount, Garage, RentOrSale, RealtorID, BuyerID, SellerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (Price, StreetAddress, City, State, ZipCode, Description, AnimalsAllowed, BedCount, BathCount, SquareFeet, ListingDate, StoryCount, Garage, RentOrSale, RealtorID, BuyerID, SellerID)
        execute_query(db_connection, query, data)

        return redirect("/listings")
    
    # Delete a listing row
    elif request.method == 'POST' and "delete_button" in request.form:
        ListingID = request.form['delete_button']
        query = "DELETE FROM Listings WHERE ListingID = %s;" % ListingID
        execute_query(db_connection, query)

        return redirect("/listings")

    # Update a listing row when edit button for that row clicked
    elif request.method == 'POST' and "edit_button" in request.form:
        ListingID = request.form['edit_button']

        query = "SELECT * FROM Listings WHERE ListingID = %s;" % (ListingID)
        update_result = execute_query(db_connection, query).fetchone()

        if update_result == None:
            query2 = "SELECT * FROM Listings;"
            cursor = execute_query(db_connection, query2)
            results = cursor.fetchall()
            return render_template("listings.j2", Listings=results)
        
        return render_template("listings_update.j2", Listing=update_result)

    # Search all attributes for a listing and display results
    elif request.method == 'POST' and "search_button" in request.form:
        Search = ('%%' + request.form['search_input'] + '%%')

        query = "SELECT * FROM Listings WHERE Price LIKE '%s' OR StreetAddress LIKE '%s' OR City LIKE '%s' OR State LIKE '%s' OR ZipCode LIKE '%s' OR Description LIKE '%s' OR AnimalsAllowed LIKE '%s' OR BedCount LIKE '%s' OR BathCount LIKE '%s' OR SquareFeet LIKE '%s' OR ListingDate LIKE '%s' OR StoryCount LIKE '%s' OR Garage LIKE '%s' OR RentOrSale LIKE '%s' OR RealtorID LIKE '%s' OR BuyerID LIKE '%s' OR SellerID LIKE '%s';" % (Search, Search, Search, Search, Search, Search, Search, Search, Search, Search, Search, Search, Search, Search, Search, Search, Search)
        cursor = execute_query(db_connection, query)
        results = cursor.fetchall()

        for result in results:
            if result["Garage"] == 1:
                result["Garage"] = "Attached"
            if result["Garage"] == 2:
                result["Garage"] = "Detached"
            if result["Garage"] == 0:
                result["Garage"] = "None"
            if result["RentOrSale"] == 0:
                result["RentOrSale"] = "Rent"
            if result["RentOrSale"] == 1:
                result["RentOrSale"] = "Sale"
            if result["AnimalsAllowed"] == 0:
                result["AnimalsAllowed"] = "No"
            if result["AnimalsAllowed"] == 1:
                result["AnimalsAllowed"] = "Yes"

        query2 = "SELECT FirstName, RealtorID FROM Realtors"
        cursor2 = execute_query(db_connection, query2)
        results2 = cursor2.fetchall()

        query3 = "SELECT FirstName, BuyerID FROM Buyers"
        cursor3 = execute_query(db_connection, query3)
        results3 = cursor3.fetchall()

        query4 = "SELECT FirstName, SellerID FROM Sellers"
        cursor4 = execute_query(db_connection, query4)
        results4 = cursor4.fetchall()
        return render_template("listings.j2", context={'Listings':results, 'Realtors':results2, 'Buyers':results3, 'Sellers':results4})

@app.route('/listings-update', methods=['POST'])
def listings_update():
    db_connection = connect_to_database()
    ListingID = request.form['update_button']
    Price = request.form['price_update']
    StreetAddress = request.form['address_update']
    City = request.form['city_update']
    State = request.form['state_update']
    ZipCode = request.form['zip_update']
    Description = request.form['description_update']
    AnimalsAllowed = request.form['animals_update']
    BedCount = request.form['beds_update']
    BathCount = request.form['baths_update']
    SquareFeet = request.form['squarefeet_update']
    ListingDate = request.form['date_update']
    StoryCount = request.form['stories_update']
    Garage = request.form['garage_update']
    RentOrSale = request.form['rentorsale_update']
    RealtorID = request.form['realtor_update']
    BuyerID = request.form['buyer_update']
    SellerID = request.form['seller_update']

    if Garage == "attached":
        Garage = 1
    elif Garage == "detached":
        Garage = 2
    else:
        Garage = 0

    if AnimalsAllowed == "yes":
        AnimalsAllowed = 1
    else:
        AnimalsAllowed = 0

    if RentOrSale == "rent":
        RentOrSale = 0
    else:
        RentOrSale = 1

    if RealtorID == "":
        RealtorID = None
    if BuyerID == "":
        BuyerID = None

    # Update a listing row
    query = "UPDATE Listings SET Price = %s, StreetAddress = %s, City = %s, State = %s, ZipCode = %s, Description = %s, AnimalsAllowed = %s, BedCount = %s, BathCount = %s, SquareFeet = %s, ListingDate = %s, StoryCount = %s, Garage = %s, RentOrSale = %s, RealtorID = %s, BuyerID = %s, SellerID = %s WHERE ListingID = %s;"
    data = (Price, StreetAddress, City, State, ZipCode, Description, AnimalsAllowed, BedCount, BathCount, SquareFeet, ListingDate, StoryCount, Garage, RentOrSale, RealtorID, BuyerID, SellerID, ListingID)
    execute_query(db_connection, query, data)
    return redirect("./listings")


@app.route('/realtors', methods=['GET', 'POST'])
def Realtors():
    db_connection = connect_to_database()

    # Display all Realtors
    if request.method == 'GET':
        query = "SELECT * FROM Realtors;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        for result in results:
            phone = '('
            phone += result['Phone'][0:3]
            phone += ') - '
            phone += result['Phone'][3:6]
            phone += ' - '
            phone += result['Phone'][6:10]
            result['Phone'] = phone
        return render_template("realtors.j2", Realtors=results)

    # Add a Realtor and display updated table
    elif request.method == 'POST' and "add_button" in request.form:
        FirstName = request.form['fname_input']
        LastName = request.form['lname_input']
        Email = request.form['email_input']
        Phone = request.form['phone_input']

        query = "INSERT INTO Realtors (FirstName, LastName, Email, Phone) VALUES (%s, %s, %s, %s);"
        data = (FirstName, LastName, Email, Phone)
        execute_query(db_connection, query, data)

        query2 = "SELECT * FROM Realtors;"
        cursor = execute_query(db_connection, query2)
        results = cursor.fetchall()

        return render_template("realtors.j2", Realtors=results)

    # Delete a Realtor and display updated table
    elif request.method == 'POST' and "delete_button" in request.form:
        RealtorID = request.form['delete_button']
        query = "DELETE FROM Realtors WHERE RealtorID = %s;" % RealtorID
        execute_query(db_connection, query)

        query2 = "SELECT * FROM Realtors;"
        cursor = execute_query(db_connection, query2)
        results = cursor.fetchall()

        return render_template("realtors.j2", Realtors=results)

    # Update a Realtor
    elif request.method == 'POST' and "edit_button" in request.form:
        RealtorID = request.form['edit_button']

        query = "SELECT * FROM Realtors WHERE RealtorID = %s;" % (RealtorID)
        update_result = execute_query(db_connection, query).fetchone()

        if update_result == None:
            query2 = "SELECT * FROM Realtors;"
            cursor = execute_query(db_connection, query2)
            results = cursor.fetchall()
            return render_template("realtors.j2", Realtors=results)
        
        return render_template("realtors_update.j2", Realtor=update_result)
        
@app.route('/realtor-update', methods=['POST'])
def realtor_update():
    db_connection = connect_to_database()
    RealtorID = request.form['update_button']
    FirstName = request.form['fname_update']
    LastName = request.form['lname_update']
    Email = request.form['email_update']
    Phone = request.form['phone_update']

    query = "UPDATE Realtors SET FirstName = %s, LastName = %s, Email = %s, Phone = %s WHERE RealtorID = %s;"
    data = (FirstName, LastName, Email, Phone, RealtorID)
    execute_query(db_connection, query, data)

    return redirect("./realtors")
    

@app.route('/buyers', methods=['GET', 'POST'])
def Buyers():
    db_connection = connect_to_database()

    # Display all Buyers
    if request.method == 'GET':
        query = "SELECT * FROM Buyers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        for result in results:
            phone = '('
            phone += result['Phone'][0:3]
            phone += ') - '
            phone += result['Phone'][3:6]
            phone += ' - '
            phone += result['Phone'][6:10]
            result['Phone'] = phone
        return render_template("buyers.j2", Buyers=results)

    # Add a Buyer and display updated table
    elif request.method == 'POST' and "add_button" in request.form:
        FirstName = request.form['fname_input']
        LastName = request.form['lname_input']
        Email = request.form['email_input']
        Phone = request.form['phone_input']

        query = "INSERT INTO Buyers (FirstName, LastName, Email, Phone) VALUES (%s, %s, %s, %s);"
        data = (FirstName, LastName, Email, Phone)
        execute_query(db_connection, query, data)

        query2 = "SELECT * FROM Buyers;"
        cursor = execute_query(db_connection, query2)
        results = cursor.fetchall()

        return render_template("buyers.j2", Buyers=results)

    # Delete a Buyer and display updated table
    elif request.method == 'POST' and "delete_button" in request.form:
        BuyerID = request.form['delete_button']
        query = "DELETE FROM Buyers WHERE BuyerID = %s;" % BuyerID
        execute_query(db_connection, query)

        query2 = "SELECT * FROM Buyers;"
        cursor = execute_query(db_connection, query2)
        results = cursor.fetchall()

        return render_template("buyers.j2", Buyers=results)

    # Update a Buyer
    elif request.method == 'POST' and "edit_button" in request.form:
        BuyerID = request.form['edit_button']

        query = "SELECT * FROM Buyers WHERE BuyerID = %s;" % (BuyerID)
        update_result = execute_query(db_connection, query).fetchone()

        if update_result == None:
            query2 = "SELECT * FROM Buyers;"
            cursor = execute_query(db_connection, query2)
            results = cursor.fetchall()
            return render_template("buyers.j2", Buyers=results)
        
        return render_template("buyers_update.j2", Buyer=update_result)

@app.route('/buyers-update', methods=['POST'])
def buyers_update():
    db_connection = connect_to_database()
    BuyerID = request.form['update_button']
    FirstName = request.form['fname_update']
    LastName = request.form['lname_update']
    Email = request.form['email_update']
    Phone = request.form['phone_update']

    query = "UPDATE Buyers SET FirstName = %s, LastName = %s, Email = %s, Phone = %s WHERE BuyerID = %s;"
    data = (FirstName, LastName, Email, Phone, BuyerID)
    execute_query(db_connection, query, data)

    return redirect("./buyers")

@app.route('/sellers', methods=['GET', 'POST'])
def Sellers():
    db_connection = connect_to_database()

    # Display all Sellers
    if request.method == 'GET':
        query = "SELECT * FROM Sellers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        for result in results:
            phone = '('
            phone += result['Phone'][0:3]
            phone += ') - '
            phone += result['Phone'][3:6]
            phone += ' - '
            phone += result['Phone'][6:10]
            result['Phone'] = phone
         # Populate dropdown menus for realtor selection
        query2 = "SELECT FirstName, RealtorID FROM Realtors"
        cursor2 = execute_query(db_connection, query2)
        results2 = cursor2.fetchall()
        
        return render_template("sellers.j2", context={'Sellers':results, 'Realtors':results2})

    # Add a Seller and display updated table
    elif request.method == 'POST' and "add_button" in request.form:
        FirstName = request.form['fname_input']
        LastName = request.form['lname_input']
        Email = request.form['email_input']
        Phone = request.form['phone_input']
        RealtorID = request.form['realtor_input']
        

        # RealtorID is nullable
        if RealtorID == "":
            RealtorID = None
        
        query = "INSERT INTO Sellers (FirstName, LastName, Email, Phone, RealtorID) VALUES (%s, %s, %s, %s, %s);"
        data = (FirstName, LastName, Email, Phone, RealtorID)
        execute_query(db_connection, query, data)

        return redirect("./sellers")
    
    # Delete a Seller and display updated table
    elif request.method == 'POST' and "delete_button" in request.form:
        SellerID = request.form['delete_button']
        query = "DELETE FROM Sellers WHERE SellerID = %s;" % SellerID
        execute_query(db_connection, query)

        return redirect("./sellers")
    
    # Update a Seller if edit button is clicked
    elif request.method == 'POST' and "edit_button" in request.form:
        
        SellerID = request.form['edit_button']

        query = "SELECT * FROM Sellers WHERE SellerID = %s;" % (SellerID)
        update_result = execute_query(db_connection, query).fetchone()

          # Populate dropdown menus for realtor selection
        query3 = "SELECT FirstName, RealtorID FROM Realtors"
        cursor3 = execute_query(db_connection, query3)
        results3 = cursor3.fetchall()


        if update_result == None:
            query2 = "SELECT * FROM Sellers;"
            cursor = execute_query(db_connection, query2)
            results = cursor.fetchall()
            return render_template("sellers_update.j2", context={'Seller':update_result, 'Realtors':results3})

        return render_template("sellers_update.j2", context={'Seller':update_result, 'Realtors':results3})
           

@app.route('/sellers-update', methods=['POST'])
def sellers_update():
    print("Sellers-update page")
    db_connection = connect_to_database()
    print("connected to db")
    SellerID = request.form['update_button']
    print("SellerID Working")
    FirstName = request.form['fname_update']
    print("SellerID Working")
    LastName = request.form['lname_update']
    print("SellerID Working")
    Email = request.form['email_update']
    print("Email Working")
    Phone = request.form['phone_update']
    print("Phone Working")
    RealtorID = request.form['realtor_update']
    print("RealtorID Working")

    print(request.form)

    if RealtorID == "":
        RealtorID = None

    query = "UPDATE Sellers SET FirstName = %s, LastName = %s, Email = %s, Phone = %s, RealtorID = %s WHERE SellerID = %s;"
    data = (FirstName, LastName, Email, Phone, RealtorID, SellerID)
    execute_query(db_connection, query, data)

    return redirect("./sellers")

@app.route('/realtors-buyers', methods=['GET', 'POST'])
def RealtorsBuyers():
    db_connection = connect_to_database()

    # Display all Realtor-Buyer relationships
    if request.method == 'GET':
        query = "SELECT * FROM RealtorsBuyers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("realtors-buyers.j2", RealtorsBuyers=results)

    # Add a Realtor-Buyer relationship and display updated table
    elif request.method == 'POST' and "add_button" in request.form:
        RealtorID = request.form['realtor_id']
        BuyerID = request.form['buyer_id']

        query = "INSERT INTO RealtorsBuyers (RealtorID, BuyerID) VALUES (%s, %s);"
        data = (RealtorID, BuyerID)
        execute_query(db_connection, query, data)

        query2 = "SELECT * FROM RealtorsBuyers;"
        cursor = execute_query(db_connection, query2)
        results = cursor.fetchall()

        return render_template("realtors-buyers.j2", RealtorsBuyers=results)
    
    # Delete a Realtor-Buyer relationship and display updated table
    elif request.method == 'POST' and "delete_button" in request.form:
        RealtorID = request.form['realtor_id']
        BuyerID = request.form['buyer_id']
        query = "DELETE FROM RealtorsBuyers WHERE RealtorID = %s and BuyerID = %s;" % (RealtorID, BuyerID)
        execute_query(db_connection, query)

        query2 = "SELECT * FROM RealtorsBuyers;"
        cursor = execute_query(db_connection, query2)
        results = cursor.fetchall()

        return render_template("realtors-buyers.j2", RealtorsBuyers=results)
    
    # Update a Realtor-Buyer relationship if edit button is clicked
    elif request.method == 'POST' and "edit_button" in request.form:
        RealtorID = request.form['realtor_id']
        BuyerID = request.form['buyer_id']

        query = "SELECT * FROM RealtorsBuyers WHERE RealtorID = %s AND BuyerID = %s;"
        data = (RealtorID, BuyerID)
        update_result = execute_query(db_connection, query, data).fetchone()

        if update_result == None:
            query2 = "SELECT * FROM RealtorsBuyers;"
            cursor = execute_query(db_connection, query2)
            results = cursor.fetchall()
            return render_template("realtors-buyers.j2", RealtorsBuyers=results)
        
        return render_template("realtors-buyers_update.j2", RealtorBuyer=update_result)
        
@app.route('/realtors-buyers-update', methods=['POST'])
def RealtorsBuyersUpdate():
    db_connection = connect_to_database()
    OldRealtor = request.form['old_realtor_id']
    OldBuyer = request.form['old_buyer_id']
    RealtorID = request.form['realtor_id']
    BuyerID = request.form['buyer_id']

    # Will only update row where both RealtorID and BuyerID match
    query = "UPDATE RealtorsBuyers SET RealtorID = %s, BuyerID = %s WHERE RealtorID = %s AND BuyerID = %s;"
    data = (RealtorID, BuyerID, OldRealtor, OldBuyer)
    execute_query(db_connection, query, data)

    return redirect("/realtors-buyers") 


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1115))
    app.run(host='0.0.0.0',port=port, debug=True)