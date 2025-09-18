from database.requests_migrate import migrate

import asyncio

if __name__ == "__main__":
    asyncio.run(migrate())
