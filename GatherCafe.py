from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
#URL of the webpage to scrape the data
URL="https://www.google.com/search?sa=X&sca_esv=e197cb97d6e85975&sca_upv=1&rlz=1C1CHBF_en-GBAU925AU925&sxsrf=ADLYWIIb-MVHYsYRGdmtsw2Tv4hICIuiZA:1720090102107&q=Breakfast+cafes+and+restaurants+near+me&ved=2ahUKEwia5JH8mo2HAxXisFYBHcvNBvYQuzF6BAgFEAQ&biw=1366&bih=641&dpr=1"
mapbase_url= "https://www.google.com/maps/search/?api=1&query="
#List for the cafes info
addresses=[]
names=[]
ratings=[]
reviews=[]
phones=[]
prices=[]
types=[]

#Create a database
conn=sqlite3.connect("instance/resturants.db")
cur=conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        address TEXT,
        ratings TEXT,
        reviews TEXT,
        price_range TEXT,
        phone_number TEXT
    )
''')
conn.commit()
conn.close()
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver=webdriver.Chrome(options=chrome_options)
driver.get(URL)

conn=sqlite3.connect("instance/resturants.db")
cur=conn.cursor()
load_more=driver.find_element(By.CLASS_NAME,value="CHn7Qb")
load_more.click()
time.sleep(5)


resturant_ratings=driver.find_elements(By.CLASS_NAME,value="yi40Hd")
ratings=[resturant_rating.text for resturant_rating in resturant_ratings if resturant_rating.text !=""]
resturant_reviews=driver.find_elements(By.CLASS_NAME,value="RDApEe")
reviews=[resturant_review.text for resturant_review in resturant_reviews]
resturants=driver.find_elements(By.CLASS_NAME,value="uMdZh")


#Loop to get the info of the cafes
for resturant,review,rating in zip(resturants,reviews,ratings):
    
    resturant.click()
    time.sleep(5)
    
    resturant_address=driver.find_element(By.CLASS_NAME,value="LrzXr")
    ad=f"{mapbase_url}{resturant_address.text.replace(" ","+")}"
    addresses.append(resturant_address.text)
    resturant_name=driver.find_element(By.CLASS_NAME,value="qrShPb")
    nm=resturant_name.text
    names.append(resturant_name.text)
    try:
        resturant_phone=driver.find_element(By.CSS_SELECTOR,value="span.LrzXr.zdqRlf.kno-fv")
        ph=resturant_phone.text
        phones.append(resturant_phone.text)
    except:
        ph="null"
    
    try:
        resturant_price=driver.find_element(By.CSS_SELECTOR,value="span.YhemCb")
        pr=resturant_price.text
        prices.append(resturant_price.text)
    except:
        pr="null"
    
    resturant_type=driver.find_element(By.CSS_SELECTOR,value="span.YhemCb+span")
    tp=resturant_type.text
    types.append(resturant_type.text)
    
    #Add the scrape data into database
    cur.execute('''
        INSERT INTO restaurants (name,type,address,ratings,reviews,price_range,phone_number)
        VALUES (?,?, ?, ?, ?,?,?)
    ''', (nm,tp, ad,rating,review, pr,ph))

conn.commit()
conn.close()

driver.quit()