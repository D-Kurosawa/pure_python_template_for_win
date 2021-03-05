"""Multi process utility"""
import os
from typing import ClassVar
from typing import Tuple
from typing import Union


class MpCPU:
    """Get number of CPU used by multi process"""

    _cpu: Union[int, str, None]
    _max_cpu: int
    _min_cpu: int
    _character_pattern: Tuple[str, ...]

    def __init__(self, cpu: Union[int, str, None] = None):
        self._cpu = cpu
        self._max_cpu = os.cpu_count()
        self._min_cpu = 1
        self._character_pattern = ("max", "min", "mid", "1/4", "1/2", "3/4", "auto")

    def get(self) -> int:
        if self._cpu is None:
            return self._max_cpu - 1

        if isinstance(self._cpu, int):
            return self._int_process()

        if isinstance(self._cpu, str):
            return self._str_process()

        raise TypeError(f"{type(self._cpu)} : Not int or str")

    def _int_process(self) -> int:
        if self._cpu > self._max_cpu:
            return self._max_cpu

        if self._min_cpu > self._cpu:
            return self._min_cpu

        return self._cpu

    def _str_process(self) -> int:
        if self._cpu.lower() not in self._character_pattern:
            raise KeyError(f"{self._cpu} not in {self._character_pattern}")

        if self._cpu.lower() == "max":
            return self._max_cpu

        if self._cpu.lower() == "min":
            return self._min_cpu

        if self._cpu.lower() == "mid":
            num = self._max_cpu // 2
            return self._get_cpu_number(num)

        if self._cpu.lower() == "1/4":
            num = self._max_cpu // 4
            return self._get_cpu_number(num)

        if self._cpu.lower() == "1/2":
            num = self._max_cpu // 2
            return self._get_cpu_number(num)

        if self._cpu.lower() == "3/4":
            num = self._max_cpu // 4
            num *= 3
            return self._get_cpu_number(num)

        return self._max_cpu - 1

    def _get_cpu_number(self, num: int) -> int:
        if self._min_cpu > num:
            return self._min_cpu
        else:
            return num


class MpCounter:
    """Get number of process by multi process"""

    _mp_count: ClassVar[int] = 0
    num: int

    def __init__(self):
        MpCounter.count_up()
        self.num = MpCounter._mp_count

    @classmethod
    def count_up(cls):
        cls._mp_count += 1

    def count_reset(self):
        MpCounter._mp_count = 0
        self.num = 0


class MpLines:
    """Multi process information lines"""

    def __init__(self, process_num=None, cpu_num=None, name=None):
        """
        :type process_num: int | None
        :type cpu_num: int | None
        :type name: str | None
        """
        self._process = process_num
        self._cpu = cpu_num
        self._name = name

    def top(self):
        print(f"\n{'*' * 60}")

        self._print_name(message="Start")

        if self._process is not None:
            print(f"  Process:{self._process:>5}")

        if self._cpu is not None:
            print(f"  CPU    :{self._cpu:>5}")

        print(f"{'*' * 60}")

    def bottom(self):
        print(f"{'*' * 60}")

        self._print_name(message="End")

        print(f"{'*' * 60}\n")

    def _print_name(self, message):
        """
        :type message: str
        """
        if self._name is None:
            print(f"<Multi process {message}>")
        else:
            print(f"<Multi process [{self._name}] {message}>")


if __name__ == "__main__":
    pass
