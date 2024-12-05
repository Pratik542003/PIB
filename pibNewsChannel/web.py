from bs4 import BeautifulSoup
import requests
import re
from PIL import Image
import io
from urllib.parse import urljoin
# req = requests.get("https://pib.gov.in/allRel.aspx")
def getAllurls():
    req = requests.get("https://pib.gov.in/allRel.aspx")
    # Parse the HTML content
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        links_dict = {}

        content_div = soup.find('div', class_='content-area')

        links = content_div.find_all('a')

        for link in links:
            title = link.get('title')
            href = link.get('href')
            # print(f"Title: {title}, Href: {href}")

            if href and '/PressReleasePage.aspx?PRID=' in href:

                href = "https://pib.gov.in" + href
                links_dict[title] = href
        return links_dict
    else:
        print("Error 404")
        return -1
# Print the dictionary
# for title, href in links_dict.items():
#     print(f"Title: {title}, Href: {href}")

def getText(link):
    # print(links_dict["PM to interact with beneficiaries of Viksit Bharat Sankalp Yatra on 16th December"])

    # req_inner = requests.get(links_dict["PM to interact with beneficiaries of Viksit Bharat Sankalp Yatra on 16th December"])
    req_inner = requests.get(link)
    if req_inner.status_code == 200:
        soup = BeautifulSoup(req_inner.content , 'html.parser')
    
        print(soup.prettify())
        target_div = soup.find('div', class_='innner-page-main-about-us-content-right-part')
        img_tags = target_div.find_all('img')
        if target_div:
            for unwanted_span in target_div.find_all('span', {'id': 'ReleaseId'}):
                unwanted_span.extract()
            for unwanted_span in target_div.find_all('span', {'id': 'lblViews'}):
                unwanted_span.extract()

            for unwanted_div in target_div.find_all('div', class_='ReleaseLang'):
                unwanted_div.extract()
            all_data = target_div.get_text()
            print("Length-" , len(all_data))

            cleaned_text = re.sub(r'\s+', ' ', all_data).strip()
            print(cleaned_text)
            return cleaned_text
        else:
            print(target_div)
            print("Div not found.")
        
        # if img_tags:
        #     for i, img_tag in enumerate(img_tags, 1):
        #         # Get the source (src) attribute of the image
        #         img_url = img_tag.get('src')

        #         print("Image URL:", img_url)

        #         # Now you can use requests to download the image if needed
        #         img_data = requests.get(img_url).content

        #         # Open the image using PIL
        #         img = Image.open(io.BytesIO(img_data))

        #         # Save the image in a lossless format (PNG)
        #         filename = f'downloaded_image_{i}.png'
        #         img.save(filename, format='PNG')
        #         print(f"Image saved as {filename}")
        
    else:
        print("Error 404")
        return None

