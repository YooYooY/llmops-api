from pathlib import Path

from flask import request, Blueprint
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from utils import success, fail, auto_handle_exceptions

rag_bp = Blueprint("rag", __name__)

# Base RAG + history prompt
RAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Use ONLY the given context to answer the user. "
        "If the context is not sufficient, say \"I don't know\".\n\n"
        "Context:\n{context}"
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])


def _get_history_dir() -> Path:
    history_dir = Path("./history")
    history_dir.mkdir(parents=True, exist_ok=True)
    return history_dir


def get_session_history(session_id: str) -> FileChatMessageHistory:
    history_dir = _get_history_dir()
    file_path = history_dir / f"{session_id}.json"
    return FileChatMessageHistory(str(file_path))


@auto_handle_exceptions(ignore=["health_check"])
class RagController:
    def __init__(self, vector_store, llm):
        """
        :param vector_store: an instance of WeaviateV4VectorStore (or similar API)
        :param llm: a ChatOpenAI (or any LangChain chat model)
        """
        self.vector_store = vector_store
        self.llm = llm

        # Build base chain (prompt -> llm)
        base_chain = RAG_PROMPT | self.llm

        # Wrap chain with history support
        self.chain_with_memory = RunnableWithMessageHistory(
            base_chain,
            lambda session_id: get_session_history(session_id),
            input_messages_key="input",
            history_messages_key="history",
        )

    def health_check(self):
        """Excluded from exception wrapping."""
        return success(message="RAG service is up.")

    def add_docs(self, app_id):
        body = request.get_json(force=True) or {}
        texts = body.get("texts", [])
        metadatas = body.get("metadatas", [{} for _ in texts])

        if not texts:
            return fail("Missing texts", status=400)

        ids = self.vector_store.add_texts(texts, metadatas)
        return success({"count": len(ids), "ids": ids}, "Documents added.")

    def search(self, app_id):
        body = request.get_json(force=True) or {}
        query = body.get("query")
        k = int(body.get("k", 3))

        if not query:
            return fail("Missing query", status=400)

        docs = self.vector_store.similarity_search(query, k=k)

        return success({
            "query": query,
            "result": [
                {"text": d.page_content, "metadata": d.metadata}
                for d in docs
            ]
        })

    def rag_search(self, app_id):
        """RAG endpoint with file-based chat history (per app_id)."""
        body = request.get_json(force=True) or {}
        query = body.get("query")
        k = int(body.get("k", 3))

        if not query:
            return fail("Missing query", status=400)

        # 1) Retrieve relevant docs from Weaviate
        docs = self.vector_store.similarity_search(query, k=k)
        context = "\n\n".join([d.page_content for d in docs])

        # 2) Use app_id as session_id
        session_id = str(app_id)

        # 3) Invoke chain with memory. Pass context + user input
        response = self.chain_with_memory.invoke(
            {"input": query, "context": context},
            config={"configurable": {"session_id": session_id}},
        )

        return success({
            "query": query,
            "answer": response.content,
            "context_snippets": [d.page_content for d in docs],
            "session_id": session_id,
        })

    def history(self, app_id):
        """
        Return last N messages for this session.
        GET /history?limit=20
        """
        limit = int(request.args.get("limit", 50))  # default: 50 messages
        session_id = str(app_id)

        # Load FileChatMessageHistory for this session
        history = get_session_history(session_id)

        messages = history.messages  # List[BaseMessage]

        # Only return last N messages
        sliced = messages[-limit:]

        # Convert LangChain messages -> JSON-safe structure
        formatted = []
        for m in sliced:
            formatted.append({
                "role": m.type,  # "human", "ai", "system"
                "content": m.content
            })

        return success({
            "session_id": session_id,
            "total_messages": len(messages),
            "messages": formatted
        })

    def delete_docs(self, app_id):
        body = request.get_json(force=True) or {}
        ids = body.get("ids", [])

        if not ids:
            return fail("Missing ids", status=400)

        self.vector_store.delete(ids)
        return success({"count": len(ids), "ids": ids}, "Documents deleted.")
