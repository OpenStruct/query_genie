from typing import Dict, List, Any

import asyncpg


async def get_schema(connection: asyncpg.Connection) -> Dict[str, List[str]]:
    """
    Fetch the database schema and simplify it to only include table names and column names.
    """
    schema = {}
    rows = await connection.fetch(
        """
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public';
        """
    )
    for row in rows:
        table_name = row["table_name"]
        column_name = row["column_name"]
        if table_name not in schema:
            schema[table_name] = []
        schema[table_name].append(column_name)  # Only include column names
    return schema


def schema_to_json(schema: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Convert the simplified schema to a JSON format.
    """
    return {
        "tables": [
            {"name": table, "columns": columns} for table, columns in schema.items()
        ]
    }
