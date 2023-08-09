from tortoise import Tortoise


async def clean_db() -> None:
    connection = Tortoise.get_connection("default")
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    _, result = await connection.execute_query(query)
    tables = [row[0] for row in result]
    for table in tables:
        query = f"DROP TABLE IF EXISTS {table} CASCADE;"
        await connection.execute_query(query)
