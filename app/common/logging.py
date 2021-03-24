import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s')

file_handler = logging.FileHandler('bank.log')
"""bank.log will get created """

file_handler.setFormatter(formatter)
"""setformatter for the time, levelname , message"""

stream_handler = logging.StreamHandler()
"""stream_handler to print the messages in the console"""

stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


