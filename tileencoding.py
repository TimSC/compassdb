
import msgpack, zlib

def WriteTile(objs, fi):
	data = []

	#Count how many times positions are used based on python id (pointer memory location)
	countMap = {}
	for obj in objs:
		for pos in obj.positions:
			pid = id(pos)
			if pid not in countMap:
				countMap[pid] = 0
			countMap[pid] += 1

	#Encode shared nodes
	sharedNodesData = []
	sharedNodesPid = {}
	for obj in objs:

		for pos in obj.positions:
			pid = id(pos)
			count = countMap[pid]
			if count <= 1: continue
			if pid in sharedNodesPid: continue
			sharedNodesPid[pid] = len(sharedNodesData)
			sharedNodesData.append(pos)

	#Convert to native python data types to be suitable for later messagepack encoding
	modObjs = []
	for obj in objs:

		#Encode shared nodes without using shared objects
		posList = []
		for pos in obj.positions:
			pid = id(pos)
			
			if pid not in sharedNodesPid:
				posList.append(pos)
			else:
				posList.append(sharedNodesPid[pid])
	
		modObjs.append((posList, obj.tags, obj.children))

	encoded = msgpack.packb((sharedNodesData, modObjs))
	encodedCompressed = zlib.compress(encoded)

	fi.write(encodedCompressed)

