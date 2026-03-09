---
name: extracting-google-maps-leads
description: Extracts business leads and contact information from Google Maps using the Apify compass/crawler-google-places Actor. Use when the user wants to scrape local businesses, find emails, or gather phone numbers for specific niches in specific locations.
---

# Extracting Google Maps Leads

## When to use this skill
- The user asks to scrape Google Maps for a specific niche and location (e.g., "Find all landscapers in Downers Grove").
- The user requests lead generation or contact list building for local businesses.

## Workflow

- [ ] **Configure Search:** Identify the search terms and location from the user request.
- [ ] **Test Run (Optional):** Run a small sample (e.g., 10 places) to present data quality and a cost estimate to the user before scaling up.
- [ ] **Execute Full Extraction:** Run the Apify `compass/crawler-google-places` Actor with `scrapeContacts: true` and expanded limits.
- [ ] **Retrieve Dataset:** Fetch the final dataset using the Apify dataset ID.
- [ ] **Format Data:** Convert the JSON output into a clean CSV using the provided helper script.
- [ ] **Present Results:** Highlight the top leads in a formatted markdown table in the chat.

## Instructions

1. **Test Run:**
   - Call the `default_api:mcp_apify_call-actor` tool with `actor: "compass/crawler-google-places"`.
   - Set `input` parameters: 
     - `searchStringsArray`: `["your niche"]`
     - `locationQuery`: `"City, State"`
     - `maxCrawledPlacesPerSearch`: `10`
     - `scrapeContacts`: `true`
     - `skipClosedPlaces`: `true`

2. **Full Extraction:**
   - Once the user approves the test run and budget, expand `maxCrawledPlacesPerSearch` to capture all available places (e.g., `150` or remove the limit if appropriate).
   - Run the Actor again and retrieve the `datasetId` from the successful output.
   - Use `default_api:mcp_apify_get-actor-output` to retrieve the data (recommended fields: `title,phone,website,emails,totalScore,reviewsCount`).

3. **Data Formatting:**
   - Save the raw JSON array to a temporary file.
   - Use the Python script in `scripts/convert_json_to_csv.py` to parse the dataset output and save it as a `.csv` file in the user's workspace.
   - Run the script: `python .agent/skills/extracting-google-maps-leads/scripts/convert_json_to_csv.py <input.json> <output.csv>`

4. **Presentation:**
   - Always present a top-tier Markdown table in the chat with the 5 best leads sorted by data quality (prioritize leads that have an explicit email address and high ratings/reviews).
   - Include a cost breakdown for the Apify run.

## Resources
- `scripts/convert_json_to_csv.py`
