from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from operator import itemgetter


#Getting the login credentials
lgn = open("login.txt", "r")
credentials = lgn.read().split(" ")
lgn.close()

#setting up driver and first page

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://login1.edupage.org/")

#logging in

wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "skgdFormSubmit")))

username = driver.find_element(By.NAME,"username")
password = driver.find_element(By.NAME,"password")
submit = driver.find_element(By.CLASS_NAME,"skgdFormSubmit")


username.send_keys(credentials[0])
password.send_keys(credentials[1])
submit.click()



#going to the missed classes page and getting the html code
driver.get("https://soaza.edupage.org/dashboard/eb.php?mode=attendance")
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"table.dash_dochadzka.readonly.fixed")))
missing_lessons = driver.find_elements(By.CSS_SELECTOR,"td")


#formatting the html code from the page

counter = 0
temp = ""
lst = []


for i in missing_lessons:

    counter += 1


    if "celý deň" in i.text:

        temp += "full day,"
        counter = 11

    elif i.text == "":

        temp += "a,"

    else:

        temp += f"{i.text},"


    if counter == 12:

        temp = temp[temp.index(',')+2:]

        lst.append(temp)
        counter = 0
        temp = ""


lst.pop()




#getting the timetable 

driver.get("https://soaza.edupage.org/dashboard/eb.php?eqa=bW9kZT10aW1ldGFibGU%3D")
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"g")))
lessons = driver.find_elements(By.CSS_SELECTOR,"text[text-anchor='middle']")


timetable = []


for i in lessons:
    timetable.append([i.text, float(i.get_attribute('x')), float(i.get_attribute('y'))])


del timetable[0:24]


sorted(timetable, key=itemgetter(2))

day = []
sorted_table = []
y_height = timetable[0][2]

for i in timetable:
    if i[2] != y_height:
        sorted_table.append(day)
        day = []
        y_height=i[2]

    day.append(i)

sorted_table.append(day)


def shorten_entries(table):
    tmp_table = []
    for i in table:
        tmp_table.append(i[0])
    return tmp_table


final_table = []

for i in sorted_table:

    final_table.append(shorten_entries(sorted(i, key=itemgetter(1))))



#FINAL MATCHING OF LISTS

days = {
    "Pondelok" : 1,
    "Utorok" : 2,
    "Streda" : 3,
    "Štvrtok" : 4,
    "Piatok" : 5
}


print(final_table)
print(lst)

final_missed = []


print(final_missed)

driver.quit()