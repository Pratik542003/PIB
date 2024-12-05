
from bs4 import BeautifulSoup
import requests

base_url = "https://pib.gov.in/allRel.aspx"
chosen_date = "13"  # Change this to the desired day

# Make a request to get the initial page
req = requests.get(base_url)

# Parse the HTML content
if req.status_code == 200:
    soup = BeautifulSoup(req.content, 'html.parser')

    # Find the dropdown/select element with date options
    select_element = soup.find('select', {'id': 'ContentPlaceHolder1_ddlday'})

    # Check if the select element is found
    if select_element:
        # Extract the options and their values
        date_options = {option['value']: option.text for option in select_element.find_all('option')}

        # Make sure the chosen_date is a valid option
        if chosen_date in date_options:
            # Make a request with the selected date
            params = {'ctl00$ContentPlaceHolder1$ddlday': chosen_date}
            req_date = requests.post(base_url, data=params)

            if req_date.status_code == 200:
                soup_date = BeautifulSoup(req_date.content, 'html.parser')

                links_dict = {}

                content_div = soup_date.find('div', class_='content-area')

                links = content_div.find_all('a')

                for link in links:
                    title = link.get('title')
                    href = link.get('href')

                    if href and '/PressReleasePage.aspx?PRID=' in href:
                        href = "https://pib.gov.in" + href
                        links_dict[title] = href

                # Now links_dict contains the links for the specified date
                print(links_dict)
            else:
                print(f"Error {req_date.status_code} while fetching content for the specified date.")
        else:
            print(f"Chosen date {chosen_date} is not a valid option.")
    else:
        print("Dropdown/select element not found.")
else:
    print(f"Error {req.status_code}")


