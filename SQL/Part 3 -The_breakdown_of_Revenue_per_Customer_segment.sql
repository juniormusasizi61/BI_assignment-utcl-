 -- part 3 - The breakdown of revenue per customer segment --
     SELECT 
    c.Segment,
    ROUND(SUM(fs.SalesAmount), 2) AS TotalRevenue
FROM FactSales fs
JOIN DimCustomer c ON fs.CustomerID = c.CustomerID
GROUP BY c.Segment
ORDER BY TotalRevenue DESC;