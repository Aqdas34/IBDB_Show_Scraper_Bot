from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from openpyxl import Workbook
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
# Initialize the WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 20)  # Explicit wait instance
driver.set_page_load_timeout(60)  # Increase page load timeout to 60 seconds
driver.set_script_timeout(60)  


def extract_a_i_data(driver, parent_div_id):
    # Locate the parent div by its id (id="venues")
    parent_div = driver.find_element(By.ID, parent_div_id)

    # Find all the 'a' and 'i' tags within the parent div (inside all child divs)
    a_tags = parent_div.find_elements(By.TAG_NAME, 'a')
    i_tags = parent_div.find_elements(By.TAG_NAME, 'i')
    i_tags = [i for i in i_tags if "Current" not in i.text]

    data = []

    # Regex to extract year from the date string
    year_regex = r"\b(\d{4})\b"  # Matches any 4-digit year
    current_year = datetime.now().year

    # Iterate through all 'a' and 'i' tags to extract the needed information
    for a, i in zip(a_tags, i_tags):
        # Extract the text from the 'a' tag (the name of the theatre or link)
        a_text = a.text.strip()

        # Extract the text from the 'i' tag (the date range or other information)
        i_text = i.text.strip()

        # Extract the years from the 'i' tag text (start and end year)
        years = re.findall(year_regex, i_text)

        # Store only the start year and end year if available
        if len(years) >= 2:
            start_year = years[0]
            end_year = years[1]
        elif len(years) == 1:
            start_year = years[0]
            end_year = "current year"
        else:
            start_year = "Unknown"
            end_year = "Unknown"

        # Append the extracted data as a dictionary to the list
        data.append({'theatre_name': a_text, 'start_year': start_year, 'end_year': end_year})

    return data


global_opening_month = "05"
global_opening_day = "29"
global_opening_year = "1989"

global_closing_month = "06"
global_closing_day = "03"
global_closing_year = "1990"



def adjust_main_list_to_columns(main_list, columns):
    # Ensure each sublist matches the number of columns
    num_columns = len(columns)
    adjusted_list = []
    
    for sublist in main_list:
        if len(sublist) < num_columns:
            # Add placeholder values if the sublist is too short
            sublist += ["-"] * (num_columns - len(sublist))
        elif len(sublist) > num_columns:
            # Truncate if the sublist is too long
            sublist = sublist[:num_columns]
        adjusted_list.append(sublist)
    
    return adjusted_list


def go_to_seasons():
    global global_opening_year
    global global_closing_year
    global global_opening_day
    global global_opening_month
    global global_closing_day
    global global_closing_month

    driver.get("https://www.ibdb.com/shows")
    dropdown_input = driver.find_element(By.CSS_SELECTOR,'input.select-dropdown')
    dropdown_input.click()
    dropdown_options = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.select-dropdown'))
        )
    nyc_production_option = dropdown_options.find_element(By.XPATH, "//li/span[contains(text(), 'NYC Productions')]")
    nyc_production_option.click()
    hidden_div = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/form/ul/li/div[2]')
    driver.execute_script("arguments[0].style.display = 'block';", hidden_div)
    input_field = driver.find_element(By.XPATH, '//*[@id="search-extra-options"]/li/div[2]/div[12]/div[1]/input[1]')
    input_field.send_keys(global_opening_month)
    input_field = driver.find_element(By.XPATH,'//*[@id="search-extra-options"]/li/div[2]/div[12]/div[1]/input[2]');
    input_field.send_keys(global_opening_day)
    input_field = driver.find_element(By.XPATH,'//*[@id="search-extra-options"]/li/div[2]/div[12]/div[1]/input[3]');
    input_field.send_keys(global_opening_year)
    input_field = driver.find_element(By.XPATH,'//*[@id="search-extra-options"]/li/div[2]/div[12]/div[2]/input[1]')
    input_field.send_keys(global_closing_month)
    input_field = driver.find_element(By.XPATH,'//*[@id="search-extra-options"]/li/div[2]/div[12]/div[2]/input[2]');
    input_field.send_keys(global_closing_day)
    input_field = driver.find_element(By.XPATH,'//*[@id="search-extra-options"]/li/div[2]/div[12]/div[2]/input[3]');
    input_field.send_keys(global_closing_year)



def find_max(main_list):
    max_n = 0
    for i in main_list:
        if len(i) > max_n:
            max_n = len(i)
    return max_n



def split_date(date_str):
    try:
        # Parse the date string
        parsed_date = datetime.strptime(date_str, "%b %d, %Y")
        # Extract year, month, and day
        return parsed_date.year, parsed_date.month, parsed_date.day
    except ValueError:
        return "-", "-", "-"

  # Increase script execution timeout to 60 seconds

