from mirrorh import get_data_leaks
from database import create_table
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

async def main():
    create_table()
    await get_data_leaks()

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, 'interval', minutes=0.30)  
    scheduler.start()
    asyncio.get_event_loop().run_forever()
