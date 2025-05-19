with fct_trans as (
    select
        transaction_date,
        store_id,
        product_quantity,
        transaction_id,
        discount_pct,
        discount_amount,
        extended_price,
        net_price,
        product_id,
        payment_method,
        customer_type
    from {{ ref('int_ledger__transactions') }}
)

select * from fct_trans