# Beautifulsoup
from bs4 import BeautifulSoup

with open("html_doc.html","r")as f:
    readDoc=f.read()
    
soup=BeautifulSoup(readDoc,"html.parser")
print(soup.prettify())  # This will organize it in a well manner

print(soup.title.string)   # Give title 

print(soup.find_all("a")) # FInding all the a

#                                       finding url
for link in soup.find_all('a'):
    print(link.get('href'))
# finding all the text
print(soup.get_text())


# for child in soup.find(class_="container").children:
#     print(child) 

# for parent in soup.find(class_="box").parents:
#     print(parent)

#                                         Modifying

# count=soup.find(class_="container")
# count.name="span"     #replace div with span
# count["class"]="myclass"      # repalce container with myclass
# count.string="I am a string"   # modify the content
# print(count)

#                                       Inserting new tags



# ulTag=soup.new_tag("ul")

# liTag=soup.new_tag("li")  
# liTag.string="Home"
# ulTag.append(liTag)

# soup.html.body.insert(0,ulTag)
# with open("New_doc.html","w")as f:
#     f.write(str(soup))


#                                       Finding Attribute

# cnt=soup.find(class_="container")
# print(cnt.has_attr("class"))  # print status code

def has_class_but_not_id(tag):
    return tag.has_attr("class") and not tag.has_attr("id")

result=soup.find_all(has_class_but_not_id)
print(result)



# Note: Websites usually do not give access/permission to scrap their Data.These types of modules requires proxy to scrap Data.

#   visit this ----->>   https://www.crummy.com/software/BeautifulSoup/bs4/doc/