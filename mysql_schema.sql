/* TPCH MySQL schema */

create table part
   (p_partkey             int                     not null primary key,
    p_name                varchar(55)             not null,
    p_mfgr                char(25)                not null,
    p_brand               char(10)                not null,
    p_type                varchar(25)             not null,
    p_size                int                     not null,
    p_container           char(10)                not null,
    p_retailprice         decimal(15,2)           not null,
    p_comment             varchar(23)             not null);

create table supplier
  (s_suppkey             int                    not null primary key,
   s_name                char(25)               not null,
   s_address             char(40)               not null,
   s_nationkey           int                    not null,
   s_phone               char(15)               not null,
   s_acctbal             decimal(15,2)          not null,
   s_comment             varchar(101)           not null);

create table partsupp
 (ps_partkey    int                    not null,
  ps_suppkey    int                    not null,
  ps_availqty   int                    not null,
  ps_supplycost decimal(15,2)          not null,
  ps_comment    varchar(199)           not null,
  constraint ps_pk primary key (ps_partkey, ps_suppkey));

create table customer
  (c_custkey     int                    not null primary key,
   c_name        varchar(25)            not null,
   c_address     varchar(40)            not null,
   c_nationkey   int                    not null,
   c_phone       char(15)               not null,
   c_acctbal     decimal(15,2)          not null,
   c_mktsegment  char(10)               not null,
   c_comment     char(117)              not null);

create table orders
  (o_orderkey      int                  not null primary key,
   o_custkey       int                  not null,
   o_orderstatus   char(1)              not null,
   o_totalprice    decimal(15,2)        not null,
   o_orderdate     datetime             not null,
   o_orderpriority char(15)             not null,
   o_clerk         char(15)             not null,
   o_shippriority  int                  not null,
   o_comment       varchar(79)          not null);

create table lineitem
  (l_orderkey               int           not null,
   l_partkey                int           not null,
   l_suppkey                int           not null,
   l_linenumber             int           not null,
   l_quantity               decimal(15,2) not null,
   l_extendedprice          decimal(15,2) not null,
   l_discount               decimal(15,2) not null,
   l_tax                    decimal(15,2) not null,
   l_returnflag             char(1)       not null,
   l_linestatus             char(1)       not null,
   l_shipdate               datetime      not null,
   l_commitdate             datetime      not null,
   l_receiptdate            datetime      not null,
   l_shipinstruct           char(25)      not null,
   l_shipmode               char(10)      not null,
   l_comment                varchar(44)   not null,
   constraint l_pk primary key (l_orderkey, l_linenumber));

create table nation
  (n_nationkey        int          not null primary key,
   n_name             char(25)     not null,
   n_regionkey        int          not null,
   n_comment          varchar(152) not null);

create table region
  (r_regionkey        int          not null primary key,
   r_name             char(25)     not null,
   r_comment          varchar(152) not null);

alter table supplier add constraint fknation foreign key (s_nationkey) references nation (n_nationkey);

alter table customer add constraint fkcnation foreign key (c_nationkey) references nation (n_nationkey);

alter table orders add constraint fkcust foreign key (o_custkey) references customer (c_custkey);

alter table lineitem add constraint fkorders foreign key (l_orderkey) references orders (o_orderkey);

alter table lineitem add constraint fkpps foreign key (l_partkey, l_suppkey) references partsupp (ps_partkey, ps_suppkey);

alter table nation add constraint fkregion foreign key (n_regionkey) references region (r_regionkey);

alter table partsupp add constraint fkp foreign key (ps_partkey) references part(p_partkey);

alter table partsupp add constraint fks foreign key (ps_suppkey) references supplier(s_suppkey);

alter table lineitem add constraint partkeyFK foreign key (l_partkey) references part (p_partkey);

alter table lineitem add constraint suppkeyFK foreign key (l_suppkey) references supplier (s_suppkey);

/* eof */
