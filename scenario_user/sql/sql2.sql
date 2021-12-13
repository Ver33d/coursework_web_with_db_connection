select date_payment,sum(payment_amount)
from `liness`
where year(date_payment)='$gener1' and month(date_payment)='$gener2'
group by date_payment