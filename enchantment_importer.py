table_file = input("Input table txt file from https://minecraft.fandom.com/wiki/Enchanting#Summary_of_enchantments\n>")
table = open(table_file,"rb").read().decode()

roman_numerals = {
	"i": 1,
	"ii": 2,
	"iii": 3,
	"iv": 4,
	"iiii": 4,
	"v": 5
}

for row in table.split("\n"):
	if "soul speed" in row.lower():
		print("Skipped",row,"as villagers don't sell soul speed'")
	print(row.split("\t"))
