from uuid import UUID

from flask import request
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig

from internal.utils import TokenLimiter
from pkg.response import fail_message, success_json

RAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant who remembers past conversations."
        "Use the given context and past conversations to answer the user"
        "If the context is not sufficient, say \"I don't know\".\n\n"
        "Context:\n{context}"
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

limiter = TokenLimiter(model_name="gpt-3.5-turbo", max_tokens=3000)


def get_appid_history(session_id) -> FileChatMessageHistory:
    return FileChatMessageHistory(f"./storage/memory/chat_history_{session_id}.json")


class VectorStoreService:

    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm

        base_chain = RAG_PROMPT | self.llm

        self.chain_with_memory = RunnableWithMessageHistory(
            base_chain,
            lambda session_id: get_appid_history(session_id),
            input_messages_key="input",
            history_messages_key="history",
        )

    def add_doc(self, app_id: UUID):
        body = request.get_json(force=True) or {}
        texts = body.get("texts", [])
        metadatas = body.get("metadatas", [])

        if not texts:
            return fail_message("Missing texts")

        ids = self.vector_store.add_texts(texts, metadatas, app_id=str(app_id))

        return success_json({"count": len(ids), "ids": ids})

    def search(self, app_id: UUID):
        body = request.get_json(force=True) or {}
        query = body.get("query", {})
        k = int(body.get("k", 3))

        if not query:
            return fail_message("Missing query")

        docs = self.vector_store.similarity_search(query, k, app_id=str(app_id))

        return success_json({
            "query": query,
            "results": [
                {"text": d.page_content, "metadata": d.metadata}
                for d in docs
            ]
        })

    def rag_search(self, app_id: UUID):
        body = request.get_json(force=True) or {}
        query = body.get("query", {})
        k = int(body.get("k", 3))

        if not query:
            return fail_message("Missing query")

        docs = self.vector_store.similarity_search(query, k, app_id=str(app_id))
        context = "\n\n".join([d.page_content for d in docs])

        limiter.trim(get_appid_history(app_id))

        config: RunnableConfig = {"configurable": {"session_id": str(app_id)}}

        response = self.chain_with_memory.invoke(
            {"input": query, "context": context},
            config
        )

        return success_json({
            "query": query,
            "answer": response.content,
            "context_snippets": [d.page_content for d in docs],
            "app_id": app_id,
        })

    def delete_doc(self, app_id: UUID):
        body = request.get_json(force=True) or {}
        ids = body.get("ids", [])

        if not ids:
            return fail_message("Missing ids")

        result = self.vector_store.delete(ids, app_id=str(app_id))

        return success_json({
            "result": result,
            "app_id": str(app_id)
        })
