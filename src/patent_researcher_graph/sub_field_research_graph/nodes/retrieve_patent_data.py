import http.client
import json
import datetime
from langchain_core.runnables import RunnableConfig
from ..state import SubFieldResearchGraphState


class RetrievePatentData:
    def __init__(self):
        self.configurable = None
    
    def retrieve_patent_data(self, state: SubFieldResearchGraphState, config: RunnableConfig):
        """
        Retrieves patent data from Google Patents using the given query and extracts specific fields.

        Args:
            query (str): The search query string.

        Returns:
            list: A list of dictionaries containing 'title', 'snippet', 'link', and 'priority_date' fields.
        """
        
        query = state["search_equation"]
        
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({
            "q": query,
            "num": 100
        })
        headers = {
            'X-API-KEY': '19d44f2fddd2f909067d631a8b7ee80a5efde880',
            'Content-Type': 'application/json'
        }
        
        # Send request
        conn.request("POST", "/patents", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data_formatted = json.loads(data.decode("utf-8"))
        organic = data_formatted.get("organic", [])
        
        entries_data = []
        
        for entry in organic:
            priorityDate = entry.get("priorityDate", None)

            # Parse priority date if available
            priority_date = None
            if priorityDate:
                try:
                    priority_date = datetime.strptime(priorityDate, "%Y-%m-%d")  # Adjust format to match "YYYY-MM-DD"
                except ValueError:
                    print(f"Error parsing priority date: {priorityDate}")

            # Store entry data
            entry_data = {
                "title": entry.get("title", "No title available"),
                "snippet": entry.get("snippet", "No snippet available"),
                "link": entry.get("link", "No link available"),
                "assignee": entry.get("assignee", "No link available"),
                "priority_date": priority_date,
                "publication_number": entry.get("publicationNumber", "No publication number available"),
            }
            entries_data.append(entry_data)
        
        return {"initial_patent_data": entries_data}
    
    def run(self, state, config: RunnableConfig):
        return self.retrieve_patent_data(state, config)