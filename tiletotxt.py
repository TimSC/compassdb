
import zlib, msgpack

if __name__ == "__main__":
	fina = "/home/tim/dev/compassdb/tiles/2041/1366/tile.dat"
	encoded = zlib.decompress(open(fina, "rb").read())	
	data = msgpack.unpackb(encoded)
	print data

