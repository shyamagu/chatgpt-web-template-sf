from pydantic import BaseSettings
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import re
from logger import logger
import tiktoken

class Settings(BaseSettings):
    FORM_REC_ENDPOINT :str
    FORM_REC_KEY :str

settings = Settings(_env_file=".env")

endpoint = settings.FORM_REC_ENDPOINT
key = settings.FORM_REC_KEY

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

def analyze_pdf(url):
    formUrl = url
    return_result = []

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document_from_url(
            "prebuilt-layout", formUrl)
    result = poller.result()

    index = 0
    for paragraph in result.paragraphs:
        content = paragraph.content
        content = re.sub(r'\s+',  ' ', content).strip()
        content = re.sub(r". ,","",content)
        # remove all instances of multiple spaces
        content = content.replace("..",".")
        content = content.replace(". .",".")
        content = content.replace("\n", "")
        content = content.strip()

        tokenizer = tiktoken.get_encoding("cl100k_base")
        tokenized = tokenizer.encode(content)
        if len(tokenized) > 8192:
            content = tokenizer.decode(tokenized[:8192])

        return_result.append({"id":index,"role":paragraph.role,"content":content})
        index += 1

    return return_result