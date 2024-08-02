import requests
from bs4 import BeautifulSoup
import os


combined_list_poem = []

def urlshaertolistsher(url):
    listurls , poet_name = getsuburls(url)
    listurlpagetoListBeyt(listurls)
    savepoem(poet_name ,combined_list_poem)
    print(f"File '{poet_name}.txt' saved successfully.")
    return combined_list_poem



def savepoem(poet_name ,combined_list_poem):
    with open(f"database/{poet_name}.txt", "w", encoding="utf-8") as file:
        for poem in combined_list_poem:
            file.write(poem + "\n")



def get_part_title_block_urls(base_url):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    headers = soup.find_all("div", {"class": "part-title-block"})
    res = []
    for header in headers:
        href = header.find("a")["href"]
        if href != '#index':
            res.append("https://ganjoor.net" + href)
    return res


def getsuburls(url):
    poet_name = url.split('/')[3]
    initial_page_urls = get_part_title_block_urls(url)
    listurls = initial_page_urls
    for page_url in initial_page_urls:
        additional_urls = get_part_title_block_urls(page_url)
        if additional_urls:
            listurls.extend(additional_urls)
    # Deduplicate URLs

    listurls = list(set(listurls))
    return listurls , poet_name 





def listurlpagetoListBeyt(listurls):
    for i in listurls:
     print((i))
    for new_url in listurls:
        number = 1
        while True:
            combined_list_poem.append("<[SOT]>")
            new_url_with_sh = f"{new_url}/sh{number}"
            response = requests.get(new_url_with_sh)
            if response.status_code == 404:
                break
            # listurls.append(new_url_with_sh)
            print(f"{new_url_with_sh} is passed")
            number += 1
            page = response.text
            soup = BeautifulSoup(page, "html.parser")

            # Find all relevant divs in the order they appear
            all_divs = soup.find_all("div", {"class": ["m1", "m2", "n","b2"]})
            # Initialize the combined list

            # Extract and clean the text based on the class
            for div in all_divs:
                if "m1" in div["class"]:
                    combined_list_poem.append("<[SOFM]>")
                    combined_list_poem.append(div.text.replace("\u200c", ""))
                    combined_list_poem.append("<[EOFM]>")

                elif "m2" in div["class"]:
                    combined_list_poem.append("<[SOSM]>")
                    combined_list_poem.append(div.text.replace("\u200c", ""))
                    combined_list_poem.append("<[EOSM]>")

                elif "b2" in div["class"]:
                    # Process each <p> tag in the "b2" div
                    for i, p in enumerate(div.find_all("p")):
                        if i == 0:
                            combined_list_poem.append("<[SOFMMBT]>")
                        elif i == 1:
                            combined_list_poem.append("<[SOSMMBT]>")

                        combined_list_poem.append(p.text.replace("\u200c", ""))
                        
                        if i == 0:
                            combined_list_poem.append("<[EOFMMBT]>")
                        elif i == 1:
                            combined_list_poem.append("<[EOSMMBT]>")





                elif "n" in div["class"]:
                    combined_list_poem.append("<[SON]>")
                    combined_list_poem.append(div.text.replace("\u200c", ""))
                    combined_list_poem.append("<[EON]>")

            combined_list_poem.append("<[EOT]>")


#End of text <[EOT]>
#End of Nasr <[EON]>
#End of End of first mesra middle beyt <[EOFMMBT]>
#End of End of Seccondmesra middle beyt <[EOSMMBT]>
#End of Seccond mesra <[EOSM]>
#End of First mesra <[EOFM]>
#End of text <[EOT]>
#End of text <[EOT]>





def get_poet_urls(base_url):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    headers = soup.find_all("div", {"class": "poet"})
    res = []
    for header in headers:
        href = header.find("a")["href"]
        if href != '#index':
            res.append("https://ganjoor.net" + href)
    return res

def poet_exists_in_database(poet_name, database_folder='database'):
    file_name = f"{poet_name}.txt"
    return os.path.exists(os.path.join(database_folder, file_name))

def filter_poet_urls(poet_urls, database_folder='database'):
    filtered_urls = []
    for url in poet_urls:
        poet_name = get_poet_name_from_url(url)
        if not poet_exists_in_database(poet_name, database_folder):
            filtered_urls.append(url)
    return filtered_urls


def get_poet_name_from_url(poet_url):
    # Extract the poet's name from the URL (assuming it is the last part of the URL path)
    return poet_url.rstrip('/').split('/')[-1]





base_url = "https://ganjoor.net"
poet_urls = get_poet_urls(base_url)
filtered_poet_urls = filter_poet_urls(poet_urls)
print(len(poet_urls),len(filtered_poet_urls))

for poet_url in filtered_poet_urls:
    combined_list = urlshaertolistsher(poet_url)
