import asyncio
import multiprocessing

from apps.daemon import Daemon
from .app import TronDaemon


class Core:

    daemons = (
        TronDaemon,
    )

    @classmethod
    def run(cls, daemon: Daemon):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(daemon.run)

    @classmethod
    def start(cls):
        processes = []
        for daemon in cls.daemons:
            process = multiprocessing.Process(target=cls.run, args=(daemon(),))
            processes.append(process)
            process.start()


class CliCore:
    # -help
    # ** Список демонов
    # ** Список параметров

    # Params
    # 0. -n ==> Название демона (Required)
    # 1. Поиск от блока и до блока  | -s ==> Начало (Optional)
    #                               | -e ==> Конец (Optional)
    # 2. Поиск из списка блоков     | -l ==> Список из блоков
    # 3. Поиск по кошелькам (Можно вместе с 1 или 2) | -a ==> Список из адресов
    # 4. Куда (По умолчанию выводит в консоль):
    # * -f___ ==> Записать в файл (-fJSON, -fTXT, -fXML) (Название файла)
    # * -s___ ==> Отправить в (-sTELEGRAM, -sEMAIL, -sRABBIT, -sREDIS) (Токен, почта или url)
    # * -gs ==> Записать в Google EXCEL

    @classmethod
    def start(cls):
        pass
