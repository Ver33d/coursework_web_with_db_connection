SELECT month(date_payment),name, id_tovar, sum(payment_amount)
From `liness` t1
join ( select * from `orders` t join `orders_web` tweb on t.id_web_order= tweb.id_order ) t2 on t1.order_id=t2.order_id
join `production` t3 on t2.id_tovar=t3.item_id
Where year(date_payment)='$gener1'
group by month(date_payment),name,id_tovar