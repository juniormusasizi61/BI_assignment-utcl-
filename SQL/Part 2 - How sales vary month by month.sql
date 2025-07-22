-- part 2- How sales vary month by month --
SELECT 
    d.Year,
    d.Month,
    ROUND(SUM(fs.SalesAmount), 2) AS TotalSales
FROM FactSales fs
JOIN DimDate d ON fs.DateID = d.DateID
GROUP BY d.Year, d.Month
ORDER BY 
    d.Year,
    FIELD(d.Month, 'January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December', 'Unknown');