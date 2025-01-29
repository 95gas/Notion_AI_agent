import requests, json
import logging
from notion2md.exporter.block import StringExporter
from llama_index.core.settings import Settings
from src.Prompts import DEFAULT_SUMMARY_TEMPLATE, DEFAULT_TAGGING_TEMPLATE
import os

# Reference api: https://thienqc.notion.site/Notion-API-Python-ca0fd21bc224492b8daaf37eb06289e8
class NotionAIAgent:
    def __init__(self, llm):
        """
        Initialize the notion AI agent
        :param llm: the llm to use
        :type llm: Any type of LLM supported by llama index
        """
        self.token = os.getenv("NOTION_INTEGRATION_TOKEN")
        self.headers  = {
                    "Authorization": "Bearer " + os.getenv("NOTION_INTEGRATION_TOKEN"),
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                    }
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger("NotionAIAgent")

        Settings.llm = llm
        self._llm = Settings.llm

    def update_page(self, page_id:str, update_data:dict[str, any])->None:
        """
        Update the page with the update_data
        :param page_id: the id of the page to update
        :type page_id: str
        :param update_data: the dictionary containing the updated data
        :type update_data: dict[str, any]
        """
        self.logger.info("Updating page")
        update_url = f"https://api.notion.com/v1/pages/{page_id}"
        data = json.dumps(update_data)
        response = requests.request("PATCH", update_url, headers=self.headers, data=data)
        if response.status_code != 200:
            self.logger.error(f"Error in updating page {page_id}:" + response.text)
        else:
            self.logger.info("Page updated successfully")

    def read_database(self, database_id:str)-> dict[str, any]:
        """
        Read the database and return the data
        :param database_id: the id of the database to read
        :type database_id: str
        :return: The dictionary containing the data
        :rtype: dict[str, any]
        """
        self.logger.info("Fetching database")
        read_url = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.request("POST", read_url, headers=self.headers)
        data = response.json()
        if response.status_code != 200:
            self.logger.error(f"Error in reading database {database_id}: " + response.text)
        else:
            self.logger.info("Database fetched successfully")
        return data

    def get_mk_page(self, page_id:str)->str:
        """
        Get and return the markdown page for the given page_id
        :param page_id: the page_id of the page to get
        :type page_id: page_id
        :return: the markdown page
        :rtype: str
        """
        # StringExporter will return output as String type
        return StringExporter(block_id=page_id,
                              token=self.token).export()

    def get_text_page(self, page_id:str)->dict[str,any]:
        """
        Get and return the text content for the given page_id
        :param page_id: the page_id of the page to get
        :type page_id: str
        :return: the data in json format
        :rtype: dict[str,any]
        """
        self.logger.info("Fetching text page")
        read_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        response = requests.request("GET", read_url, headers=self.headers)
        data = response.json()
        if response.status_code != 200:
            self.logger.error("Error in fetching text page: " + response.text)
        else:
            self.logger.info("Text page fetched successfully")
        return data

    def get_summary(self, text: str)->str:
        """
        Get and return the summary for the given text
        :param text: the text to get the summary for
        :type text: str
        :return: the summary of the text
        :rtype: str
        """
        summary = str(self._llm.complete(prompt=DEFAULT_SUMMARY_TEMPLATE.format(text=text)))
        return summary.strip()

    def get_tags(self, text: str)->list[str]:
        """
        Get and return the topic tags for the given text
        :param text: the text to get the tags for
        :type text: str
        :return: the list of topic tags
        :rtype: list[str]
        """
        raw_resp = self._llm.complete(prompt=DEFAULT_TAGGING_TEMPLATE.format(text=text), response_format={"type": "json_object"})
        formatted_ans = json.loads(str(raw_resp))
        return formatted_ans["tags_list"]

    def add_summary(self, database_id:str)->None:
        """
        Add the summary for the given database to each pages in it
        :param database_id: the id of the database
        :type database_id: str
        :return: None
        :rtype: None
        """
        try:
            self.logger.info("Adding summary")
            table = self.read_database(database_id)
            for row in table['results']:
                name = row['properties']['Name']['title'][0]["plain_text"]
                if not row['properties']["AI summary"]["rich_text"]:
                    id_page = row["id"]
                    self.logger.info(f"Getting summary of page with id: {id_page}")
                    text_page_mk = self.get_mk_page(id_page)
                    summary = self.get_summary(text_page_mk)
                    rich_text = [{
                        "type": "text",
                        "text": {
                            "content": summary,
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": summary,
                        "href": None
                    }]
                    self.logger.info(f"Adding summary to page with name: {name}")
                    update_data = {"properties":{"AI summary":{"rich_text": rich_text}}}
                    self.update_page(id_page, update_data)
                else:
                    self.logger.info(f"Skipping summary of page with name: {name}")
        except Exception as e:
            self.logger.error("Error in adding summary:" + str(e))


    def add_tags(self, database_id:str)->None:
        """
        Add the tags to the given database
        :param database_id: the id of the database
        :type database_id: str
        :return: None
        :rtype: None
        """
        try:
            self.logger.info("Adding topic tags")
            table = self.read_database(database_id)
            for row in table['results']:
                name = row['properties']['Name']['title'][0]["plain_text"]
                if not row['properties']["Topics"]["multi_select"]:
                    id_page = row["id"]
                    self.logger.info(f"Getting topic tags of page with id: {id_page}")
                    text = row['properties']["AI summary"]["rich_text"]
                    tags_list = self.get_tags(text)
                    tags = [tag.upper() for tag in tags_list]
                    self.logger.info("TAGs: [" + ",".join(tags) + "]")
                    multi_select = [{"name": tag} for tag in tags]
                    self.logger.info(f"Adding topic tags to page with name: {name}")
                    update_data = {"properties":{"Topics":{"multi_select": multi_select}}}
                    self.update_page(id_page, update_data)
                else:
                    self.logger.info(f"Skipping topic tags of page with name: {name}")
        except Exception as e:
            self.logger.error("Error in adding summary:" + str(e))