
months = ("enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre")

for index_month, month in enumerate(months):
	print("<div class='month'>")
	print("<h2 class='month_name'>",month,"</h2>")
	print("<div class='month_days'>")

	index_month = "0"+str(index_month+1) if len(str(index_month)) == 1 else index_month+1

	for day in range(1,32):
		print("<div class='day'>")
		print("<p>",str(day),"</p>")

		if len(str(day)) == 1: day = "0"+str(day)
		date = str(day) + "-" + str(index_month)


		# print(day,index_month)
		print("<div class='day_offers' id='vuelta"+date+"'>")
		print("</div>")
		print("</div>")

	print("</div>")

	print("</div>")
	print()
