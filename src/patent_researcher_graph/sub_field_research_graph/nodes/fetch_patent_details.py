import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Optional, Union

from langchain_core.runnables import RunnableConfig
from ..state import SubFieldResearchGraphState, PatentDetails
from ...configuration import Configuration
from pydantic import BaseModel, Field

# -------------------------------------------------------------------
# Helper functions for web scraping patent details
# -------------------------------------------------------------------
async def fetch_details(session: aiohttp.ClientSession, patent: dict, semaphore: asyncio.Semaphore) -> dict:
    """
    Fetch detailed patent information asynchronously using aiohttp.
    """
    link = patent.get("link", "No link available")
    async with semaphore:
        try:
            print(f"Fetching detailed information from: {link}")
            async with session.get(link) as response:
                if response.status != 200:
                    print(f"Failed to retrieve content from {link}. Status code: {response.status}")
                    return {
                        "title": patent.get("title", "No title available"),
                        "snippet": patent.get("snippet", "No snippet available"),
                        "assignee": patent.get("assignee", "No assignee available"),
                        "publication_number": patent.get("publicationNumber", "No publication number available"),
                        "link": link,
                        "priority_date": patent.get("priority_date", None),
                        "abstract": "Failed to fetch",
                        "claims": "Failed to fetch",
                        "legal_status": "Failed to fetch",
                        "forward_citations": "Failed to fetch",
                    }
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                return {
                    "title": patent.get("title", "No title available"),
                    "snippet": patent.get("snippet", "No snippet available"),
                    "assignee": patent.get("assignee", "No assignee available"),
                    "publication_number": patent.get("publicationNumber", "No publication number available"),
                    "link": link,
                    "priority_date": patent.get("priority_date", None),
                    "abstract": get_abstract(soup),
                    "claims": get_claims(soup),
                    "legal_status": extract_last_legal_status(soup),
                    "forward_citations": count_forward_citations(soup),
                }
        except Exception as e:
            print(f"Error while processing {link}: {e}")
            return {
                "title": patent.get("title", "No title available"),
                "snippet": patent.get("snippet", "No snippet available"),
                "assignee": patent.get("assignee", "No assignee available"),
                "publication_number": patent.get("publicationNumber", "No publication number available"),
                "link": link,
                "priority_date": patent.get("priority_date", None),
                "abstract": "Error occurred",
                "claims": "Error occurred",
                "legal_status": "Error occurred",
                "forward_citations": "Error occurred",
            }

async def process_patent_details_async(patents: List[dict], max_concurrent_requests: int = 10) -> List[dict]:
    """
    Enriches patent data with detailed information via asynchronous web scraping.
    """
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_details(session, patent, semaphore) for patent in patents]
        results = await asyncio.gather(*tasks)
    return results

async def process_patent_details(patents: List[dict]) -> List[dict]:
    """
    Wrapper for asynchronous processing of patent details.
    """
    return await process_patent_details_async(patents)

# -------------------------------------------------------------------
# Web scraping helper functions for extracting specific content
# -------------------------------------------------------------------
def get_abstract(soup: BeautifulSoup) -> str:
    """
    Extracts the abstract from the BeautifulSoup object.
    """
    abstract_text = ""
    try:
        abstract_section = soup.find('section', {'itemprop': 'abstract'})
        if abstract_section:
            abstract_div = abstract_section.find('div', class_='abstract')
            if abstract_div:
                abstract_text = abstract_div.get_text(strip=True)
            else:
                # Fallback: traverse nested containers
                for element in abstract_section.find_all(True, recursive=True):
                    if element.name and element.get_text(strip=True):
                        abstract_text += element.get_text(strip=True) + " "
        else:
            print("Abstract section with itemprop='abstract' not found.")
    except Exception as e:
        print(f"Error extracting abstract: {e}")
    return abstract_text.strip()

def get_claims(soup: BeautifulSoup, english: bool = False) -> str:
    """
    Extracts the claims from the BeautifulSoup object.
    """
    claims_text = ""
    try:
        claims_section = soup.find('section', {'itemprop': 'claims'})
        if claims_section:
            claims_elements = claims_section.find_all('claim', recursive=True)
            for claim in claims_elements:
                claim_text = claim.get_text(strip=True)
                claims_text += f"{claim_text} "
            if not claims_text.strip():
                claims_divs = claims_section.find_all('div', class_='claim-text', recursive=True)
                for claim_div in claims_divs:
                    claims_text += claim_div.get_text(strip=True) + " "
        if english:
            translated_elements = claims_section.find_all('span', class_='google-src-text')
            if translated_elements:
                claims_text = ""
                for element in translated_elements:
                    claims_text += element.get_text(strip=True) + " "
    except Exception as e:
        print(f"Error extracting claims: {e}")
    return claims_text.strip()

def extract_last_legal_status(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the last legal status from the patent HTML content.
    """
    applications = soup.find_all("li", itemprop="application")
    if not applications:
        return None
    last_application = applications[-1]
    legal_status = last_application.find("span", itemprop="legalStatus")
    return legal_status.get_text(strip=True) if legal_status else None

def count_forward_citations(soup: BeautifulSoup) -> Union[int, str]:
    """
    Counts the number of forward citations from the patent HTML content.
    """
    forward_family = soup.find_all("tr", itemprop="forwardReferencesFamily")
    forward_orig = soup.find_all("tr", itemprop="forwardReferencesOrig")
    forward_ind = soup.find_all("tr", itemprop="forwardReferences")
    total = len(forward_family) + len(forward_orig) + len(forward_ind)
    return total

# -------------------------------------------------------------------
# The FetchPatentDetails Node
# -------------------------------------------------------------------
class FetchPatentDetails:
    def __init__(self):
        self.configurable = None

    def run(self, state: SubFieldResearchGraphState, config: RunnableConfig):
        # Retrieve the basic patent documents from the state
        patents = state["initial_patent_documents"]
        if not patents:
            print("No initial patent documents found in state.")
            state["enriched_patent_documents"] = []
            return state

        # Use asyncio to run the asynchronous processing of patent details
        enriched_patents_dicts = asyncio.run(process_patent_details(patents))
        
        # Validate and transform each enriched patent detail using the Pydantic model
        enriched_patents = []
        for pd in enriched_patents_dicts:
            try:
                patent_detail = PatentDetails(**pd)
                enriched_patents.append(patent_detail)
            except Exception as e:
                print(f"Validation error for patent: {e}")
        
        # Update the state with the enriched patent documents
        return {"enriched_patent_documents": enriched_patents}
