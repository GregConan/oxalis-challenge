with dim_product as (
    select distinct
        product_id,
        product_name, 
        unit_price
    from {{ ref('int_ledger__transactions') }}
)

select * from dim_product