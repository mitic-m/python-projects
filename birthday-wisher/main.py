##################### Hard Starting Project ######################

import datetime as dt
import pandas
import random
import smtplib

MY_EMAIL = "marko.practice26@gmail.com"
MY_PASSWORD = "udrw tiha ezhh zvvu"

now = dt.datetime.now()
today_day = now.day
today_month = now.month

data = pandas.read_csv("birthdays.csv")

#dict comprehension
birthdays_dict = {(row.month, row.day) : row for (index, row) in data.iterrows()}

if (today_month, today_day) in birthdays_dict:
    #getting person which birthday is today
    birthday_person = birthdays_dict.get((today_month, today_day))
    #generating random number for choosing random letter
    random_file_number = random.choice(range(1, 4))
    #generating file path
    file_path = f"letter_templates/letter_{random_file_number}.txt"
    with open(file_path) as letter_file:
        #reading letter and saving it to variable
        contents = letter_file.read()
        #replacing placeholder with real name
        letter = contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=birthday_person["email"],
                            msg=f"Subject: Happy Birthday\n\n{letter}")



