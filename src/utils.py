from config import cdmSchemaPath

def readFields():
	with open(cdmSchemaPath, 'r') as f:
		lines = f.readlines()
	for line in lines:
		data = line.split(",")
		if len(data) > 2:
			print(data[0],data[1])