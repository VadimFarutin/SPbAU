select Country.Name,
	   Country.Population,
       Country.SurfaceArea from Country, City, Capital,
							    (select Country.Code as Code,
									    max(City.Population) as MaxPopulation
									    from Country, City
							     where Country.Code = City.CountryCode
							     group by Country.Name) as MaxPopulationCity
where MaxPopulationCity.Code = Country.Code and
	  MaxPopulationCity.Code = City.CountryCode and
	  City.Id = Capital.CityId and
	  City.Population != MaxPopulation
group by (1.0 * Country.SurfaceArea / Country.Population);

