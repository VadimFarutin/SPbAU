select First.Name, count(Second.Id) Millionaire
       from Country First left join City Second
       on First.Code = Second.CountryCode and Second.Population >= 1000000
group by First.Name
order by Millionaire desc;
