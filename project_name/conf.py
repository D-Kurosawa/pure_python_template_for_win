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
        conf = _load_json_config()
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
        self.foo_a = _make_load_file(self._dic['foo_A'])

    def _set_info_of_foo_b_files(self):
        self.foo_b = _find_load_files(self._dic['foo_B'])


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
        self.bar_a = _make_load_file(self._dic['bar_A'])

    def _set_info_of_bar_b_files(self):
        self.bar_b = _find_load_files(self._dic['bar_B'])


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
        self.foo_a = _make_save_file(self._dic['foo_A'])

    def _set_info_of_foo_b_base_file(self):
        self.foo_b = _make_base_file(self._dic['foo_B'])


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
        self.bar_a = _make_save_file(self._dic['bar_A'])

    def _set_info_of_bar_b_base_file(self):
        self.bar_b = _make_base_file(self._dic['bar_B'])


def _load_json_config():
    """
    :rtype: dict
    """
    try:
        arg = sys.argv[1]
    except IndexError:
        raise IndexError('Not found command line arguments')
    except Exception:
        raise Exception

    with open(arg, 'r', encoding='utf-8') as j:
        return json.load(j)


def _exists_path(path):
    """
    :type path: str
    :rtype: Path
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    return p


def _make_load_file(dic):
    """
    :type dic: dict
    :rtype: Path
    """
    p = _exists_path(dic['path'])
    file = p / dic['file']

    if not file.exists():
        raise FileNotFoundError(dic['file'])

    return file


def _make_save_file(dic):
    """
    :type dic: dict
    :rtype: Path
    """
    p = _exists_path(dic['path'])
    return p / dic['file']


def _make_base_file(dic):
    """
    :type dic: dict
    :rtype: Path
    """
    p = _exists_path(dic['path'])
    return p / dic['base_name']


def _find_load_files(dic):
    """
    :type dic: dict
    :rtype: list[Path]
    """
    p = _exists_path(dic['path'])
    files = [f for f in p.glob(f"**/{dic['pattern']}")]

    if not files:
        raise FileNotFoundError(files)

    return files


if __name__ == '__main__':
    def _main():
        conf = ConfigLoader()
        conf.load()
        conf.walk()


    _main()
