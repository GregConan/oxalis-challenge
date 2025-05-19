with dim_store as (
    select distinct store_id, store_region
    from {{ ref('int_ledger__transactions') }}
)

select * from dim_store
