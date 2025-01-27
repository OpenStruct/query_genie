## Understand the Components of a RAG System

A RAG system combines:

- Retrieval: Fetching relevant data from a database or knowledge base.
- Generation: Using a language model to generate a natural language response based on the retrieved data.

The hope for this project is to:

1. Parse the user's query.
2. Translate it into a database query (e.g., SQL).
3. Execute the query to retrieve the data.
4. Generate a response based on the retrieved data.

## System Design

**a. Natural Language Understanding (NLU)**

- Use a language model **(TBD)** to understand the user's query.
- Extract key information from the query, such as:
    - Metric: "How many people"
    - Condition: "spent more than $200"
    - Timeframe: "past 10 days"
    - ETC

**b. Query Translation**

- Convert the parsed query into a database query (e.g., SQL).
    - Example: "How many people spent more than $200 in the past 10 days"
      SQL:

```sql
SELECT COUNT(DISTINCT user_id)
FROM transactions
WHERE amount > 200
  AND transaction_date >= NOW() - INTERVAL '10 days';
```

**c. Database Interaction**

- Connect to your database (e.g., PostgreSQL, MySQL, etc.).
- Execute the generated query and retrieve the results.

**d. Response Generation**

- **TBD** on how the response should be. The response can be a simple count, a visualization, or a natural language
  sentence.

## 5. Challenges and Improvements

- Query Translation Accuracy
- Error Handling
- Performance
- Security

To help the model to understand the data in the database, we will feed it with the schema information. Example: table
names, column names, data types, relationships, etc.

```json
{
  "tables": [
    {
      "name": "transactions",
      "columns": [
        {
          "name": "user_id",
          "type": "integer",
          "foreign_key": "users.id"
        },
        {
          "name": "amount",
          "type": "float"
        },
        {
          "name": "transaction_date",
          "type": "date"
        }
      ]
    },
    {
      "name": "users",
      "columns": [
        {
          "name": "id",
          "type": "integer",
          "primary_key": true
        },
        {
          "name": "name",
          "type": "text"
        }
      ]
    }
  ]
}
```

This process will be automated whenever a user tries to interact with the system. The system will automatically fetch
the schema information from the database and feed it to the language model.

## Problems to resolve

1. Passing the schema information to the model causes an error, and so we need to find a better way of doing it.
```shell
Token indices sequence length is longer than the specified maximum sequence length for this model (2504 > 512). Running this sequence through the model will result in indexing errors
```