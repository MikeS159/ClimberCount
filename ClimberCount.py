import bs4 as bs
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
url = "https://portal.rockgympro.com/portal/public/c3b9019203e4bc4404983507dbdf2359/occupancy?&iframeid=occupancyCounter&fId=1644"      #Link for RCC counter that gets embedded
driver.get(url) #Need selenium because the count is produced by JS
html = driver.page_source
soup = bs.BeautifulSoup(html, features="lxml")
lines = soup.text.split("\n")
now = datetime.now()
now = now - timedelta(hours=1)  #Subtract 1 hour because my server is in France....
dt_string = now.strftime("%d/%m/%Y %a %H:%M")
#print(dt_string)
#print(span.text)
counts = []
for l in lines:
    if "'count' :" in l:
        counts.append(l)
count = counts[2]       #Couldn't accuractly get RCC count, for some reason using the span would sometimes return count for MCC or HCC. So yay... manul hack, should probably error handle here...
count = count.replace("'count' :", "")
count = count.replace(",", "")
count = count.replace(" ", "")

with open("ClimberCount.csv", "a") as myfile:
    myfile.write(dt_string + "," + count + "\n")

driver.quit()   #Don't forget to quit browser or it will eat up all your RAM
