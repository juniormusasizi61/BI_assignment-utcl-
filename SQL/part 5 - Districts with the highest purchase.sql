
-- part 5 - districts with the highest sales --
SELECT 
    c.District,
    ROUND(SUM(fs.SalesAmount), 2) AS TotalSales
FROM FactSales fs
JOIN DimCustomer c ON fs.CustomerID = c.CustomerID
GROUP BY c.District
ORDER BY TotalSales DESC;

-- 