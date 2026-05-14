create table user
(
    name_id     int auto_increment comment '用户ID，主键自增'
        primary key,
    name        varchar(50)                        not null comment '用户名',
    password    varchar(100)                       not null comment '用户密码（建议存储加密后密码）',
    create_time datetime default CURRENT_TIMESTAMP null comment '创建时间，默认当前时间',
    up_time     datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '更新时间，修改时自动更新'
)
    comment '用户基础信息表' charset = utf8mb4;

create table user_token
(
    id        int auto_increment comment '主键ID，自增'
        primary key,
    name_id   int                                not null comment '关联user表的用户ID',
    name      varchar(50)                        null,
    token     varchar(255)                       not null comment '用户登录令牌',
    expire_at datetime default CURRENT_TIMESTAMP null comment '过期时间',
    create_at datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '创建时间'
)
    comment '用户令牌信息表' charset = utf8mb4;

create index idx_name_id
    on user_token (name_id)
    comment '为关联字段创建索引，提升查询效率';