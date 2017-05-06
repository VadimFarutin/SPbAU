select Name, count(Id) MillionaireCount
       from Country left join (select CountryCode, Id
                                      from City
                               where Population >= 1000000)
       on Code = CountryCode
group by Name
order by MillionaireCount desc;
