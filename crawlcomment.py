import selenium
from selenium import webdriver
from time import sleep
import random
import pandas as pd
import pymongo

# 1. Déclaration browser
browser = webdriver.Chrome(executable_path="./chromedriver.exe")

# 2. Ouvert URL de post
browser.get("https://www.facebook.com/radio6officiel/photos/a.154020847949649/2757871987564509/?type=3")
sleep(5)

# 3. Obtenez le lien montrant le commentaire
showcomment_link = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div[1]/div[2]")
showcomment_link.click()

sleep(random.randint(2,5))

try:
    showcomment_link.click()
except selenium.common.exceptions.StaleElementReferenceException:
    pass
sleep(3)

# 4. Trouvez tous les commentaires
comment_list = browser.find_elements_by_xpath("//div[@role='article']")

content = browser.find_elements_by_xpath("//div[@dir='auto']")

images = browser.find_elements_by_tag_name("img")

users = []
contents = []
urls =[]
for idx, (user, cont) in enumerate(zip(comment_list, content)):
    users.append(user.find_element_by_class_name("pq6dq46d").text)
    contents.append(cont.text)
    # print("{}, {} : {}".format(idx, user.find_element_by_class_name("pq6dq46d").text, cont.text))
    # print("{}, {}, {}, {}".format(idx, user.find_element_by_class_name("pq6dq46d").text, cont.text, img.get_attribute("src")))


for idx,(img) in enumerate(images):
    url= img.get_attribute("src")
    urls.append(url)
    #print("{}:{}".format(idx,urls[idx]))


#Enregistrer des données sur ordinateur
d = {'User':users, 'Comment': contents}
df = pd.DataFrame(data=d)
# print(df)
# df.to_csv('D:/MongoDB/Data/crawlcomment.csv',index=False)
# pd.read_csv('D:/MongoDB/Data/crawlcomment.csv')

#Enregistrer des données sur MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['mydatabase']
mydoc = mydb["crawlcomment"]

data = {'Users': 'Comments'}
for user, content in zip(users, contents):
    data[user]=content

mydoc.insert_one(data)
# mydoc.insert_many(df)

print('done')
