import logging


logger = logging.Logger("datapack-generator", logging.INFO)

def command_warning(name: str, *warnings: str):
    message = " ".join(warnings)
    logger.warning(f"( /{name} ) {message}")
