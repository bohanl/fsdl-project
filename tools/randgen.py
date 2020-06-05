import random
from collections import namedtuple
from itertools import chain
import csv

#
# Random query generator
#
# Input
#   a set of relations
#   a set of FK constraints

FK = namedtuple('FK', 'rel, k1, k2')

relation_joins = {
  'customer': [
    FK(rel='nation', k1='c_nationkey', k2='n_nationkey'),
  ],
  'lineitem': [
    FK(rel='orders', k1='l_orderkey', k2='o_orderkey'),
    FK(rel='partsupp', k1='l_partkey', k2='ps_partkey'),
  ],
  'nation': [
    FK(rel='region', k1='n_regionkey', k2='r_regionkey'),
  ],
  'orders': [
    FK(rel='customer', k1='o_custkey', k2='c_custkey'),
  ],
  'part': [],
  'partsupp': [
    FK(rel='part', k1='ps_partkey', k2='p_partkey'),
    FK(rel='supplier', k1='ps_suppkey', k2='s_suppkey'),
  ],
  'region': [],
  'supplier': [
    FK(rel='nation', k1='s_nationkey', k2='n_nationkey'),
  ],
}

COND = namedtuple('COND', 'col,start,end')

relation_conds = {
  'customer': [
    # COND(col='c_custkey', start=1, end=150000,),  # pk
    COND(col='c_acctbal', start=-917.75, end=9561.95,),
  ],
  'lineitem': [
    # COND(col='l_orderkey', start=1, end=5998726,),  # pk
    # COND(col='l_linenumber', start=1, end=7,),      # pk
    COND(col='l_quantity', start=1.00, end=50.00,),
    COND(col='l_extendedprice', start=951.02, end=101646.50,),
    COND(col='l_discount', start=0.00, end=0.10,),
    COND(col='l_tax', start=0.00, end=0.08,),
   ],
  'orders': [
    # COND(col='o_orderkey', start=1,end=6000000,),  # pk
    COND(col='o_custkey', start=1,end=149999,),
    COND(col='o_totalprice', start=882.72,end=490359.88,),
  ],
  'part': [
    # COND(col='p_partkey', start=1,end=200000,),  # pk
    COND(col='p_retailprice', start=901.00,end=2098.99,),
  ],
  'partsupp': [
    # COND(col='ps_partkey', start=1,end=200000,),  # pk
    # COND(col='ps_suppkey', start=1,end=10000,),   # pk
    COND(col='ps_availqty', start=1,end=9999,),
    COND(col='ps_supplycost', start=1.00,end=1000.00,),
  ],
  'supplier': [
    # COND(col='s_suppkey', start=1,end=10000,),   # pk
    COND(col='s_acctbal', start=-966.20,end=9915.24,),
  ],
}


relations = sorted(relation_joins.keys())
columns = sorted([c.col for c in list(chain(*relation_conds.values()))])

def traverse_graph(target_depth, depth, rels, joins):
    """ Traverse acyclic directed join graph
    to construct the join query.
    @param[in] target_depth the depth to traverse
    @param[in] depth the current depth
    @param[out] list of relations
    @param[out] list of join conditions

    """
    if depth >= target_depth:
      return

    curr_rel = rels[-1]
    if len(relation_joins[curr_rel]) == 0:
        return

    fk = random.choice(relation_joins[curr_rel])

    rels.append(fk.rel)  # add relation
    joins.append("{} = {}".format(fk.k1, fk.k2))  # add join condition

    traverse_graph(target_depth, depth + 1, rels, joins)


def generate_query(rel, n_rels):
    rels, joins, conds = [rel], [], []
    traverse_graph(n_rels - 1, 0, rels, joins)
    query = "SELECT * FROM " + rels[0]
    for i, c in enumerate(joins):
        query += " JOIN {} ON {}".format(rels[i + 1], c)

    where = []
    for r in rels:
        if r not in relation_conds:
            continue
        # randomly select a relation to add
        # the condition clause
        cond = random.choice(relation_conds[r])
        param = random.uniform(cond.start, cond.end)
        where.append("{} >= {:0.2f}".format(cond.col, param))
        percent = round((param - cond.start) / (cond.end - cond.start), 4)
        conds.append((cond, (1. - percent),))
    if where:
        query += (" WHERE " + " AND ".join(where))
    query += ";"
    return query, rels, joins, conds


if __name__ == '__main__':
    query_set = set()
    with open('queries.csv', 'w',) as csvfile:
        query_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for i in range(20000):
            query, rels, joins, conds = generate_query(
                    random.choice([*relation_joins]),
                    random.randint(1, 8))
            if query in query_set:
                continue
            rels_vec, cols_vec = [0] * len(relations), [0] * len(columns)
            for r in rels:
                rels_vec[relations.index(r)] = 1
            for c, p in conds:
                cols_vec[columns.index(c.col)] = p
            query_writer.writerow([query] + rels_vec + cols_vec)
            query_set.add(query)

