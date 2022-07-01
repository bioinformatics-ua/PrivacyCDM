from config import cdmSchemaPath

def readFields():
	with open(cdmSchemaPath, 'r') as f:
		lines = f.readlines()
	for line in lines:
		data = line.split(",")
		if len(data) > 2:
			print(data[0],data[1])

def processAttributes(listOfAttributes):
	dictOfAttributes = {}
	for table, field in listOfAttributes:
		table = table.lower()
		if table not in dictOfAttributes:
			dictOfAttributes[table] = []
		dictOfAttributes[table].append(field.lower())
	return dictOfAttributes

def attibutesToLatexTable(dictOfAttributes):
	for table in dictOfAttributes:
		tableToPrint = table.replace("_", "\\_")
		print("\t" + tableToPrint, end = ' & ')
		tableFields = ""
		for field in dictOfAttributes[table]:
			tableFields += field
			tableFields += ", "
		tableFields = tableFields[:-2]
		tableFields += " \\\\  \\hline"
		tableFields = tableFields.replace("_", "\\_")
		print(tableFields)