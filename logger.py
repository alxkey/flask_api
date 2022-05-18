import logging

file_log = logging.FileHandler('file.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s \
                                                                                 %(threadName)s : %(message)s')
logger = logging.getLogger('LOGGER')