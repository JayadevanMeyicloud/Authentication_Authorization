import logging

logging.basicConfig(
    filename='app.log',
    filemode='w',   # use lowercase
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Application started")