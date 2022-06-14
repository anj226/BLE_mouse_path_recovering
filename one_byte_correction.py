from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes

def e(key, plaintext):
    plaintext = long_to_bytes(plaintext)
    if len(plaintext) < 16:
        plaintext = b'\x00' + plaintext
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return bytes_to_long(ciphertext)

def p1(pres, preq, rat, iat):
    return (pres << 72) + (preq << 16) + (rat << 8) + iat 

def p2(ia, ra):
    return (ia << 48) + ra

def c1(k, r, pres, preq, rat, iat, ia, ra):
    _p1 = p1(pres, preq, rat, iat)
    _p2 = p2(ia, ra)
    return hex( e(k, e(k, r ^ _p1) ^ _p2 ) )

def error_byte_detect(key, slave_r, pres, preq, rat, iat, ia, ra, confirm):
    for i in range(16):
        for b in range(256):
            test_r = (slave_r ^ (slave_r & (0xFF << (i*8)) )) + (b << (i*8))
            # print(hex(test_r))
            if c1(key, test_r, pres, preq, rat, iat, ia, ra) == confirm:
                return test_r

# The sample data we captured from our experiment
key = b'\x00'*16            #In BLE Legacy - Just works the Temporary Key is set to 0
preq = 0x0f0d102d000101
pres = 0x03011001000302
iat, rat = 0, 1
ia = 0x14abc5ec6bbf
ra = 0xe01098104d6b
master_r = 0x1b909dd0fa6c13dd29ad0453f2325385
slave_r = 0x59937f6155abc12aaa8934489a84c444
master_confirm = 0xb3cc6450b12f0faa3ebcd71835f20e06
slave_confirm = 0x62ee2712f8771e10997c99c11dd04c5d

if c1(key, master_r, pres, preq, rat, iat, ia, ra) != hex(master_confirm):
    print("Master random is error!")
    master_r = error_byte_detect(key, master_r, pres, preq, rat, iat, ia, ra, hex(master_confirm))
    print(f"The right master random shoud be {hex(master_r)}.")

if c1(key, slave_r, pres, preq, rat, iat, ia, ra) != hex(slave_confirm):
    print("Slave random is error!")
    slave_r = error_byte_detect(key, slave_r, pres, preq, rat, iat, ia, ra, hex(slave_confirm))
    print(f"The right slave random shoud be {hex(slave_r)}.")

_r = ((slave_r % (1 << 64)) << 64) + master_r % (1 << 64)

STK = e(key, _r)
print(f"The STK(short term key) is {hex(STK)}.")
