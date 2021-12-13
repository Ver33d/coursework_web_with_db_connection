select category, material, name, date_receipt, unit, price_unit, quantity_warehause
from `production`
where item_id in(select id_tovar from (select * from `orders` t join
 `orders_web` tweb on t.id_web_order= tweb.id_order) itemm
where price=(select max(price) from `orders`
where year(date_receipt)='$gener1' and month(date_receipt)='$gener3'))