import hashlib
import sys


fileProxy = open("./servidorProxy.py", "rb")
readFileProxy = fileProxy.read()
hashFileProxy = hashlib.sha224(readFileProxy)
writeHash = open("hashInteg.txt", "w")
writeHash.write(hashFileProxy.hexdigest())