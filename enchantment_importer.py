table_file = input("Input table txt file from https://minecraft.wiki/w/Enchanting#Summary_of_enchantments\n>")
table = open(table_file).read()

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
	else:
		row_split=row.split("\t")
		if len(row_split) > 1 and roman_numerals[row_split[4].lower()] > 1:
			for book_num in range(roman_numerals[row_split[4].lower()]):
				print("book_of_"+row_split[0].lower().replace(" ","_")+"_"+str(book_num+1))
		else:
			print("book_of_"+row_split[0].lower().replace(" ","_"))
