from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load tokenizer and model
tokenizer = T5Tokenizer.from_pretrained("mrm8488/t5-base-finetuned-wikiSQL", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("mrm8488/t5-base-finetuned-wikiSQL")


def get_sql(query, schema):
    input_text = f"translate to PostgreSQL. The database has this schema {schema}. {query}"
    features = tokenizer([input_text], return_tensors="pt")

    output = model.generate(input_ids=features["input_ids"], attention_mask=features["attention_mask"])
    return tokenizer.decode(output[0], skip_special_tokens=True)


# def get_sql(query, schema):
#     # Split the schema into smaller chunks (e.g., one table at a time)
#     for table in schema["tables"]:
#         table_schema = {"tables": [table]}  # Process one table at a time
#         input_text = f"translate to PostgreSQL. The database has this schema {table_schema}. {query}"
#
#         features = tokenizer(
#             [input_text],
#             return_tensors="pt",
#             max_length=512,
#             truncation=True,
#         )
#
#         output = model.generate(input_ids=features["input_ids"], attention_mask=features["attention_mask"])
#         sql_query = tokenizer.decode(output[0], skip_special_tokens=True)
#         print(f"Generated SQL for table {table['name']}: {sql_query}")
#
#     return sql_query  # Return the last generated SQL query

# query = "How many models were finetuned using BERT as base model?"
# print(get_sql(query))
