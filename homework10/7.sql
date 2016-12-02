select First.Name
       from Country First left join City Second
       on First.Code = Second.CountryCode
where First.Population != 0
group by First.Name
having First.Population > 2 * sum(Second.Population) or count(Second.Id) == 0
order by First.Name;
