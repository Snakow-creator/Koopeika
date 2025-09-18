from database.models import delete_all

import asyncio

if __name__ == "__main__":
  asyncio.run(delete_all())
