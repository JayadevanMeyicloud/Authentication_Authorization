import logging
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)
os.makedirs(
    LOG_DIR,
    exist_ok=True
)
LOG_FILE=os.path.join(
    LOG_DIR,
    "app.log"
)
logging.basicConfig(
    filename='LOG_FILE',
    filemode='a',   # use lowercase
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Application started")