import requests


class NotionDatabase:
    def __init__(self, api_key, database_id):
        if not api_key or not database_id:
            raise ConnectionError("Notion Database: Require api key AND database id")

        self.api_key = api_key
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.base_url = "https://api.notion.com/v1"

        print("Notion init.")

    def check_property_value(self, property_name, target_value, property_type):
        url = f"{self.base_url}/databases/{self.database_id}/query"

        if property_type not in ["number", "title", "rich_text", "url"]:
            raise ValueError(
                "property_type must be 'number', 'title', 'rich_text', or 'url'."
            )

        filter_payload = {
            "property": property_name,
            property_type: {"equals": target_value},
        }

        payload = {"filter": filter_payload}

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            data = response.json()
            results = data.get("results")
            return len(results) > 0
        except Exception as e:
            raise ValueError(f"Network Connection Error during Notion query: {e}")

    def add_row(self, properties):
        url = f"{self.base_url}/pages"
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }

        try:
            response = requests.post(
                url, headers=self.headers, json=payload, timeout=10
            )
            response.raise_for_status()
            return "Successfully added item to notion database."

        except Exception as e:
            return f"Failed to add row. Error: {e}"
