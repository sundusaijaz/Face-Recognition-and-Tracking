import datetime
dob = '26/4/2000'
dob_day = int(dob.split("/")[0])
dob_month = int(dob.split("/")[1])
dob_year = int(dob.split("/")[2])
today_day = datetime.datetime.now().day
today_month = datetime.datetime.now().month
today_year = datetime.datetime.now().year



#age of user
difference_age = today_year-dob_year
if today_month < dob_month:
  print(f"age is : {difference_age-1}")
elif today_month > dob_month:
  print(f"age is : {difference_age}")
else:
  if today_month == dob_month:
    if today_day < dob_day:
      print(f"age is : {difference_age-1}")
    else:
      print(f"age is : {difference_age}")
  else:
    print(f"age is : {difference_age}")

#calculating how many days left in next birthday
isPassed = None 
if dob_month > today_month:
  #dob not passed
  difference  = (dob_month - today_month)*30 
  if dob_day > today_day:
    difference = difference + (dob_day-today_day)
  elif dob_day < today_day:
    difference = difference - (today_day-dob_day)
  print(f"{difference} days to your BDAY remains")
elif dob_month < today_month:
  #dob is passed
  difference = (12 - today_month) * 30 + ((dob_month)*30)
  if dob_day > today_day:
    difference = difference + (dob_day-today_day)
  #dob hasn't passed
  elif dob_day < today_day:
    difference = difference - (today_day-dob_day)
  
  print(f"{difference} days to your BDAY remans")
#for the same month
if dob_month == today_month:
    if dob_day == today_day:
      print("365 days remaning")
    elif dob_day > today_day:
      day = dob_day - today_day
      print(f"{day} days to your BDAY are remaining")
    else:
      print(f"{365- (today_day - dob_day)} days remains")


