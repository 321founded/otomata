"""
Notion API client with caching support.
"""
import json
import hashlib
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
import requests


NOTION_API_KEY = "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"


class NotionClient:
    """Notion API client with automatic caching."""

    def __init__(self, token: Optional[str] = None):
        self.base_url = "https://api.notion.com/v1"
        self.token = token or NOTION_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2025-09-03",
            "Content-Type": "application/json"
        }

        # Setup cache directory
        self.cache_dir = Path(__file__).parent.parent / '.cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_ttl = 86400  # 24 hours

    def _get_cache_key(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> str:
        cache_data = {
            'method': method,
            'endpoint': endpoint,
            'params': params or {},
            'data': data or {}
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()

    def _get_cached(self, cache_key: str) -> Optional[Dict]:
        cache_file = self.cache_dir / f"{cache_key}.json"
        if not cache_file.exists():
            return None
        file_age = time.time() - cache_file.stat().st_mtime
        if file_age > self.cache_ttl:
            cache_file.unlink()
            return None
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def _set_cache(self, cache_key: str, data: Dict):
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to cache response: {e}")

    def _request(self, method: str, endpoint: str, params: Dict = None,
                 data: Dict = None, use_cache: bool = True) -> Dict:
        if use_cache and method == 'GET':
            cache_key = self._get_cache_key(method, endpoint, params, data)
            cached = self._get_cached(cache_key)
            if cached:
                print(f"✓ Using cached response")
                return cached

        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            result = response.json()

            if use_cache and method == 'GET':
                cache_key = self._get_cache_key(method, endpoint, params, data)
                self._set_cache(cache_key, result)

            return result

        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response.text else {}
            error_msg = error_data.get('message', str(e))
            error_code = error_data.get('code', '')
            status_code = e.response.status_code

            if status_code == 404:
                raise Exception(f"Notion API error (404): Resource not found. {error_msg}")
            elif status_code == 403:
                raise Exception(f"Notion API error (403): Forbidden. {error_msg}")
            elif status_code == 401:
                raise Exception(f"Notion API error (401): Unauthorized. {error_msg}")
            elif status_code == 400:
                raise Exception(f"Notion API error (400): Bad request. {error_msg}")
            else:
                raise Exception(f"Notion API error ({status_code}): {error_msg}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

    def search(self, query: str, filter_type: Optional[str] = None, sort: str = "relevance") -> Dict:
        data = {"query": query}
        if sort != "relevance":
            data["sort"] = {"direction": "descending", "timestamp": sort}
        if filter_type:
            data["filter"] = {"value": filter_type, "property": "object"}
        return self._request('POST', 'search', data=data, use_cache=True)

    def get_page(self, page_id: str) -> Dict:
        page_id = page_id.replace('-', '')
        return self._request('GET', f'pages/{page_id}')

    def get_page_blocks(self, page_id: str) -> Dict:
        page_id = page_id.replace('-', '')
        return self._request('GET', f'blocks/{page_id}/children')

    def query_data_source(self, data_source_id: str, filter_obj: Optional[Dict] = None,
                          sorts: Optional[list] = None, page_size: int = 100) -> Dict:
        data_source_id = data_source_id.replace('-', '')
        data = {"page_size": page_size}
        if filter_obj:
            data["filter"] = filter_obj
        if sorts:
            data["sorts"] = sorts
        return self._request('POST', f'data_sources/{data_source_id}/query', data=data)

    def query_database(self, database_id: str, filter_obj: Optional[Dict] = None,
                       sorts: Optional[list] = None, page_size: int = 100) -> Dict:
        database_id = database_id.replace('-', '')
        try:
            db_info = self.get_database(database_id)
            data_sources = db_info.get('data_sources', [])
            if not data_sources:
                raise Exception(f"Database {database_id} has no data sources.")
            data_source_id = data_sources[0]['id']
            return self.query_data_source(data_source_id, filter_obj, sorts, page_size)
        except Exception as e:
            raise

    def get_database(self, database_id: str) -> Dict:
        database_id = database_id.replace('-', '')
        return self._request('GET', f'databases/{database_id}')

    def create_page(self, parent_id: str, parent_type: str,
                    title: str, properties: Optional[Dict] = None,
                    content: Optional[list] = None) -> Dict:
        parent_id = parent_id.replace('-', '')
        data = {
            "parent": {f"{parent_type}_id": parent_id},
            "properties": {}
        }
        if parent_type == "database":
            data["properties"]["Name"] = {"title": [{"text": {"content": title}}]}
        else:
            data["properties"]["title"] = {"title": [{"text": {"content": title}}]}
        if properties:
            data["properties"].update(properties)
        if content:
            data["children"] = content
        return self._request('POST', 'pages', data=data, use_cache=False)

    def update_page(self, page_id: str, properties: Optional[Dict] = None,
                    archived: Optional[bool] = None) -> Dict:
        page_id = page_id.replace('-', '')
        data = {}
        if properties:
            data["properties"] = properties
        if archived is not None:
            data["archived"] = archived
        return self._request('PATCH', f'pages/{page_id}', data=data, use_cache=False)

    def append_blocks(self, page_id: str, blocks: list) -> Dict:
        page_id = page_id.replace('-', '')
        data = {"children": blocks}
        return self._request('PATCH', f'blocks/{page_id}/children', data=data, use_cache=False)
