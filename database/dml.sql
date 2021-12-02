-- for displaying tables
SELECT * FROM Listings;
SELECT * FROM Realtors;
SELECT * FROM Buyers;
SELECT * FROM Sellers;
SELECT * FROM RealtorsBuyers;

-- add a listing
-- colon character : is used to denote variables that will have data from the backend programming language
INSERT INTO Listings (Price, StreetAddress, City, State, ZipCode, Description, AnimalsAllowed, BedCount, BathCount, SquareFeet, ListingDate, StoryCount, Garage, RentOrSale, RealtorID, BuyerID, SellerID);
    VALUES (:price_input, :address_input, :city_input, :state_input, :zip_input, :description_input, :animals_input, :beds_input, :baths_input, :squarefeet_input, :date_input, :stories_input, :garage_input, :rentsale_input, :realtor_input, :buyer_input, :seller_input);

-- get data for update listing form
SELECT * FROM Listings WHERE ListingID = :listingid_update;

-- for displaying names in dropdown menus
SELECT FirstName, RealtorID FROM Realtors;
SELECT FirstName, BuyerID FROM Buyers;
SELECT FirstName, SellerID FROM Sellers;

-- update a listing
UPDATE Listings SET Price = :price_update, StreetAddress = :address_update, City = :city_update, State = :state_update, ZipCode = :zip_update, Description = :description_update, AnimalsAllowed = :animals_update, BedCount = :beds_update, BathCount = :baths_update, SquareFeet = :squarefeet_update, ListingDate = :date_update, StoryCount = :stories_update, Garage = :garage_update, RentOrSale = :rentsale_update, RealtorID = :realtor_update, BuyerID = :buyer_update, SellerID = :seller_update
    WHERE ListingID = :listingid_update;

-- to search any attribute in listings
SELECT * FROM Listings WHERE Price LIKE '%:search_input%' OR StreetAddress LIKE '%:search_input%' OR City LIKE '%:search_input%' OR State LIKE '%:search_input%' OR ZipCode LIKE '%:search_input%' OR Description LIKE '%:search_input%' OR AnimalsAllowed LIKE '%:search_input%' OR BedCount LIKE '%:search_input%' OR BathCount LIKE '%:search_input%' OR SquareFeet LIKE '%:search_input%' OR ListingDate LIKE '%:search_input%' OR StoryCount LIKE '%:search_input%' OR Garage LIKE '%:search_input%' OR RentOrSale LIKE '%:search_input%' OR RealtorID LIKE '%:search_input%' OR BuyerID LIKE '%:search_input%' OR SellerID LIKE '%:search_input%';

-- delete a listing
DELETE FROM Listings WHERE ListingID = :listingid_delete;

-- add a realtor
INSERT INTO Realtors (FirstName, LastName, Email, Phone) VALUES (:fname_input, :lname_input, :email_input, :phone_input);

-- get data for update realtor form
SELECT * FROM Realtors WHERE RealtorID = :realtor_id_update;

-- update a realtor
UPDATE Realtors SET FirstName = :fname_update, LastName = :lname_update, Email = :email_update, Phone = :phone_update WHERE RealtorID = :realtor_id_update;

-- delete a realtor (also deletes all realtor-buyer relationships associated with the realtor)
DELETE FROM Realtors WHERE RealtorID = :realtor_id_delete;

-- add a buyer
INSERT INTO Buyers (FirstName, LastName, Email, Phone) VALUES (:fname_input, :lname_input, :email_input, :phone_input);

-- get data for update buyer form
SELECT * FROM Buyers WHERE BuyerID = :buyer_id_update;

-- update a buyer
UPDATE Buyers SET FirstName = :fname_update, LastName = :lname_update, Email = :email_update, Phone = :phone_update WHERE BuyerID = :buyer_id_update;

-- delete a buyer (also deletes all realtor-buyer relationships associated with the buyer)
DELETE FROM Buyers WHERE BuyerID = :buyer_id_delete;

-- add a seller
INSERT INTO Sellers (FirstName, LastName, Email, Phone, RealtorID);
    VALUES (:fname_input, :lname_input, :email_input, :phone_input, :realtor_id_input);

-- get data for update seller form
SELECT * FROM Sellers WHERE SellerID = :seller_id_update;

-- update a seller
UPDATE Sellers SET FirstName = :fname_update, LastName = :lname_update, Email = :email_update, Phone = :phone_update, RealtorID = :realtor_id_update WHERE SellerID = :seller_id_update;

-- delete a seller (also deletes all listings associated with the seller)
DELETE FROM Sellers WHERE SellerID = :seller_id_delete;

-- add a realtor-buyer relationship
INSERT INTO RealtorsBuyers (RealtorID, BuyerID)
    VALUES (:realtor_id_input, :buyer_id_input);

-- get data for update realtor-buyer relationship form
SELECT * FROM RealtorsBuyers 
    WHERE RealtorID = :realtor_id_update, BuyerID = :buyer_id_update;

-- update a realtor-buyer relationship
UPDATE RealtorsBuyers SET RealtorID = :realtor_id_new, BuyerID = :buyer_id_new
    WHERE RealtorID = :realtor_id_from_find_step AND BuyerID = :buyer_id_from_find_step;

-- delete a realtor-buyer relationship
DELETE FROM RealtorsBuyers WHERE RealtorID = :realtor_id_delete AND BuyerID = :buyer_id_delete;
