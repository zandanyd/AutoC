import multiprocessing
from typing import Optional
import logging
import re
import docling.exceptions
from docling.document_converter import DocumentConverter
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTMLParser:
    def __init__(self, url: str):
        self.url = url
        self.converter = DocumentConverter()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    @staticmethod
    def _extract_article_content_from_markdown(markdown: str) -> str:
        # Regex to match the title and everything after it, TODO: improve method (?)
        pattern = r"(# .*)"
        match = re.search(pattern, markdown, re.DOTALL)
        if match:
            return match.group(1)
        return markdown

    def _manually_fetch_blog_html_content(self) -> str:
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Remove common irrelevant elements
        for element in soup(["script", "style", "footer", "header", "nav"]):
            element.extract()

        # Remove elements with certain classes or IDs
        for element in soup(
            ["div", "span"],
            {"class": ["sidebar", "widget", "advertisement", "comments"]},
        ):
            element.extract()

        # Extract the remaining text content
        return soup.get_text(strip=True)

    def _extract_textual_content_with_docling(
        self, result_queue: multiprocessing.Queue
    ):
        logger.info("Attempting to extract HTML data using docling")
        try:
            conversion_result = self.converter.convert(source=self.url)
            markdown = conversion_result.document.export_to_markdown(
                image_placeholder=""
            )
            if markdown:
                result_queue.put(self._extract_article_content_from_markdown(markdown))
                return
        except docling.exceptions.ConversionError:
            logger.warning("Failed to extract blog content using docling")
        result_queue.put(None)

    def _extract_textual_content_with_beautifulsoup(self) -> Optional[str]:
        logger.info("Attempting to extract HTML data using BeautifulSoup")
        try:
            content = self._manually_fetch_blog_html_content()
            return content if content else None
        except Exception as e:
            logger.warning(f"Failed to extract blog content using BeautifulSoup: {e}")
        return None

    def get_textual_content(self) -> Optional[str]:
        result_queue = multiprocessing.Queue()
        process = multiprocessing.Process(
            target=self._extract_textual_content_with_docling, args=(result_queue,)
        )
        process.start()
        process.join(timeout=60)

        if process.is_alive():
            logger.warning(
                "Docling extraction is taking too long, falling back to BeautifulSoup"
            )
            process.terminate()
            process.join()

        content = result_queue.get() if not result_queue.empty() else None

        if content is None:
            content = self._extract_textual_content_with_beautifulsoup()

        if content:
            return content

        logger.error("Failed to extract blog content")
