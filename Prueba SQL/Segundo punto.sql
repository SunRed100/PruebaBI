
select 
	count(distinct f.client_id) filter (where f.prestamos >= 3) as Total


	from(
		select 
			  client_id 
			, count(distinct loan_id) as "prestamos"		
		

			from loans		

			group by 1
		) f