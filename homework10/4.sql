select Country.Name,
       count(case when Country.Code = City.CountryCode and
                       City.Population >= 1000000
                  then 1 else null end) Millionaire
       from Country, City
group by Country.Name
order by Millionaire desc;
