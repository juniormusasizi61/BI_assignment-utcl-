SELECT SaleID, ProductID, CustomerID, DateID, Quantity, SalesAmount FROM FactSales;
SELECT DateID, FullDate, Month, Quarter, Year FROM DimDate;
SELECT ProductID, ProductName, Category, SubCategory FROM DimProduct;
SELECT CustomerID, CustomerName, Segment, City, District, Country FROM DimCustomer;