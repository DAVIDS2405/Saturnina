import logging
import sys
from logtail import LogtailHandler
from config.envs import settings

# Logger principal de la aplicación
logger = logging.getLogger('app_logger')

formatter = logging.Formatter(
    fmt="%(levelname)s:     %(message)s  %(asctime)s", datefmt='%m/%d/%Y %I:%M:%S %p')

# Handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app/logs/app.log')
better_stack_handler = LogtailHandler(source_token=settings.LOGGER_TOKEN)

# Configurar los formatos
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
better_stack_handler.setFormatter(formatter)

# Agregar handlers al logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.addHandler(better_stack_handler)

# Nivel del logger
logger.setLevel(logging.INFO)
