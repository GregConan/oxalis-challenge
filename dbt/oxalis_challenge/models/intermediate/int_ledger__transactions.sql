with stg_trans as (
    select * from  {{ ref('stg_ledger__transactions') }}
),

-- Calculate extended price (amount * unit price)

ext_price as (
    select
        transaction_id,
        (unit_price * product_quantity) as extended_price
    from stg_trans
),

-- Calculate net price (cost, net of quantity and discount) and
-- total amount of money the customer saved (discount amount)

prices as (
    select 
        x.transaction_id,
        x.extended_price,
        (x.extended_price * (1 + s.discount_pct)) as net_price,
        (x.extended_price * s.discount_pct) as discount_amount
    from
        stg_trans as s
    left join
        ext_price x
        on x.transaction_id = s.transaction_id
),

int_trans as (
    select 
        s.transaction_id,
        s.store_id,
        dense_rank() over (ORDER BY s.product_name) AS "product_id",
        s.transaction_date,
        s.product_quantity,
        s.unit_price,
        s.discount_pct,
        p.discount_amount,
        p.extended_price,
        p.net_price,
        s.product_name,
        s.payment_method,
        s.store_region,
        s.customer_type
    from
        stg_trans as s 
    left join
        prices p
        on p.transaction_id = s.transaction_id
)

select * from int_trans
