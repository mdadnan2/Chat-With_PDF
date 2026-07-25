from app.services.embedding_service import EmbeddingService

embedding_service = EmbeddingService()

text = """
Backend Developer with experience in Node.js,
NestJS, MongoDB, PostgreSQL and AWS.
"""

embedding = embedding_service.generate_embedding(text)

print(type(embedding))
print(len(embedding))
print(embedding[:10])