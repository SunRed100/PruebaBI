with a as(
	select distinct
		client_id

		from(
			select 
			  	l.client_id 
				, sum(l.principal_amount) as "prestamos"		
		

				from loans l
					join clients c using(client_id)		
				where c.city_id = 7 /* Por si el cliente es de una ciudad pero hizo el credito en otra */
				group by 1
			) f
		where prestamos > 10000000

), b as(
	select distinct
		 avg(p.amount)

		from loans l
			join payments p using(loan_id)
			join a on l.client_id = a.client_id

		where p.chanel = 'ELECTRONIC'	
)

select * from b