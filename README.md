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
    # Название приложения
    # Подойдет любая строка из английских букв, цифр и символов '-', '_'
    name='console_example',

    # Информация про приложение
    # В целом тут может быть написано что угодно
    version='1.0',
    url='https://github.com/chegoryu/PythonSetupExample',
    license='MIT',
    author='Egor Chunaev',
    author_email='none@none.com',
    description='Console example with setuptools',

    # Какие пакеты надо собирать в этом приложении
    # Например пакеты в этом примере это ['cli', 'cli.helpers']
    # Можно указать их явно, но, к счастью, есть специальная функция которая сама их находит
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

Как можно заметить `setup.py` представляет собой вызов специальной функции из `setuptools` с правильными параметрами. Разберем их подробнее.

#### name и информация про приложение

```python
name='console_example',

version='1.0',
url='https://github.com/chegoryu/PythonSetupExample',
license='MIT',
author='Egor Chunaev',
author_email='none@none.com',
description='Console example with setuptools',
```

Среди всех этих параметров есть только два важных.

Первый это `name` которое задает общее имя нашего приложения. На него наложены некоторые ограничения, а именно - `name` должн состоять только из английских букв, цифр, символов `_`, `-`.

В качестве `name` рекомендуется указывать что-нибудь разумное из чего можно понять что делает ваше приложение.

Второй это `version` который должн удовлетворять [следующему формату](https://www.python.org/dev/peps/pep-0440).
На самом деле версия нам не так важна, поэтому всегда можно просто указывать `'1.0'`, переустановки приложения с такой же версией проходят штатно.

В остальных же полях можно написать что угодно.

#### packages

```python
from setuptools import find_packages

...

packages=find_packages(),
```

Набор пакетов в вашем приложении. В целом это просто набор всех директорий из которых состоит ваше приложение.

Например для следующей структуры директорий надо указать `['cli', 'cli.helpers']`:

```
.
├── cli
│   ├── __init__.py
│   ├── cli.py
│   └── helpers
│       ├── __init__.py
│       └── helpers.py
└── setup.py
```

К счастью есть фукнция `find_packages` которая сама может найти все пакеты в вашем приложении, лучше всего воспользоваться именно ей.

#### install_requires

```
install_requires=['click'],
```

Указание зависимостей нашего приложения.

Поиск пакетов для установки происходит в [pipy](https://pypi.org), в котором уже собрано более 273634 разных проектов.

В данном случае мы используем [библиотеку click](https://pypi.org/project/click).

#### entry_points

```python
entry_points={
    'console_scripts': [
        'console_example=cli:cli'
    ],
}
```

Входные точки в наше приложение.

Их может быть несколько, на каждую из них будет создан специальный скрипт запуска.
Например в примере выше будет создан скрипт запуска который запускает функцию `cli` из папки `cli`.

Его код нам не особо важен, но для общего развития его полезно посмотреть:

```python
#!/usr/local/bin/python3
# EASY-INSTALL-ENTRY-SCRIPT: 'console-example==1.0','console_scripts','console_example'
__requires__ = 'console-example==1.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('console-example==1.0', 'console_scripts', 'console_example')()
    )
```

В общем случае точки входа указываются следующим образом.

Пусть в файле `path/to/file.py` находится функции `run1` и `run2`, и мы хотим чтобы при установке создавались скрипты `run_my_app_ver1`, `run_my_app_ver2` которые запускают эти функции.

Также пусть у нас есть модуль `/path/to/module/__init__.py` в котором есть класс `MyApp` с статической функцией `run_main_loop`,
и мы хотим чтобы при установке создавался скрипт `run_my_app_ver3` который запускает эту фукнцию.

Тогда нам надо указать следующие точки входа:

```python
entry_points={
    'console_scripts': [
        'run_my_app_ver1=path.to.file:run1',
        'run_my_app_ver2=path.to.file:run2',
        'run_my_app_ver3=path.to.module:MyApp.run_main_loop'
    ],
}
```

### Как запускать

По сути запускать очень просто, всего лишь надо выполнить `./setup.py install` и все установится.

К сожалению скрипты для запуска установливаются куда-то вглубь системы, например на `unix` системах они будут установленны куда-то в `/usr/local/bin`.

Чтобы нам было удобно ими пользоваться их хочется установить (по факту создать) где-то рядом с местом откуда мы все устанавливаем,
для этого надо запустить `./setup.py install --install-scripts .` и все будет создано в той же директории где находится сейчас скрипт установки.

Но этого не рекомендуется делать, ибо скриптов для запуска может быть очень много и они просто засорят текущую директорию, лучше все использовать какую-то отдельную,
например `scripts`, тогда команда установки будет выглядеть как `./setup.py install --install-scripts ./scripts`.

Также не надо пугаться лишний файлов. Например после установки консольного приложения там будут созданы некоторые дополнительные файлы:
```
Что было до:
.
├── cli
│   ├── __init__.py
│   ├── cli.py
│   └── helpers
│       ├── __init__.py
│       └── helpers.py
└── setup.py

Что стало после (с учетом установки скриптов в ./scripts):
.
├── build
│   ├── bdist.macosx-10.12-x86_64
│   └── lib
│       └── cli
│           ├── __init__.py
│           ├── cli.py
│           └── helpers
│               ├── __init__.py
│               └── helpers.py
├── cli
│   ├── __init__.py
│   ├── cli.py
│   └── helpers
│       ├── __init__.py
│       └── helpers.py
├── console_example.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   ├── requires.txt
│   └── top_level.txt
├── dist
│   └── console_example-1.0-py3.7.egg
├── scripts
│   └── console_example
└── setup.py
```

Они создаются ибо `setuptools` все же был создан для распространения библиотек и эти файлы нужны для этого.

После установки консольное приложение можно запустить вот так (с учетом установки в ./scripts):

```
[~/PythonSetupExample/console_example]$ ./scripts/console_example
Usage: console_example [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  sort  Sort numbers.
  sum   Sum numbers.
chegoryu@chegoryu-osx:~/Desktop/PythonSetupExample/PythonSetupExample/console_example$ ./scripts/console_example sum 3 1 2
6
chegoryu@chegoryu-osx:~/Desktop/PythonSetupExample/PythonSetupExample/console_example$ ./scripts/console_example sort 3 1 2
1 2 3
chegoryu@chegoryu-osx:~/Desktop/PythonSetupExample/PythonSetupExample/console_example$ ./scripts/console_example sort 3 1 2 --reverse
3 2 1
```

### Пример с GUI

TODO

### Особенности работы с Windows

TODO
