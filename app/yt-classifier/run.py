import uvicorn
import psutil
import score_lists
from config import BaseConfig

score_lists.read_lists()

if __name__ == "__main__":
    print("number of Logical CPUS Detected:", psutil.cpu_count(logical=True))
    print("number of Physical CPUS Detected:", psutil.cpu_count(logical=False))
    if int(BaseConfig.AUTODETECT_CPU) > 0:
        uvicorn.run("fastapi-app:application", host="0.0.0.0", port=int(BaseConfig.SERVICE_PORT), log_level="info",
                    workers=psutil.cpu_count(logical=True))
    else:
        uvicorn.run("fastapi-app:application", host="0.0.0.0", port=int(BaseConfig.SERVICE_PORT), log_level="info",
                    workers=1)
