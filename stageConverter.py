lavaRoof = "lava2,{0},0,150,100,lava2.png\n"
lavaFloor = "lava,{0},600,150,100,lava.png\n"
ground = "layer2,{0},600,150,100,layer2.png\n"
roof = "layer3,{0},0,150,100,layer3.png\n"
blueCoin = "blueCoin,{0},{1},57,65,6,3,blueCoin.png\n"
blueDimond = "blueDimond,{0},{1},56,60,6,7,blueDimond.png\n"
redCoin ="redCoin,{0},{1},58,65,6,2,redCoin.png\n"
redDimond = "redDimond,{0},{1},54,60,6,10,redDimond.png\n"
goldCoin = "goldCoin,{0},{1},53,60,6,1,goldCoin.png\n"
smallRock= "smallRock,{0},{1},80,80,40,smallRock.png\n"
mediumRock="mediumRock,{0},{1},110,110,55,mediumRock.png\n"
bigRock="bigRock,{0},{1},140,140,70,bigRock.png\n"
flag = "flag,{0},{1},100,100,flag.png\n"

# p="Platform,{0},{1},200,52\n" # x, y
# g="Gomba,{0},{1},{2},35,70,70,5,gomba.png\n" # x, y, g
# s="Star,{0},{1},-1,20,40,40,6,star.png,{2},{3},False\n" # x,y,theta,radius
# m="Mario,{0},{1},{2},39,78,78,4,marioRun.png\n" #x, y, g


file = open("bear.csv","r")
lavafallStage=file.read().split("\n")[:]
file.close()

file = open("lavafall.csv","w")
y = 0
for line in lavafallStage:
	line = line.split(",")
	x = 0
	for segment in line:
		if segment == 'lava2':
			file.write(lavaRoof.format(x))
		elif segment == 'lava':
			file.write(lavaFloor.format(x))
		elif segment == 'layer2':
			file.write(ground.format(x))
		elif segment == 'layer3':
			file.write(roof.format(x))
		elif segment == 'blueCoin':
			file.write(blueCoin.format(x,y))
		elif segment == 'blueDimond':
			file.write(blueDimond.format(x,y))
		elif segment == 'redCoin':
			file.write(redCoin.format(x,y))
		elif segment == 'redDimond':
			file.write(redDimond.format(x,y))
		elif segment == 'goldCoin':
			file.write(goldCoin.format(x,y))
		elif segment == 'smallRock':
			file.write(smallRock.format(x,y))
		elif segment == 'mediumRock':
			file.write(mediumRock.format(x,y))
		elif segment == 'bigRock':
			file.write(bigRock.format(x,y))
		elif segment == 'flag':
			file.write(flag.format(x,y))
		x+=5
	y+=5
file.close()
