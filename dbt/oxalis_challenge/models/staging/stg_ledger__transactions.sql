with raw_trans as (
    select * from  {{ source('ledger', 'transaction') }}
),

renamed as (
    select
        date as transaction_date,
        store_id,
        quantity as product_quantity,
        price as unit_price,
        transaction_id,
        discount as discount_pct,
        product_name,
        payment_method,
        region as store_region,
        customer_type
    from raw_trans
)

select * from renamed