select Country.Name
       from Country left join City
       on Country.Code = City.CountryCode
group by Country.Name
having Country.Population > 2 * sum(coalesce(City.Population, 0))
order by Country.Name;
