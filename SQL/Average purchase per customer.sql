-- part 4  - average purchase amount per customer ---
SELECT 
    c.CustomerID,
    c.CustomerName,
    ROUND(AVG(fs.SalesAmount), 2) AS AvgPurchaseAmount
FROM FactSales fs
JOIN DimCustomer c ON fs.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.CustomerName
ORDER BY AvgPurchaseAmount DESC;