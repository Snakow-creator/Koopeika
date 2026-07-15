from config import profile
from tasks.logger import log


async def profile_cleaner():
    log.debug("check profile cleanup")
    try:
        profile.cleanup(timeout=15) # default 1800
        log.debug("Successfully profile cleanup")
    except Exception as e:
        log.error(f"Profile cleanup error: {e}")
