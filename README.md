# Notion_AI_agent
 An AI agent for generating summaries and topic tags for a Notion database

# Installation
- Install python (3.9 preferrable)
- Install packages:
  ```
  pip install -r requirements.txt
  ```

# Good to know
The following scripts has beed designed for a dataset as shown below. In my case I used it in the scenario of personal growth text. In the examples below the fields 'AI summary' and 'Topics' have been generated and inserted using the agent developed in this repo.
![image](https://github.com/user-attachments/assets/c993b2a4-8eab-4eca-9569-b164b8f40260)

For generalizing it to your project, just replaces the name of the dictionary keys in the [code](https://github.com/95gas/Notion_AI_agent/blob/main/src/classes/NotionAIAgent.py).


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

# Libs used
- Llama index for the management of the openai llm
- [Notion2md](https://github.com/echo724/notion2md) for extracting an html version of the page

# Support
For adding more supported features, [this](https://developers.notion.com/reference/page) is how a notion page appears in json once fetched.
