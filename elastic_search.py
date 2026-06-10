from typing import Any

import requests


DEFAULT_INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
    },
    "mappings": {
        "properties": {
            "course": {"type": "keyword"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "answer": {"type": "text"},
        }
    },
}


class ElasticSearchIndex:
    def __init__(
        self,
        index_name: str = "course-faq",
        base_url: str = "http://localhost:9200",
    ) -> None:
        self.index_name = index_name
        self.base_url = base_url.rstrip("/")

    def create_index(self, recreate: bool = False) -> None:
        if recreate:
            requests.delete(f"{self.base_url}/{self.index_name}", timeout=10)

        response = requests.put(
            f"{self.base_url}/{self.index_name}",
            json=DEFAULT_INDEX_SETTINGS,
            timeout=10,
        )

        if response.status_code not in {200, 201, 400}:
            response.raise_for_status()

        if response.status_code == 400 and "resource_already_exists_exception" not in response.text:
            response.raise_for_status()

    def index_documents(self, documents: list[dict[str, Any]]) -> None:
        for document in documents:
            document_id = document.get("id")
            url = f"{self.base_url}/{self.index_name}/_doc/{document_id}"
            response = requests.put(url, json=document, timeout=10)
            response.raise_for_status()

    def search(
        self,
        query: str,
        filter_dict: dict[str, Any] | None = None,
        boost_dict: dict[str, float] | None = None,
        num_results: int = 5,
    ) -> list[dict[str, Any]]:
        fields = self._build_fields(boost_dict)
        must_query: dict[str, Any] = {
            "multi_match": {
                "query": query,
                "fields": fields,
                "type": "best_fields",
            }
        }

        filters = []
        for key, value in (filter_dict or {}).items():
            filters.append({"term": {key: value}})

        body = {
            "size": num_results,
            "query": {
                "bool": {
                    "must": must_query,
                    "filter": filters,
                }
            },
        }

        response = requests.post(
            f"{self.base_url}/{self.index_name}/_search",
            json=body,
            timeout=10,
        )
        response.raise_for_status()

        hits = response.json()["hits"]["hits"]
        return [hit["_source"] for hit in hits]

    @staticmethod
    def _build_fields(boost_dict: dict[str, float] | None) -> list[str]:
        if not boost_dict:
            return ["question", "section", "answer"]

        fields = ["question", "section", "answer"]
        boosted_fields = []

        for field in fields:
            boost = boost_dict.get(field)
            if boost is None:
                boosted_fields.append(field)
            else:
                boosted_fields.append(f"{field}^{boost}")

        return boosted_fields
