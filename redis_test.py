import random
import json
import operator
from rediscluster import StrictRedisCluster


redis_node = [
    {"host": "192.168.10.183", "port": "6379"}
]
redis_db = StrictRedisCluster(startup_nodes=redis_node, max_connections=32, decode_responses=True)
pipe = redis_db.pipeline(transaction=False)

rcm = [i for i in redis_db.cluster_nodes() if 'master' in i['flags'] and i['link-state'] == 'connected']
nodes = [i for i in sorted(rcm, key=operator.itemgetter('id'))]
print '========================='
print len(nodes)



rcm = [i for i in redis_db.cluster_nodes() if 'slave' in i['flags'] and i['link-state'] == 'connected']
node = random.choice(rcm)

value = pipe.get("foo")
print "=================" + str(value)
