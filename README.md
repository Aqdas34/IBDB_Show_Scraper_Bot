# IBDB Show Scraper Bot  

## Overview  
This Python bot scrapes show data from **[IBDB (Internet Broadway Database)](https://www.ibdb.com/shows)**. It filters shows based on a user-provided **year range** and extracts key details such as:  
- **Show Name**  
- **First Preview Date**  
- **Type of Show** (e.g., Musical, Play, etc.)  
- **Show Statistics**  

## How It Works  

1. **Running the Bot**  
   - When executed, the bot automatically scrapes show data from IBDB.  

2. **Filtering by Year Range**  
   - Users provide a **start year** and an **end year**.  
   - The bot filters the shows that fall within this range.  

3. **Data Extraction**  
   - The bot fetches and extracts the following details for each show:  
     - **Show Name**  
     - **First Preview Date**  
     - **Type of Show** (Musical, Play, etc.)  
     - **Statistics** (e.g., total performances, reviews, etc.)  

4. **Output & Storage**  
   - The extracted data is **stored in a structured format** (EXCEL).  

## Features  
✅ **Automated Scraping** – No manual browsing required.  
✅ **Year-Based Filtering** – Fetches only relevant shows within the given range.  
✅ **Detailed Show Information** – Captures name, preview date, type, and stats.  
✅ **Exportable Data** – Saves results in a structured format for further analysis.  

## Additional Notes  
- Ensure you have **a stable internet connection** while running the bot.  
- Make sure all required Python dependencies (e.g., `requests`, etc.) are installed.  
