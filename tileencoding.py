
import msgpack, zlib, uuid, struct
import compass

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
	
		uuidBytes = None
		if obj.uuid is not None:
			uuidBytes = obj.uuid.bytes

		modObjs.append({'p':posList, 't':obj.tags, 'c':obj.children, 'u':uuidBytes})

	encoded = msgpack.packb((sharedNodesData, modObjs))
	encodedCompressed = zlib.compress(encoded)

	fi.write(encodedCompressed)

def ReadTile(fi):

	encoded = zlib.decompress(fi.read())	
	data = msgpack.unpackb(encoded)	

	sharedNodes = data[0]
	objs = data[1]

	#Iterate over shared objects
	for node in sharedNodes:
		pass

	#Iterate over objects
	objsOut = []
	for obj in objs:
		tmpObj = compass.GisObj()
		for pos in obj['p']:
			try:
				iterator = iter(pos)
			except TypeError:
				tmpObj.positions.append(sharedNodes[pos])
			else:
				tmpObj.positions.append(pos)

		tmpObj.tags = obj['t']
		tmpObj.children = obj['c']
		if obj['u'] is not None:
			tmpObj.uuid = uuid.UUID(bytes=obj['u'])
		else:
			tmpObj.uuid = None
		objsOut.append(tmpObj)

	return objsOut

