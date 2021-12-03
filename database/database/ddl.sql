-- adds Realtors table and attributes to database; RealtorID is a foreign key to the Sellers, Listings, RealtorsBuyers tables
CREATE TABLE IF NOT EXISTS Realtors (
    RealtorID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    CONSTRAINT Full_Name UNIQUE (FirstName, LastName)
);

-- adds Buyers table and attributes to database; BuyerID is a fk to the Listings and RealtorsBuyers tables
CREATE TABLE IF NOT EXISTS Buyers (
    BuyerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    CONSTRAINT Full_Name UNIQUE (FirstName, LastName)
);

-- adds Sellers table and attributes to database; SellerID is a fk to the Listings table, if a realtor is deleted associated seller rows are updated
CREATE TABLE IF NOT EXISTS Sellers (
    SellerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    RealtorID INT,
    FOREIGN KEY (RealtorID) REFERENCES Realtors(RealtorID)
    ON DELETE SET NULL
);

-- adds Listings table and attributes to database; if a seller is deleted associated listings are deleted, if a buyer or realtor are deleted associated listings are updated
CREATE TABLE IF NOT EXISTS Listings (
    ListingID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Price INT NOT NULL,
    StreetAddress VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    State VARCHAR(2) NOT NULL,
    ZipCode INT NOT NULL,
    Description TEXT,
    AnimalsAllowed BOOLEAN NOT NULL,
    BedCount INT NOT NULL,
    BathCount INT NOT NULL,
    SquareFeet INT NOT NULL,
    ListingDate DATE NOT NULL,
    StoryCount INT NOT NULL,
    Garage INT NOT NULL,
    RentOrSale BOOLEAN NOT NULL,
    RealtorID INT,
    FOREIGN KEY (RealtorID) REFERENCES Realtors(RealtorID)
    ON DELETE SET NULL,
    BuyerID INT,
    FOREIGN KEY (BuyerID) REFERENCES Buyers(BuyerID)
    ON DELETE SET NULL,
    SellerID INT NOT NULL,
    FOREIGN KEY (SellerID) REFERENCES Sellers(SellerID)
    ON DELETE CASCADE,
    CONSTRAINT full_address UNIQUE (StreetAddress,City,State,ZipCode)
);

-- add M:M table for Realtors and Buyers; if a realtor or buyer is deleted, all associated entries in the table are deleted
CREATE TABLE IF NOT EXISTS RealtorsBuyers (
    RealtorID INT NOT NULL,
    FOREIGN KEY (RealtorID) REFERENCES Realtors(RealtorID)
    ON DELETE CASCADE,
    BuyerID INT NOT NULL,
    FOREIGN KEY (BuyerID) REFERENCES Buyers(BuyerID)
    ON DELETE CASCADE
);


-- insert sample data
INSERT INTO Realtors (FirstName, LastName, Email, Phone) VALUES ('John', 'Doe', 'john.doe@stricklandrealty.com', '1234567890');
INSERT INTO Buyers (FirstName, LastName, Email, Phone) VALUES ('Jane', 'Smith', 'jsmith@sample.com', '9876543210');
INSERT INTO Sellers (FirstName, LastName, Email, Phone, RealtorID) VALUES ('Hank', 'Hill', 'assistantmanager@stricklandpropane.com', '1111111111', 1);
INSERT INTO Listings (Price, StreetAddress, City, State, ZipCode, Description, AnimalsAllowed, BedCount, BathCount, SquareFeet, ListingDate, StoryCount, Garage, RentOrSale, RealtorID, BuyerID, SellerID)
    VALUES (239000, '84 Rainey St', 'Arlen', 'TX', 73104, 'Sample text', 1, 3, 2, 1500, '2021-11-08', 1, 1, 1, 1, 1, 1);
INSERT INTO RealtorsBuyers (RealtorID, BuyerID) VALUES (1, 1);