# Function to extract links based on XPath
def extract_links(xpath):
    """Extract all links from the specified parent element."""
    try:
        parent_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        links = parent_element.find_elements(By.TAG_NAME, "a")
        return [link.get_attribute("href") for link in links if link.get_attribute("href")]
    except Exception as e:
        print(f"Error extracting links: {e}")
        return []



def assign_value(tag_list: list, value):
    for i in tag_list:
        if i == value:
            tag_list.remove(i)  # Remove the value from the list
            return i  # Return the value
    return "-"  # Return None if the value is not found



columns = [
        "Season", "Show title", "Opening Year", "Opening Month", "Opening Day",
        "Closing Year", "Closing Month", "Closing Day", "First preview year",
        "First preview Month", "First preview Day", "Total previews",
        "Total performances", "Play/Musical/Special", "Genre",
        "Original/Revival", "Theatre", "Week ending year", "Week ending month",
        "Week ending day", "Gross", "Attendance", "%Capacity", "#Previews", "#Perf."
    ]



def scroll_up(driver, amount=None):
    """
    Scrolls up the webpage using Selenium.
    
    Parameters:
        driver: The Selenium WebDriver instance.
        amount: The number of pixels to scroll up. If None, scrolls to the top of the page.
    """
    if amount is None:
        # Scroll to the top of the page
        driver.execute_script("window.scrollTo(0, 0);")
    else:
        # Scroll up by the specified amount
        driver.execute_script(f"window.scrollBy(0, -{amount});")

