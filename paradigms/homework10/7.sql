select Country.Name
       from Country left join City
       on Country.Code = City.CountryCode
group by Country.Name
having Country.Population > 0 and
       Country.Population > 2 * sum(City.Population)
order by Country.Name;
