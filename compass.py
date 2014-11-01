
import msgpack, copy, uuid, os
import slippytiles, tileencoding

class GisObj(object):
	def __init__(self):
		positions = []
		tags = {}
		children = []

class TileBranch(object):
	def __init__(self, x, y, zoom):
		self.tileId = (x, y, zoom)


	def Commit(self, mapObj, commitUuid):
		print "Committing to tile {0}, {1}, {2}".format(*self.tileId)

		#Filter objects to find what is in this tile
		objsWithin = mapObj.GetObjsWithinTile(*self.tileId)
		print "Num objects in tile", len(objsWithin)

		#Save to file
		pth = "tiles"
		if not os.path.exists(pth):
			os.mkdir(pth)
		pth += "/{0}".format(self.tileId[0])
		if not os.path.exists(pth):
			os.mkdir(pth)
		pth += "/{0}".format(self.tileId[1])
		if not os.path.exists(pth):
			os.mkdir(pth)
		fina = pth + "tile.dat"
		fi = open(fina, "wb")

		tileencoding.WriteTile(fi)

		fi.close()


class Map(object):
	def __init__(self):
		self._objs = []
		self.nativeZoom = 12

	def Copy(self):
		return copy.deepcopy(self)

	def AddGisObj(self, gisObj):
		self._objs.append(gisObj)

	def WithinTiles(self):
		out = set()
		for obj in self._objs:
			for pos in obj.positions:
				tilex, tiley = slippytiles.deg2num(pos[0], pos[1], self.nativeZoom)
				out.add((tilex, tiley, self.nativeZoom))
		return out

	def GetObjsWithinTile(self, x, y, zoom):
		nwCorner = slippytiles.num2deg(x, y, zoom)
		seCorner = slippytiles.num2deg(x+1, y+1, zoom)
		print nwCorner, seCorner

		outFiltered = []
		count = 0
		for obj in self._objs:
			within = False
			for pos in obj.positions:
				if pos[0] < seCorner[0] or pos[0] >= nwCorner[0]: continue
				if pos[1] < nwCorner[1] or pos[1] >= seCorner[1]: continue
				within = True
				break
			if within:
				outFiltered.append(obj)

			count += 1
		return outFiltered

class TileManager(object):
	def __init__(self):
		pass

	def Commit(self, mapObj):
		#Check which tiles are referenced
		withinTiles = mapObj.WithinTiles()
		print withinTiles

		commitUuid = uuid.uuid4()

		for tilex, tiley, zoom in withinTiles:
			tile = TileBranch(tilex, tiley, zoom)
			tile.Commit(mapObj, commitUuid)

if __name__ == "__main__":

	sharedPoint = (51.24762292031704, -0.590133572441356)
	currentMap = Map()

	longWay = [(51.25625276724307, -0.5569565354674175),
		(51.25266853326553, -0.5610435318131136),
		(51.2498167331032, -0.5661505613209978),
		(51.248907880503666, -0.5702562124940027),
		(51.249628696108054, -0.5753632420018869),
		(51.249503337684125, -0.5798193755920997),
		(51.248782520114766, -0.5829737173469692),
		(51.24771694301155, -0.5870292996032302),
		sharedPoint,
		(51.24734085108016, -0.5939094804215219),
		(51.2458991368506, -0.5961125127582564),
		(51.24289019635384, -0.5968134775926718),
		(51.241448342606276, -0.5990165099294061),
		(51.23856449951962, -0.600518577431725),
		(51.23467729452127, -0.603222298935899),
		(51.233047078549895, -0.6067271231079763),
		(51.23129139675417, -0.6114336012819089),
		(51.23066435130686, -0.6145378741200347),
		(51.22834420885645, -0.6185433874595516),
		(51.22326456973149, -0.6319618571469335),
		(51.21956423276796, -0.6372691623217938),
		(51.21761986871632, -0.6417753648287504),
		(51.21416998846001, -0.6473830835040743)]

	longWayObj = GisObj()
	longWayObj.positions = longWay
	longWayObj.tags = {"type": "long way"}
	currentMap.AddGisObj(longWayObj)

	shortway = [sharedPoint,
		(51.247168669637766, -0.5884420676103962),
		(51.247201912030505, -0.5871144149645342),
		(51.24804404463198, -0.5849016605547642),
		(51.24798864164526, -0.5836625180852929),
		(51.247712739373924, -0.5822479185608349),
		(51.247712739373924, -0.5797945416403808),
		(51.24821419054396, -0.5758390972176076),
		(51.247963465642414, -0.5703315163757717)]

	shortWayObj = GisObj()
	shortWayObj.positions = longWay
	shortWayObj.tags = {"type": "short way"}
	currentMap.AddGisObj(shortWayObj)

	sharedPoint2 = (51.24373784556225, -0.5957410012035282)
	closeWay = [sharedPoint2, 
		(51.24163228801223, -0.5960242337679789),
		(51.2414278761271, -0.5875932007620944),
		(51.24061272024824, -0.5861819021533217),
		(51.24092302587304, -0.5837744253554917),
		(51.243582702505805, -0.5843054864138366),
		(51.24555519668222, -0.5882353382455883),
		(51.2453335723415, -0.5918819575128893),
		sharedPoint2]

	closeWayObj = GisObj()
	closeWayObj.positions = closeWay
	closeWayObj.tags = {"type": "closed way"}
	currentMap.AddGisObj(closeWayObj)

	point = (51.24109091450995, -0.5899589570782465)
	pointObj = GisObj()
	pointObj.positions = [point]
	pointObj.tags = {"type": "single point"}
	currentMap.AddGisObj(pointObj)
		
	tileManager = TileManager()
	tileManager.Commit(currentMap)

