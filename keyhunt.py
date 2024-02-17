#!/usr/bin/python3

from wallet import create_wallet, get_address
from random import seed, randrange
from time import time
from datetime import datetime
import redis
import sys

#-----------------------------------------------------------------
args = {}
for q in range(1, len(sys.argv)):
  p = sys.argv[q]
  if p[0:2] != '--': continue
  if not '=' in p: continue
  param = sys.argv[q].split('=')
  args[ param[0][2:] ] = param[1]
#-----------------------------------------------------------------

_redis_h  = args.get('redis_host')
_redis_p  = args.get('redis_port')
_id       = args.get('id')
_interval = args.get('interval')
_address  = args.get('address')

if _interval == None:
  sys.exit('arg "interval" is required')
if _address == None:
  sys.exit('arg "address" is required')

if _redis_h == None:
  _redis_h = 'localhost'

if _redis_p == None:
  _redis_p = '6379'

if _id == None:
  _id = randrange(65536)

r = redis.Redis(host=_redis_h, port=_redis_p, decode_responses=True)

n = int(_id)

addr_info = _interval.split(':')

start_key       = addr_info[0]
end_key         = addr_info[1]
search_address  = _address

#start_key = '10000000'
#end_key   = '1'
#search_address = '19EEC52krRUK1RkUAEZmQdjTyHT7Gp1TYT'

p1 = int(start_key[0], base=16)
p2 = int(end_key[0],   base=16)
k = len(start_key[1:])

base_key = ['0' for q in range(64)]
hex_l = list('0123456789abcdef')

#-----------------------------------------------------------------

sys.stdout.write( '--- searching [{}]---\n'.format(_id) )

seed(time())

me = False

addr = r.get('search_address')
while addr is None or addr == '':

  for q in list(range(k))[::-1]:
    base_key[ -1-q ] = hex_l[ randrange(16) ]

  for q in range(p2 + 1 - p1):
    base_key[-k-1] = hex_l[ p1 + q ]
    private_key = ''.join(base_key)
    address = get_address(private_key)
    short_key = private_key[ -k-1: ]
    # sys.stdout.write('Trying private_key: {} --> address: {}\n'.format(short_key, address))
    if address == search_address:
      r.set('search_address', address)
      me = True
      break

  addr = r.get('search_address')
#-------------------------------------------------------------

if me:
  privKey = (''.join(['0' for q in range(64)]) + short_key)[-64:]
  sys.stdout.write('\n--- found by: {p} ---\nprivate_key: {key} --> address: {address}\n\n'.format(p = _id, key = privKey, address = address) )
else:
  sys.stdout.write('\n--- someone has found the key\n' )

