with dim_store as (
    select * from {{ ref('dim_ledger__store') }}
),

fct_trans as (
    select * from {{ ref("fct_ledger__transactions") }}
),

store_rev_agg as (
    select 
        store_id,
        sum(net_price) as revenue
    from
        fct_trans
    group by 
        store_id
),

store_rev_join as (
    select 
        d.store_id,
        d.store_region,
        s.revenue
    from
        store_rev_agg as s
    left join
        dim_store as d
        on d.store_id = s.store_id
),

store_rev_disp as (
    select 
        store_id,
        store_region,
        to_char(revenue, '99999999D99') as total_revenue
    from store_rev_join
    order by store_id
)

select * from store_rev_disp

