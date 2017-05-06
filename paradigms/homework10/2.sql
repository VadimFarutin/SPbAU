select Country.Name, LiteracyRate.Rate from Country, LiteracyRate
where Country.Code = LiteracyRate.CountryCode
group by Country.Name
having LiteracyRate.Year = max(LiteracyRate.Year)
order by LiteracyRate.Rate desc limit 1;
