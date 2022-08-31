import os
import sys
import json

from loguru import logger

CONFIG_PATH = "config/config.json"


def set_logger():
    log_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSSSSS} | " "<lvl>{level: ^9}</lvl> | " "{message}"
    )
    logger.add(sys.stderr, level="INFO", format=log_format)
    logger.add(
        f"logs/system.log",
        rotation="1 day",
        retention="7 days",
        level="INFO",
        encoding="UTF-8",
        compression="gz",
        format=log_format,
    )


def load_config():
    return load_json(CONFIG_PATH)


def load_json(file_path):
    return json.load(open(file_path, "r", encoding="UTF-8"))


def walk_dir(dir_path):
    for dirPath, _, fileList in os.walk(dir_path):
        for fileName in fileList:
            fullPath = os.path.join(dirPath, fileName)
            yield fullPath, fileName


def to_int(args):
    try:
        return int(args[0]), 1
    except:
        return 1, 0


def exchange_name(msg):
    exchange_list = [
        ("我", "!@#$1$#@!"),
        ("my", "!@#$2$#@!"),
        ("My", "!@#$3$#@!"),
        ("MY", "!@#$4$#@!"),
        ("你", "我"),
        ("妳", "我"),
        ("您", "我"),
        ("!@#$1$#@!", "你"),
        ("!@#$2$#@!", "your"),
        ("!@#$3$#@!", "Your"),
        ("!@#$4$#@!", "YOUR"),
    ]

    for sub, repl in exchange_list:
        msg = msg.replace(sub, repl)
    return msg


def get_token():
    config = load_config()
    token_key = "token_dev" if config["is_dev"] else "token_release"
    return config[token_key]


def get_debug_guild():
    config = load_config()
    return config.get("debug_guild", list())
