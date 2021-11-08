-- for displaying tables
SELECT * FROM Listings
SELECT * FROM Realtors
SELECT * FROM Buyers
SELECT * FROM Sellers
SELECT * FROM RealtorsBuyers

-- add a listing
INSERT INTO Listings (Price, StreetAddress, City, State, ZipCode, Description, AnimalsAllowed, BedCount, BathCount, SquareFeet, ListingDate, StoryCount, Garage, RentOrSale, RealtorID, BuyerID, SellerID)
    VALUES (:price_input, :address_input, :city_input, :state_input, :zip_input, :description_input, :animals_input, :beds_input, :baths_input, :squarefeet_input, :date_input, :stories_input, :garage_input, :rentsale_input, :realtor_input, :buyer_input, :seller_input)

-- get data for update listing form
SELECT * FROM Listings WHERE ListingID = :listingid_update

-- update a listing
UPDATE Listings SET Price = :price_update, StreetAddress = :address_update, City = :city_update, State = :state_update, ZipCode = :zip_update, Description = :description_update, AnimalsAllowed = :animals_update, BedCount = :beds_update, BathCount = :baths_update, SquareFeet = :squarefeet_update, ListingDate = :date_update, StoryCount = :stories_update, Garage = :garage_update, RentOrSale = :rentsale_update, RealtorID = :realtor_update, BuyerID = :buyer_update, SellerID = :seller_update
    WHERE ListingID = :listingid_update

-- delete a listing
DELETE FROM Listings WHERE ListingID = :listingid_delete

-- add a realtor
INSERT INTO Realtors (FirstName, LastName, Email, Phone) VALUES (:fname_input, :lname_input, :email_input, :phone_input)

-- get data for update realtor form
SELECT * FROM Realtors WHERE RealtorID = :realtorid_update

-- update a realtor
UPDATE Realtors SET FirstName = :fname_update, LastName = :lname_update, Email = :email_update, Phone = :phone_update WHERE RealtorID = :realtorid_update

-- delete a realtor (also deletes all realtor-buyer relationships associated with the realtor) - how to handle listings and sellers (make not null or delete?)
DELETE FROM Realtors WHERE RealtorID = :realtorid_delete
DELETE FROM RealtorsBuyers WHERE RealtorID = :realtorid_delete

-- add a buyer
INSERT INTO Buyers (FirstName, LastName, Email, Phone) VALUES (:fname_input, :lname_input, :email_input, :phone_input)

-- get data for update buyer form
SELECT * FROM Buyers WHERE BuyerID = :buyerid_update

-- update a buyer
UPDATE Buyers SET FirstName = :fname_update, LastName = :lname_update, Email = :email_update, Phone = :phone_update WHERE BuyerID = :buyerid_update

-- delete a buyer (also deletes all realtor-buyer relationships associated with the buyer)
DELETE FROM Buyers WHERE BuyerID = :buyerid_delete
DELETE FROM RealtorsBuyers WHERE BuyerID = :buyerid_delete

-- add a seller
INSERT INTO Sellers (FirstName, LastName, Email, Phone, RealtorID)
    VALUES (:fname_input, :lname_input, :email_input, :phone_input, (SELECT RealtorID FROM Realtors WHERE FirstName = :realtor_fname_input AND LastName = :realtor_lname_input))

-- get data for update seller form
SELECT * FROM Sellers WHERE SellerID = :sellerid_update

-- update a seller
UPDATE Sellers SET FirstName = :fname_update, LastName = :lname_update, Email = :email_update, Phone = :phone_update, RealtorID = (SELECT RealtorID FROM Realtors WHERE FirstName = :realtor_fname_update AND LastName = :realtor_lname_update) WHERE SellerID = :sellerid_update

-- delete a seller (also deletes all listings associated with the seller)
DELETE FROM Sellers WHERE SellerID = :sellerid_delete
DELETE FROM Listings WHERE SellerID = :sellerid_delete

-- add a realtor-buyer relationship
INSERT INTO RealtorsBuyers (RealtorID, BuyerID)
    VALUES ((SELECT RealtorID FROM Realtors WHERE FirstName = :realtor_fname_input AND LastName = :realtor_lname_input), (SELECT BuyerID FROM Buyers WHERE FirstName = :buyer_fname_input AND LastName = :buyer_lname_input))

-- get data for update realtor-buyer relationship form
SELECT * FROM RealtorsBuyers 
    WHERE RealtorID = (SELECT RealtorID FROM Realtors WHERE FirstName = :realtor_fname_update AND LastName = :realtor_lname_update), BuyerID = (SELECT BuyerID FROM Buyers WHERE FirstName = :buyer_fname_update AND LastName = :buyer_lname_update)

-- update a realtor-buyer relationship
UPDATE RealtorsBuyers SET RealtorID = (SELECT RealtorID FROM Realtors WHERE FirstName = :realtor_fname_update AND LastName = :realtor_lname_update), BuyerID = (SELECT BuyerID FROM Buyers WHERE FirstName = :buyer_fname_update AND LastName = :buyer_lname_update)
    WHERE RealtorID = :realtor_id_from_find_step AND BuyerID = :buyer_id_from_find_step

-- delete a realtor-buyer relationship
DELETE FROM RealtorsBuyers WHERE RealtorID = :realtor_id_delete AND BuyerID = :buyer_id_delete