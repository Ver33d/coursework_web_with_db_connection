select name,material,price
from orders_web o join production p on o.id_tovar=p.item_id where id_order = $id_order