# Function to fetch show information from a link
def fetch_show_information(link, main_list, max_i_values_length):
    try:
        # link = "https://www.ibdb.com/broadway-production/charlie-and-the-chocolate-factory-509567"
        # link = "https://www.ibdb.com/broadway-production/celebrity-autobiography-520492"
        driver.get(link)
        time.sleep(1)
        driver.get(f"{link}#Statistics")
        # time.sleep(2)


        global global_opening_year
        global global_closing_year
        global global_opening_day
        global global_opening_month
        global global_closing_day
        global global_closing_month

        
        # options_to_check = ['2022-23', '2023-24', '2024-25']
        options_to_check = [
    f"{global_closing_year.zfill(4)}-{str(int(global_closing_year) + 1)[2:].zfill(2)}",
    f"{global_opening_year.zfill(4)}-{global_closing_year[2:].zfill(2)}",
    f"{str(int(global_opening_year) - 1).zfill(4)}-{global_opening_year[2:].zfill(2)}"
]

        print(options_to_check)
        extracted_data = extract_a_i_data(driver, 'venues')

        # Try to find and click the first available option
        # option_selected = False
        # for option in options_to_check:
        #     # Find dropdown options based on the option text
        #     dropdown_options = driver.find_elements(By.XPATH, f'//li[span[text()="{option}"]]')
            
        #     # If the option is found, click it and break the loop
        #     if dropdown_options:
        #         dropdown_options[0].click()
        #         option_selected = True
        #         print(f'Selected: {option}')
        #         break

        # # If no option was selected, handle the case
        # if not option_selected:
        #     print('None of the options were available.')
                # Wait and extract show details
        

        try:
            opening_date = wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]"))
            ).text
        except NoSuchElementException:
            opening_date = "-"

        try:
            closing_date = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]").text
        except NoSuchElementException:
            closing_date = "-"

        try:
            first_preview = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]").text
        except NoSuchElementException:
            first_preview = "-"

        try:
            title = driver.find_element(By.CLASS_NAME, "title-label").text
        except NoSuchElementException:
            title = "-"



        try:
            tot_preview = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[2]/div[3]/div[1]/div[2]").text
        except NoSuchElementException:
            tot_preview = "-"

        try:
            perf = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[2]").text
        except NoSuchElementException:
            perf = "-"


              
        # hidden_tags = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[3]/div[1]') 
        
        # hidden_tags = driver.find_element(By.XPATH, '//*[contains(@class, "col") and contains(@class, "s12") and contains(@class, "txt-paddings") and contains(@class, "tag-block-compact")]')
        # Fetch all <i> elements within the parent element


        play_music = "-"
        genre = "-"
        original_revival = "-"
        theatre=None

        
        hidden_tags = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[3]/div[1]')
        i_elements = hidden_tags.find_elements(By.TAG_NAME, 'i')

        i_values = sorted([element.text for element in i_elements])
        play_music = assign_value(i_values,'Play')
        if play_music == '-':
            play_music = assign_value(i_values,'Musical')
        # play_music = assign_value(i_values,'Play')
        if play_music == '-':
            play_music = assign_value(i_values,'Special')
        
        genre = assign_value(i_values,'Drama')

        original_revival = assign_value(i_values,'Original')
        if original_revival == '-':
            original_revival = assign_value(i_values,'Revival')

        
        try:
            if len(extracted_data) == 1:
                theatre = driver.find_element(By.XPATH, '//*[@id="venues"]/div/div[2]/a').text
            else:
                for theatre_option in extracted_data:
                    if int(global_opening_year) >= int(theatre_option['start_year']):
                        theatre = theatre_option['theatre_name']
            # theatre = driver.find_element(By.XPATH, '//*[@id="venues"]/div/div[2]/a').text
        except NoSuchElementException:
            theatre = "-"

        # Process dates
        opening_year, opening_month, opening_day = split_date(opening_date)
        closing_year, closing_month, closing_day = split_date(closing_date) if closing_date != "-" else ("-", "-", "-")
        preview_year, preview_month, preview_day = split_date(first_preview) if first_preview != "-" else ("-", "-", "-")


        # Wait for and retrieve season info
        # season = dropdown_input.get_attribute("value")
        dropdown_input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Statistics"]/div/div[1]/div[1]/div/div[2]/div/input'))
        )
        season= f"{global_opening_year}-{global_closing_year[2:]}"
        print(season)

        print(f"options_to_check = {options_to_check}")


        option_selected = False
        dropdown_clicked = False  # Flag to track if the dropdown has been clicked
        scroll_up(driver)
        time.sleep(2)
        for option in options_to_check:
            # Open the dropdown only on the first iteration or when needed
            if not dropdown_clicked:
                dropdown_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.select-dropdown'))
                )
                dropdown_input.click()
                time.sleep(1)
                dropdown_clicked = True  # Set flag to avoid repeated clicks

            print(f'\n option = {option}')

            # Find dropdown options based on the option text
            dropdown_options = driver.find_elements(By.XPATH, f'//li[span[text()="{option}"]]')
            
            # If the option is found, click it and break the loop
            if dropdown_options:
                dropdown_options[0].click()
                option_selected = True
                dropdown_clicked = False  # Reset flag to reopen dropdown if needed
                print(f'Selected: {option}')
                
                # Wait for the table to load
                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="Statistics"]/div/div[2]'))
                )
                rows = table.find_elements(By.TAG_NAME, "tr")

                # Parse rows into structured data
                data = []
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = [cell.text for cell in cells]
                    if row_data:
                        date_str = row_data[0]
                        row_data = row_data[1:]
                        year, month, day = split_date(date_str)
                        if year and month and day:
                            row_data.insert(0, day)
                            row_data.insert(0, month)
                            row_data.insert(0, year)
                        if year == int(global_opening_year) or year == int(global_closing_year):
                            data.append(row_data)
                data = [[item for item in sublist if item != ''] for sublist in data]
                show_data = [[season, title, opening_year, opening_month, opening_day, closing_year, closing_month,
                            closing_day, preview_year, preview_month, preview_day, tot_preview, perf,play_music,genre,original_revival,  theatre] + row for row in data]
                for s in show_data:
                    main_list.append(s)
                i_values = sorted(i_values)
            
                for row in show_data:
                    row.extend(i_values)

            else:
                option_selected = False
                print(f'Option "{option}" not found. Skipping...')

                    

        # If no option was selected, handle the case
        if not option_selected:
            print('None of the options were available.')





        max_i_values_length = max(max_i_values_length, len(i_values))


        # print(f"data = {data}")

        # Combine static and dynamic data
        
        




        # print(show_data)
        return show_data,max_i_values_length
    except Exception as e:
        print(f"Error fetching information from {link}: {e}")
        csv_file = "error_logs_double.csv"
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
    # Write a row with the link and error message
            writer.writerow([link, e])
        return [],max_i_values_length

try:

    go_to_seasons()
    time.sleep(7)


    div = driver.find_element(By.ID, 'productions')
    links = div.find_elements(By.TAG_NAME, 'a')

    hrefs = [link.get_attribute('href') for link in links]
    print(len(hrefs))


    max_i_values_length = 0
    # fetch_show_information("https://www.ibdb.com/broadway-production/back-to-the-future-the-musical-535440",[],max_i_values_length)
    main_list = []
    count = 1
    for link in hrefs:
        print(count)
        count += 1
        _,max_i_values_length = fetch_show_information(link, main_list,max_i_values_length)
  

    # fetch_show_information("https://www.ibdb.com/broadway-production/buttons-on-broadway-4301",main_list)

    columns.extend([f"Comment{i+1}" for i in range(max_i_values_length)])

    # Adjust the main list to match the number of column
    main_list =  adjust_main_list_to_columns(main_list, columns)
    # # Create a DataFrame and save to Excel
    df = pd.DataFrame(main_list, columns=columns)
    df.to_excel("double.xlsx", index=False)
    print("Data saved to double.xlsx")

finally:
    # Quit the driver
    driver.quit()