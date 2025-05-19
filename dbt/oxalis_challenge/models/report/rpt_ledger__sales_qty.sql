with dim_store as (
    select * from {{ ref('dim_ledger__store') }}
),

dim_product as (
    select * from {{ ref('dim_ledger__product') }}
),

fct_trans as (
    select * from {{ ref("fct_ledger__transactions") }}
),

prod_sales_agg as (
    select
        t.product_id,
        sum(t.product_quantity) as total_qty_sold,
        sum(case when t.store_id = 5
            then t.product_quantity else 0 end) as store_5_sold,
        sum(case when t.store_id = 6
            then t.product_quantity else 0 end) as store_6_sold,
        sum(case when t.store_id = 7
            then t.product_quantity else 0 end) as store_7_sold
    from
        fct_trans t
    group by 
        product_id
),

prod_sales_disp as (
    select 
        p.product_name as product,
        s.total_qty_sold as total_sold,
        store_5_sold,
        store_6_sold,
        store_7_sold
    from
        dim_product as p
    left join
        prod_sales_agg as s
        on p.product_id = s.product_id
    order by
        s.total_qty_sold desc
)

select * from prod_sales_disp