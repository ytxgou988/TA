#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

cache = redis.StrictRedis(host = 'localhost', port = 6379)
print cache.lrange('pkg', 0, -1)
for i in range(cache.llen('pkg')):
    cache.rpop('pkg')
    cache.flushall()
print cache.lrange('pkg', 0, -1)
