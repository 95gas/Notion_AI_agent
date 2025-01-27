# Notion_AI_agent
 An AI agent for generating summaries and topic tags for a Notion database

# Installation
- Install python (3.9 preferrable)
- Install packages:
  ```
  pip install -r requirements.txt
  ```

# Run
1. add the foled 'env' in the roort containing a file named 'keys.env' with the following env variables:
   ```
   NOTION_INTEGRATION_TOKEN
   DATABASE_ID
   OPENAI_API_KEY
   OPENAI_MODEL_NAME_CHAT
   ```
3. Run it:
   ```
   python main.py
   ```

# Support
For adding more supported features, [this](https://developers.notion.com/reference/page) is how a notion page appears in json once fetched.
