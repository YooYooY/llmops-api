### add

```bash
curl -X POST http://127.0.0.1:5000/add \
-H "Content-Type: application/json" \
-d '{
  "texts": [
    "Cats love sleeping in the sun.",
    "Dogs enjoy running in the park."
  ],
  "metadatas": [
    {"page": 1}, {"page": 2}
  ]
}'
```

### query

```bash
curl -X POST http://127.0.0.1:5000/query \
-H "Content-Type: application/json" \
-d '{"query": "I have a cat that loves napping all day."}'
```

### rag-query

```bash
curl -X POST http://127.0.0.1:5000/rag-query \
-H "Content-Type: application/json" \
-d '{"query": "Why do cats like to sleep so much?"}'
```

### delete

```bash
curl -X DELETE http://127.0.0.1:5000/delete \
-H "Content-Type: application/json" \
-d '{"ids": ["uuid-1"]}'
```