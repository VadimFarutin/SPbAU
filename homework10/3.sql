select City.Name from City, Capital, Country
where City.Id = Capital.CityId and
      City.CountryCode = Country.Code and
      Country.Name like "Malaysia";
