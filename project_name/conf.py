"""Load application configure file"""
import json
import sys
from pathlib import Path

from .mypkg import mputil


class ConfigLoader:
    """
    :type setting: AppSettings
    :type loads: AppLoadings
    :type saves: AppSavings
    """

    def __init__(self):
        conf = JsonCmdLineArg.load()
        self.setting = AppSettings(conf['set'])
        self.loads = AppLoadings(conf['load'])
        self.saves = AppSavings(conf['save'])

    def load(self):
        self.setting.set()
        self.loads.set()
        self.saves.set()

    def walk(self):
        for key, val in self._walk_generator(self.__dict__):
            print(f"{key:<40}: {val}")

    def _walk_generator(self, dic):
        """
        :type dic: dict
        """
        for key, val in dic.items():
            yield key, val
            try:
                nest_value = val.__dict__  # type: dict
            except AttributeError:
                pass
            else:
                for child_key, child_val in self._walk_generator(nest_value):
                    yield key + ' -> ' + child_key, child_val


class AppSettings:
    """
    :type _dic: dict
    :type cpu: int
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        self._dic = dic
        self.cpu = 1

    def set(self):
        self._set_info_of_number_of_usage_cpu()

    def _set_info_of_number_of_usage_cpu(self):
        self.cpu = mputil.MpCPU(self._dic['cpu']).get()


class AppLoadings:
    """
    :type foo: LoadingFooInfoSetter
    :type bar: LoadingBarInfoSetter
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        self.foo = LoadingFooInfoSetter(dic['foo'])
        self.bar = LoadingBarInfoSetter(dic['bar'])

    def set(self):
        self.foo.set()
        self.bar.set()


class LoadingFooInfoSetter:
    """
    :type _dic: dict
    :type foo_a: Path
    :type foo_b: list[Path]
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        self._dic = dic
        self.foo_a = Path()
        self.foo_b = list()

    def set(self):
        self._set_info_of_foo_a_file()
        self._set_info_of_foo_b_files()

    def _set_info_of_foo_a_file(self):
        self.foo_a = FileMaker.load(self._dic['foo_A'])

    def _set_info_of_foo_b_files(self):
        self.foo_b = FileMaker.find(self._dic['foo_B'])


class LoadingBarInfoSetter:
    """
    :type _dic: dict
    :type bar_a: Path
    :type bar_b: list[Path]
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        self._dic = dic
        self.bar_a = Path()
        self.bar_b = list()

    def set(self):
        self._set_info_of_bar_a_file()
        self._set_info_of_bar_b_files()

    def _set_info_of_bar_a_file(self):
        self.bar_a = FileMaker.load(self._dic['bar_A'])

    def _set_info_of_bar_b_files(self):
        self.bar_b = FileMaker.find(self._dic['bar_B'])


class AppSavings:
    """
    :type foo: SavingFooInfoSetter
    :type bar: SavingBarInfoSetter
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        self._dic = dic
        self.foo = SavingFooInfoSetter(dic['foo'])
        self.bar = SavingBarInfoSetter(dic['bar'])

    def set(self):
        self.foo.set()
        self.bar.set()


class SavingFooInfoSetter:
    """
    :type _dic: dict
    :type foo_a: Path
    :type foo_b: Path
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        self._dic = dic
        self.foo_a = Path()
        self.foo_b = Path()

    def set(self):
        self._set_info_of_foo_a_file()
        self._set_info_of_foo_b_base_file()

    def _set_info_of_foo_a_file(self):
        self.foo_a = FileMaker.save(self._dic['foo_A'])

    def _set_info_of_foo_b_base_file(self):
        self.foo_b = FileMaker.base(self._dic['foo_B'])


class SavingBarInfoSetter:
    """
    :type _dic: dict
    :type bar_a: Path
    :type bar_b: Path
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        self._dic = dic
        self.bar_a = Path()
        self.bar_b = Path()

    def set(self):
        self._set_info_of_bar_a_file()
        self._set_info_of_bar_b_base_file()

    def _set_info_of_bar_a_file(self):
        self.bar_a = FileMaker.save(self._dic['bar_A'])

    def _set_info_of_bar_b_base_file(self):
        self.bar_b = FileMaker.base(self._dic['bar_B'])


class JsonCmdLineArg:

    @staticmethod
    def _get_cmd_line_arg():
        """
        :rtype: str
        """
        try:
            arg = sys.argv[1]
        except IndexError:
            raise IndexError('Not found command line arguments')
        except Exception:
            raise Exception
        return arg

    @classmethod
    def load(cls):
        """
        :rtype: dict
        """
        with open(cls._get_cmd_line_arg(), 'r', encoding='utf-8') as j:
            return json.load(j)


class FileMaker:

    @staticmethod
    def _has_key(dic, *args):
        """
        :type dic: dict
        """
        for arg in args:
            if arg not in dic:
                raise KeyError(f"Not in key : {arg}")

    @staticmethod
    def _exists_path(path):
        """
        :type path: str
        :rtype: Path
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)

        return p

    @classmethod
    def load(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, 'path', 'file')

        p = cls._exists_path(dic['path'])
        file = p / dic['file']

        if not file.exists():
            raise FileNotFoundError(dic['file'])

        return file

    @classmethod
    def find(cls, dic):
        """
        :type dic: dict
        :rtype: list[Path]
        """
        cls._has_key(dic, 'path', 'pattern')

        p = cls._exists_path(dic['path'])
        files = [f for f in p.glob(f"**/{dic['pattern']}")]

        if not files:
            raise FileNotFoundError(files)

        return files

    @classmethod
    def save(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, 'path', 'file')

        p = cls._exists_path(dic['path'])
        return p / dic['file']

    @classmethod
    def base(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, 'path', 'base_name')

        p = cls._exists_path(dic['path'])
        return p / dic['base_name']


if __name__ == '__main__':
    def _main():
        conf = ConfigLoader()
        conf.load()
        conf.walk()


    _main()
