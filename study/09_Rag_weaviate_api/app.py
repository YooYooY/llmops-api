import uuid

from flask import Flask
from langchain_openai import ChatOpenAI

from rag_controller import rag_bp, RagController
from weaviate_store_v4 import WeaviateV4VectorStore


def create_app():
    app = Flask(__name__)

    # Init vector store + LLM
    vector_store = WeaviateV4VectorStore(collection_name="RagDocs")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    # Init controller
    controller = RagController(vector_store=vector_store, llm=llm)

    # --- Routes using app_id from URL ---
    @rag_bp.route("/apps/<uuid:app_id>/health", methods=["GET"])
    def health(app_id: uuid.UUID):
        return controller.health_check()

    @rag_bp.route("/apps/<uuid:app_id>/add", methods=["POST"])
    def add_docs(app_id: uuid.UUID):
        return controller.add_docs(app_id)

    @rag_bp.route("/apps/<uuid:app_id>/search", methods=["POST"])
    def search(app_id: uuid.UUID):
        return controller.search(app_id)

    @rag_bp.route("/apps/<uuid:app_id>/rag", methods=["POST"])
    def rag_search(app_id: uuid.UUID):
        return controller.rag_search(app_id)

    @rag_bp.route("/apps/<uuid:app_id>/delete", methods=["DELETE"])
    def delete_docs(app_id: uuid.UUID):
        return controller.delete_docs(app_id)

    @rag_bp.route("/apps/<uuid:app_id>/history", methods=["GET"])
    def history(app_id: uuid.UUID):
        return controller.history(app_id)

    app.register_blueprint(rag_bp, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
