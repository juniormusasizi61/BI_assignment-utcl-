-- Part 1 Products that generrate the most revenue -
SELECT 
    p.ProductID,
    p.ProductName,
    p.Category,
    p.SubCategory,
    ROUND(SUM(fs.SalesAmount), 2) AS TotalRevenue
FROM FactSales fs
JOIN DimProduct p ON fs.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName, p.Category, p.SubCategory
ORDER BY TotalRevenue DESC;