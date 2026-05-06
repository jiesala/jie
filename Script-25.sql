#选择数据库
use taobao;

#创建用户表，商品表，用户行为表
create table taobao_user(
	user_id varchar(20) primary key,
	user_gender varchar(20),
	user_age int
);

create table taobao_product(
	product_id varchar(20) primary key,
	product_category varchar(20)
);

create table user_behavior(
	id long auto_increment primary key,
	euser_id varchar(20),
	eproduct_id varchar(20),
	payment_type varchar(20),
	timestamp datetime,
	p_quntity int,
	p_price double,
	constraint fk_user foreign key (euser_id) references taobao_user(user_id),
    constraint fk_product foreign key (eproduct_id) references taobao_product(product_id)
);

#更新user_behavior主键列，让主键列从1开始
set @row_number=0;
update user_behavior
set id = (@row_number := @row_number + 1);

#为用户表添加数据
insert into taobao_user(user_id,user_gender,user_age) 
select distinct customer_id,gender,age from taobao_user_behavior;

#为商品表添加数据
insert into taobao_product(product_id,product_category)
select distinct invoice_no,category from taobao_user_behavior;

#为用户行为表添加数据
insert into user_behavior(euser_id,eproduct_id,payment_type,timestamp,p_quntity,p_price)
select customer_id,invoice_no,payment_method,invoice_date,quantity,price 
from taobao_user_behavior;

#更新价格数据四舍五入保留两位小数
update user_behavior set p_price = round(p_price, 2);

#为构建RFM模型查询数据

select distinct year(timestamp) from user_behavior;#获取最大年分--2023

#获取2023年最大时间戳--2023-3-08
select distinct timestamp 
from user_behavior 
where timestamp >= '2023-01-01 00:00:00' 
  and timestamp <= '2023-12-31 23:59:59'
order by timestamp desc;
#查询R M,并把导入到一个新的表中
create table user_rfm_result as
select
	a.user_id,
	coalesce(datediff('2023-03-08',max(b.timestamp)),999) as recency,
	coalesce(sum(b.p_quntity),0) as frequency,
	coalesce(sum(b.p_price),0) as monetary
from 
	taobao_user a
left join 
	user_behavior b 
on 
	a.user_id=b.euser_id
	and b.timestamp>=date_sub('2023-03-08',interval 365 day)
	and b.timestamp<='2023-03-08'
group by 
a.user_id;
#为标签提供数据基础
create table cluster_analysis_result as
with user_spending as (
    -- 第一步：关联数据
    select
        c.cluster,
        u.user_gender,
        p.product_category,
        b.p_price as spend_amount
    from user_rfm_clustered c
    join user_behavior b on c.user_id = b.euser_id
    join taobao_product p on b.eproduct_id = p.product_id
    join taobao_user u on c.user_id = u.user_id
),
category_stats as (
    -- 第二步：计算每个簇在各品类的消费总额并排名
    select
        cluster,
        product_category,
        sum(spend_amount) as category_total_spend,
        row_number() over (partition by cluster order by sum(spend_amount) desc) as rn
    from user_spending
    group by cluster, product_category
),
cluster_profile as (
    -- 第三步：计算簇的总体特征（性别占比、总消费）
    select
        cluster,
        -- 统计总人数
        count(*) as total_users,
        -- 统计男性人数
        sum(case when user_gender = 'Male' then 1 else 0 end) as male_count,
        -- 统计女性人数
        sum(case when user_gender = 'Female' then 1 else 0 end) as female_count,
        -- 计算簇总消费（用于后续算占比）
        sum(spend_amount) as cluster_total_spend
    from user_spending
    group by cluster
)
-- 第四步：输出最终结果
select
    cp.cluster,
    cp.total_users,
    -- 计算男性占比
    round((cp.male_count / cp.total_users) * 100, 2) as male_pct,
    -- 计算女性占比
    round((cp.female_count / cp.total_users) * 100, 2) as female_pct,
    -- 核心消费品类标签
    cs.product_category as main_category,
    -- 核心品类消费额
    cs.category_total_spend,
    -- 核心品类占该簇总消费的比例
    round((cs.category_total_spend / cp.cluster_total_spend) * 100, 2) as category_spend_pct
from cluster_profile cp
-- 关联品类排名表，只取排名第一的品类 (rn = 1)
join category_stats cs on cp.cluster = cs.cluster and cs.rn = 1
order by cp.cluster;

