from bs4 import BeautifulSoup
import requests
import re
from PIL import Image
import io
from urllib.parse import urljoin

# Fetch the main page containing press releases
req = requests.get("https://pib.gov.in/allRel.aspx")
if req.status_code == 200:
    soup = BeautifulSoup(req.content, 'html.parser')
    links_dict = {}

    # Find the content area containing links
    content_div = soup.find('div', class_='content-area')
    links = content_div.find_all('a') if content_div else []

    # Extract title and href of relevant links
    for link in links:
        title = link.get('title')
        href = link.get('href')
        if href and '/PressReleasePage.aspx?PRID=' in href:
            href = urljoin("https://pib.gov.in", href)
            links_dict[title] = href

    # Print the dictionary
    for title, href in links_dict.items():
        print(f"Title: {title}, Href: {href}")

    # Fetch details of a specific press release page
    req_inner = requests.get("https://pib.gov.in/PressReleasePage.aspx?PRID=1986741")
    if req_inner.status_code == 200:
        inner_soup = BeautifulSoup(req_inner.content, 'html.parser')
        target_div = inner_soup.find('div', class_='innner-page-main-about-us-content-right-part')

        if target_div:
            # Clean up unwanted elements within the target div
            for unwanted in target_div.find_all(['span', 'div'], {'id': ['ReleaseId', 'lblViews'], 'class': ['ReleaseLang']}):
                unwanted.extract()

            # Extract and clean text content
            all_data = target_div.get_text()
            cleaned_text = re.sub(r'\s+', ' ', all_data).strip()
            print("Extracted Text:", cleaned_text)

            # Process and download images
            img_tags = target_div.find_all('img')
            if img_tags:
                for i, img_tag in enumerate(img_tags, 1):
                    img_url = urljoin("https://pib.gov.in", img_tag.get('src'))
                    print("Image URL:", img_url)

                    # Download and save the image in a lossless format (PNG)
                    img_data = requests.get(img_url).content
                    img = Image.open(io.BytesIO(img_data))
                    filename = f'downloaded_image_{i}.png'
                    img.save(filename, format='PNG')
                    print(f"Image saved as {filename}")
        else:
            print("Target div not found.")
    else:
        print("Error fetching inner page:", req_inner.status_code)
else:
    print("Error fetching main page:", req.status_code)
