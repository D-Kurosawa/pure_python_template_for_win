"""Execute multi process"""
import multiprocessing as mp
import os

from .conf import ConfigLoader
from .mypkg import mputil


class MpExec:
    """
    :type _conf: ConfigLoader
    :type _lines: mputil.MpLines
    """

    def __init__(self, conf):
        """
        :type conf: ConfigLoader
        """
        self._conf = conf
        self._lines = mputil.MpLines()

    def run(self):
        self._lines.top()

        with mp.Pool(self._conf.setting.cpu) as p:
            iterator = p.imap_unordered(self._wrapper, self._arguments())
            result = list(iterator)

        self._lines.bottom()
        self._is_success(result)

    def _arguments(self):
        foo = range(10)
        guide = len(foo) // self._conf.setting.cpu

        for f in foo:
            yield f, guide

    def _worker(self, foo, guide):
        print(
            f">>\t\tpid:{os.getpid():>6}{mputil.MpCounter().num:>5}/"
            f"{guide}\t\t*****EXAMPLE***** : {foo}"
        )

        bar = self._conf.setting.cpu
        print(bar)

        return True

    def _wrapper(self, args):
        return self._worker(*args)

    @staticmethod
    def _is_success(result):
        if not all(result):
            raise Exception("Multiprocessing return error")


if __name__ == "__main__":
    pass
