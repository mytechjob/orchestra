import asyncio
from sqlalchemy import text
from src.db.session import engine, init_db

async def rebuild_users_table():
    async with engine.begin() as conn:
        print("Dropping users table...")
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        print("Table dropped.")
    
    print("Re-initializing database...")
    await init_db()
    print("Database rebuilt successfully.")

if __name__ == "__main__":
    asyncio.run(rebuild_users_table())
