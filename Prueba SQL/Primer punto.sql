select 
	 to_char(origination_date, 'YYYY-MM') as "Fecha"
	, count(distinct loan_id) as "Total de prestamos"
	, count(distinct client_id) as "Total de usuarios únicos"
	, sum(principal_amount) as "Monto total a capital"

	from loans
/* Para no convertir todos los registros con date() */
	where origination_date between date('2019-01-01')::timestamp and date('2019-10-01')::timestamp 

	group by 1
	desc