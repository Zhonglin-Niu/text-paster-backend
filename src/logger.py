import sys
import logging


def get_logger() -> logging.Logger:
    return SingletonLogger().logger


def exception_handler(exctype, value, traceback):
    get_logger().error("Uncaught exception", exc_info=(exctype, value, traceback))


class SingletonLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            sys.excepthook = exception_handler
            cls._instance = super(SingletonLogger, cls).__new__(cls)

            # 创建日志记录器
            cls._instance.logger = logging.getLogger(__name__)
            cls._instance.logger.setLevel(logging.DEBUG)

            # 创建一个handler，用于写入日志文件
            fh = logging.FileHandler('log', encoding='utf-8')

            # 定义handler的输出格式
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)-10s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S'
            )
            fh.setFormatter(formatter)

            # 将处理器添加到记录器
            cls._instance.logger.addHandler(fh)

        return cls._instance
