"""Given an article, extract IOCs from the content"""

import os
from dotenv import load_dotenv
import logging
from typing import List, Any
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from backend.prompts import get_prompts
from backend.llm import get_chat_llm_client
from backend.data_model.ioc import IOC, IOCType

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IOCsExtractor:
    def __init__(self, article_content: str):
        self.article_content = article_content
        self.prompts = get_prompts()

    @staticmethod
    def _llm() -> Any:
        model_name = os.getenv("LLM_MODEL", "meta-llama/llama-3-3-70b-instruct")

        return get_chat_llm_client(
            model_name=model_name,
            model_parameters={
                "decoding_method": "sample",
                "temperature": 0,
                "max_tokens": 1024,
            },
        )

    @staticmethod
    def _json_escaping(response: AIMessage) -> AIMessage:
        content = response.content
        content = content.replace("\\", "\\\\")
        return AIMessage(content=content)

    @staticmethod
    def _response_to_iocs(iocs_response: List[str], ioc_type: IOCType) -> List[IOC]:
        return [IOC(type=ioc_type, value=o) for o in iocs_response]

    def _extract_ioc(self, ioc_type: IOCType) -> RunnableSequence:
        llm = self._llm()
        system_message = SystemMessagePromptTemplate.from_template(
            template=self.prompts["iocs"]["system"],
            partial_variables={
                "ioc_type": ioc_type.value,
                "context": self.article_content,
            },
        )
        user_message = HumanMessage(content="LIST_OF_IOCS:")
        messages = [system_message, user_message]

        prompt = ChatPromptTemplate.from_messages(messages=messages)

        return (
            prompt
            | llm
            | (lambda x: self._json_escaping(x))
            | JsonOutputParser()
            | (lambda x: self._response_to_iocs(x, ioc_type))
        )

    def extract_iocs_from_text(self) -> List[IOC]:
        iocs, val_l = [], []
        tasks = {
            IOCType.URL.name: self._extract_ioc(IOCType.URL),
            IOCType.IP.name: self._extract_ioc(IOCType.IP),
            IOCType.MD5.name: self._extract_ioc(IOCType.MD5),
            IOCType.SHA256.name: self._extract_ioc(IOCType.SHA256),
            IOCType.CHROME_EXTENSION.name: self._extract_ioc(IOCType.CHROME_EXTENSION),
        }
        res = RunnableParallel(**tasks).invoke(input={})

        # make sure we remove duplicate iocs
        for ioc_of_type in res.values():
            for ioc in ioc_of_type:
                if ioc.value not in val_l:
                    iocs.append(ioc)
                    val_l.append(ioc.value)
        return iocs
