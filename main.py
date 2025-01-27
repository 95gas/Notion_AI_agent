import os
from dotenv import load_dotenv
from src.classes.LLMs import LLM
from src.classes.NotionAIAgent import NotionAIAgent
import logging

if __name__ == '__main__':

    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    logger = logging.getLogger("NotionAIAgent")

    #oad secrets
    load_dotenv("env/keys.env")

    # Initialize Notion agent
    try:
        llm = LLM().openai_llm()
        notion_agent = NotionAIAgent(llm)
        logger.info("Notion agent initialized successfully")
    except Exception as error:
        logger.error(f"Could not initialized agent: {error}")
        exit(1)

    # Run summary and topic tagging for notion database target
    database_id = os.getenv("DATABASE_ID")

    logger.info("Starting summary generation...")
    notion_agent.add_summary(database_id)
    logger.info("Starting topic labels generation...")
    notion_agent.add_tags(database_id)