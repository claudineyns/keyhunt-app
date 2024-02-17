import hashlib, base58, codecs, ecdsa
from time import time
from random import randrange

hex = list('0123456789abcdef')

def create_wallet(randrange = randrange):
  private_key = ''.join([ hex[randrange(16)] for q in range(64) ])
  return get_address(private_key)

def get_address(private_key):
  '''
  Step 1
  generate an uncompressed public key from the private key that we have
  '''

  # Hex decoding the private key to bytes using codecs library
  private_key_bytes = codecs.decode(private_key, 'hex')
  # Generating a public key in bytes using SECP256k1 & ecdsa library
  public_key_raw = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
  public_key_bytes = public_key_raw.to_string()
  # Hex encoding the public key from bytes
  public_key_hex = codecs.encode(public_key_bytes, 'hex')
  # Bitcoin public key begins with bytes 0x04 so we have to add the bytes at the start
  public_key = (b'04' + public_key_hex).decode("utf-8")

  '''
  Step 2
  Compress the uncompressed public key
  '''

  # Checking if the last byte is odd or even
  if (ord(bytearray.fromhex(public_key[-2:])) % 2 == 0):
    public_key_compressed = '02'
  else:
    public_key_compressed = '03'

  # Add bytes 0x02 to the X of the key if even or 0x03 if odd
  public_key_compressed += public_key[2:66]

  '''
  Step 3
  Perform SHA-256 hashing on the compressed public key
  '''

  # Converting to bytearray for SHA-256 hashing
  hex_str = bytearray.fromhex(public_key_compressed)
  sha = hashlib.sha256()
  sha.update(hex_str)
  public_sha_hex = sha.hexdigest() # .hexdigest() is hex ASCII

  '''
  Step 4
  Perform RIPMED-160 hashing on the result of SHA-256
  '''

  #print(hashlib.algorithms_available)

  rip = hashlib.new('ripemd160')
  rip.update(sha.digest())
  key_hash = rip.hexdigest()

  '''
  Step 5
  Add version byte in front of RIPEMD-160 hash (0x00 for Main Network)
  '''

  modified_key_hash = "00" + key_hash

  '''
  Step 6
  Perform SHA-256 hash on the extended RIPEMD-160 result (Below steps are called Base58Check encoding)
  '''

  sha = hashlib.sha256()
  hex_str = bytearray.fromhex(modified_key_hash)
  sha.update(hex_str)
  key_hash_sha_hex = sha.hexdigest()

  '''
  Step 7
  Perform SHA-256 hash on the result of the previous SHA-256 hash
  '''

  #sha_2 = hashlib.sha256()
  #sha_2.update(sha.digest())
  #sha2_hex = sha_2.hexdigest()

  '''
  Step 8
  Take the first 4 bytes of the second SHA-256 hash, this is the address checksum
  '''

  #checksum = sha_2.hexdigest()[:8]

  '''
  Step 9
  Add the 4 checksum bytes from stage 8 at the end of extended RIPEMD-160 hash from stage 5,
  this is the 25-byte binary Bitcoin Address
  '''

  #byte_25_address = modified_key_hash + checksum

  '''
  Step 10 (Final Result)
  Convert the result from a byte string into a base58 string using Base58Check encoding,
  this is the most commonly used Bitcoin Address format
  '''

  #address = base58.b58encode(bytes(bytearray.fromhex(byte_25_address))).decode('utf-8')

  '''
  Alternative
  After Step 6:
  Making use of b58.encode_check from base58 library directly at Step 6
  '''

  key_bytes = codecs.decode(modified_key_hash, 'hex')
  address2 = base58.b58encode_check(key_bytes).decode('utf-8')

  return address2
