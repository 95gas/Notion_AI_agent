from llama_index.core import PromptTemplate

DEFAULT_SUMMARY_TEMPLATE = PromptTemplate(
    "Given the following markdown-formatted text {text}, return a really short summary as a new text reporting all the topics "
    "discussed in the text. Not start with 'the text explores ..' or 'the text is about ..'. Write it as it is a new text."
    "The summary has to match the language of the input text."
    "When the topic is changing, please start a new line."
)

DEFAULT_TAGGING_TEMPLATE = PromptTemplate(
    "Given the following text {text} related to the field of the personal growth, perform the following tasks:\n"
    "1-Provide a list of max 10 topic labels that describe the main topics discussed in the input text. The tags have to match the main language of the input text. 'Personal growth' is not a valid tag.\n"
    "2-Remove from the list those tags that are not belonging to the personal growth area.\n"
    "Return an JSON object containing the list with the tags. The list can be empty if no labels have been found."
    "Respect this JSON schema"
    "{"
    "   'tags_list': [str]"
    "}"
)