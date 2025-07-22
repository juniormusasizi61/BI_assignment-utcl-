CREATE DATABASE retail_sales_dw;
USE retail_sales_dw;

CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    UnitPrice DECIMAL(10, 2)
);

CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    Segment VARCHAR(50)
);

CREATE TABLE Region (
    RegionID INT PRIMARY KEY,
    District VARCHAR(50)
);

CREATE TABLE Date (
    DateID INT PRIMARY KEY,
    Date DATE,
    Month INT,
    Year INT
);

CREATE TABLE Sales (
    SaleID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT,
    CustomerID INT,
    RegionID INT,
    DateID INT,
    Quantity INT,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (RegionID) REFERENCES Region(RegionID),
    FOREIGN KEY (DateID) REFERENCES Date(DateID)
);