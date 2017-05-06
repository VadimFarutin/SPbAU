select StartYear,
       EndYear,
       Name,
       (LiteracyRate.Rate - StartRate) / (EndYear - StartYear) as Growth
       from Country, LiteracyRate,
            (select First.CountryCode as CountryCode,
                    First.Year as StartYear,
                    min(Second.Year) as EndYear,
                    First.Rate as StartRate
                    from LiteracyRate as First, LiteracyRate as Second 
             where First.CountryCode = Second.CountryCode and
                   StartYear < Second.Year
             group by CountryCode, StartYear) as Interval
where Interval.CountryCode = Country.Code and
      Interval.CountryCode = LiteracyRate.CountryCode and
      Interval.EndYear = LiteracyRate.Year
order by Growth desc;
