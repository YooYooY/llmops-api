import os
from typing import List, Dict, Any

import weaviate
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from weaviate import connect_to_weaviate_cloud, connect_to_local
from weaviate.classes.config import Configure, Property, DataType


class WeaviateV4VectorStore:
    """
    Minimal vector store wrapper for Weaviate v4.

    Exposes a LangChain-like API:
      - add_texts(texts, metadatas)
      - similarity_search(query, k)
      - delete(ids)
    """

    def __init__(self, collection_name: str = os.getenv("WEAVIATE_COLLECTION", "")):
        self.collection_name = collection_name

        self._init_client()
        self._init_embeddings()
        self._ensure_collection()

    def _init_client(self):
        weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080").strip()
        weaviate_api_key = os.getenv("WEAVIATE_API_KEY", "").strip()
        openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()

        if not openai_api_key:
            raise RuntimeError("Missing OPENAI_API_KEY")

        # Cloud vs local selection
        if weaviate_api_key:
            self.client = connect_to_weaviate_cloud(
                cluster_url=weaviate_url,
                auth_credentials=weaviate.auth.AuthApiKey(weaviate_api_key),
                headers={"X-OpenAI-Api-Key": openai_api_key},
            )
        else:
            self.client = connect_to_local(
                host="localhost",
                port=8080,
                grpc_port=50051,
                headers={"X-OpenAI-Api-Key": openai_api_key},
            )

        if not self.client.is_ready():
            raise RuntimeError("Weaviate is not ready. Check WEAVIATE_URL / credentials / container.")

    def _init_embeddings(self):
        # You can change model name if needed
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    def _ensure_collection(self):
        if not self.client.collections.exists(self.collection_name):
            self.client.collections.create(
                name=self.collection_name,
                vectorizer_config=Configure.Vectorizer.none(),  # use our own vectors
                properties=[
                    Property(name="text", data_type=DataType.TEXT),
                    Property(name="page", data_type=DataType.INT),
                ],
            )
        self.collection = self.client.collections.get(self.collection_name)

    # ---------- Public API ----------

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] | None = None) -> List[str]:
        if metadatas is None:
            metadatas = [{} for _ in texts]

        vectors = self.embeddings.embed_documents(texts)
        ids: List[str] = []

        for text, meta, vec in zip(texts, metadatas, vectors):
            props: Dict[str, Any] = {"text": text}
            # add whitelist metadata fields here
            if "page" in meta:
                props["page"] = int(meta["page"])

            obj_uuid = self.collection.data.insert(properties=props, vector=vec)
            ids.append(str(obj_uuid))

        return ids

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        q_vec = self.embeddings.embed_query(query)
        result = self.collection.query.near_vector(near_vector=q_vec, limit=k)

        docs: List[Document] = []

        if result.objects is None:
            return docs

        for obj in result.objects:
            props = obj.properties or {}
            text = props.pop("text", "")
            metadata = props
            metadata["id"] = obj.uuid  # keep id in metadata

            docs.append(Document(page_content=text, metadata=metadata))

        return docs

    def delete(self, ids: List[str]) -> None:
        for uid in ids:
            try:
                self.collection.data.delete_by_id(uid)
            except Exception:
                # best-effort delete
                continue
