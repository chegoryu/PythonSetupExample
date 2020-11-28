# PythonSetupExample

## Вступление

К сожалению сейчас нет простого способа для распространения приложений написаных на `Python`.
Это связано с тем что `Python` является интерпретируемым языком, и при попытке запустить приложение в другом окружении возникают проблемы с тем что:

* Не все нужные сторонние библиотеки установленны
* Не все установленные библиотеки обновлены до нужной версии

Есть несколько путей решения это проблемы. На первый взгляд самый простой путь - статическая сборка (когда все нужные зависимости зашиваются в один/несколько бинарных файлов и поставляются вместе).
Для этого уже написано много разных утилит, например [pyinstaller](https://www.pyinstaller.org) или [py2exe](https://www.py2exe.org).

Но эти утилиты стабильно работают только в рамках одной системы, например при попытке перенести бинарный файл собраный на `windows 7` на `windows 10` при запуске может возникнуть окно `magic *.dll file not found`,
а в худшем случае приложение будет крашится при запуске и понять в чем причина будет очень сложно.

Поэтому не хочется использовать статическую сборку, а хочется оставить интерпритацию кода.
Но в этом случае помимое основного приложения надо поставлять ещё и скрипт для установки всех нужных зависимостей.

В качестве этого скрипта предлагается использовать [setuptools](https://setuptools.readthedocs.io/en/latest).
Это достаточно популярный метод распространения библиотек на `Python`, в котором очень много сложных зависимостей можно описать в одну строчку:

```
install_requires=['kivy>=1.11.1', 'click']
```

И при вызове скрипта установки он сам найдет все нужные пакеты и установит/обновит их:

```
# Обновление kivy с версии 1.11.1 до версии 2.0.0rc4
# Обновление происходи поскольку мы разрешаем версию >=1.11.1 и при установке происходит поиск
# максимально возможной версии, которая удовлетворяет ограничениям

Processing dependencies for gui-example==1.0
Searching for Kivy==2.0.0rc4
Best match: Kivy 2.0.0rc4
Processing Kivy-2.0.0rc4-py3.7-macosx-10.12-x86_64.egg
Removing Kivy 1.11.1 from easy-install.pth file
Adding Kivy 2.0.0rc4 to easy-install.pth file

# Если бы было указано kivy==1.11.1, то была бы установленна именно эта версия

Processing dependencies for gui-example==1.0
Searching for kivy==1.11.1
Reading https://pypi.org/simple/kivy/
Downloading https://files.pythonhosted.org/packages/0f/51/1fdcd05217919e77016f8f241d19a87d1d15cf1c074d78a6f3c5ca44198b/Kivy-1.11.1-cp37-cp37m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl#sha256=8819a27a09871af451760cb69486ced52e830c8a0a37480f22ef5e692f12c05b
Best match: Kivy 1.11.1
Processing Kivy-1.11.1-cp37-cp37m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl
Installing Kivy-1.11.1-cp37-cp37m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl to /usr/local/lib/python3.7/site-packages
writing requirements to /usr/local/lib/python3.7/site-packages/Kivy-1.11.1-py3.7-macosx-10.12-x86_64.egg/EGG-INFO/requires.txt
Removing Kivy 2.0.0rc4 from easy-install.pth file
Adding Kivy 1.11.1 to easy-install.pth file
```

Поиск пакетов для установки происходит в [pipy](https://pypi.org), в котором уже собрано более 273634 разных проектов.

## Как установить pip и setuptools

Для работы с `setuptools` нам нужно установить менеджер пакетов `pip`.

Для этого уже есть много разных инструкций в интернете, например [инструкция с сайта pypa](https://pip.pypa.io/en/stable/installing).

При поиске в google первая статься на русском, которая описывает установку для всех систем (Windows/Max OS/Linux) [находится тут](https://pythonru.com/baza-znanij/ustanovka-pip-dlja-python-i-bazovye-komandy).

После установки `pip` надо установить `setuptools`:

```
pip install setuptools
```

Чтобы посмотреть список уже установленных пакетов и их версий, можно воспользоваться `pip list`.
У `pip` есть ещё много полезных комманд, со всеми можно ознакомиться через `pip -h`.

## setup.py

То, как устанавливать приложение описывается при помощи `setup.py` скрипта.
В данном репозитории уже написаны два примера - [для консольного приложения](https://github.com/chegoryu/PythonSetupExample/blob/master/console_example/setup.py) и [для приложения с GUI](https://github.com/chegoryu/PythonSetupExample/blob/master/gui_example/setup.py).

Ниже они будут разобраны подробнее.

Для запуска скриптов и приложений ниже показаны примеры команд для `unix` систем, для особенностей работы с `windows` есть отдельный раздел.

Чтобы скачать все примеры себе на компьютер можно либо воспользоваться `git` если он у вас настроен (команда `git clone git@github.com:chegoryu/PythonSetupExample.git`), либо скачать архив с репозиторием:

![image](https://github.com/chegoryu/PythonSetupExample/blob/master/readme_images/how_to_download.png)

### Как написать

Рассмотрим пример `setup.py` для [для консольного приложения](https://github.com/chegoryu/PythonSetupExample/blob/master/console_example/setup.py):

```python
#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    # Информация про приложение
    # В целом тут может быть написано что угодно
    # Единственные ограничения:
    #     1. Разумный name на английском языке без пробелов
    #     2. Версия в специальном формате, но для наших нужд не надо углубляться в детали и можно всегда писать '1.0'
    name='console_example',
    version='1.0',
    url='https://github.com/chegoryu/PythonSetupExample',
    license='MIT',
    author='Egor Chunaev',
    author_email='none@none.com',
    description='Console example with setuptools',

    # Какие пакеты надо собирать в этом приложении
    # Например пакеты в этом примере это ['cli', 'cli.helpers']
    # Можно указать их явно, но, к счастью, есть специальная функция которах их сама находит
    # Так же можно замети что отделение helpers.py в отдельную директорию кажется избыточным
    # на самом деле это так и есть и было сделано специально чтобы показать что происходит при
    # двух и более пакетах
    packages=find_packages(),

    # Зависимости для приложения
    # В данном случае мы используем внешнюю библиотеку 'click'
    install_requires=['click'],

    # Точка входа в приложение
    # По умолчанию скрипты для запуска устанавливается в '/usr/local/bin' или что-то подобное в других системах
    # Чтобы создать скрипт запуска в установочной директории запустите './setup.py install --install-scripts .'
    # после этого скрипт запуска будет создан в каталоге установки
    # и может быть запущен как './console_example <args>'
    # Но рекомендуется устанавливать скрипты в отдельной директории './setup.py install --install-scripts ./scripts'
    # потому что в дополнение к основным скриптам также могут быть установлены скрипты зависимостей,
    # это не заметно в случае с консольным приложением, но в случае примера приложения gui видно явно
    entry_points={
        'console_scripts': [
            'console_example=cli:cli'
        ],
    }
)
```

#### Информация про приложение

#### packages

#### install_requires

#### entry_points=

### Как запускать

TODO

### Пример с GUI

TODO

### Особенности работы с Windows

TODO
