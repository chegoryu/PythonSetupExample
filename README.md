# PythonSetupExample

1. [Вступление](#вступление)
2. [Как установить pip и setuptools](#как-установить-pip-и-setuptools)
3. [setup.py](#setuppy)
    1. [Как написать](#как-написать)
        1. [name и информация про приложение](#name-и-информация-про-приложение)
        2. [packages](#packages)
        3. [install_requires](#install_requires)
        4. [entry_points](#entry_points)
    2. [Как запускать](#как-запускать)
    3. [Пример с GUI](#пример-с-gui)
    4. [Особенности работы с windows](#особенности-работы-с-windows)
4. [Как правильно распространять приложения](#как-правильно-распространять-приложения)

## Вступление

К сожалению, на текущий момент не существует простых способов распространения приложений, написаных на языке `Python`, из-за того, что
`Python` является интерпретируемым языком, поэтому при попытке запустить приложение в другом окружении возникают следующие проблемы:

* Не все нужные сторонние библиотеки установленны
* Не все установленные библиотеки обновлены до нужной версии

Существует несколько способов решения данной проблемы. Самое простое из них - это статическая сборка, добавляющая все необходимые зависимости в один или несколько герметичных бинарных файлов.
На данный момент реализовано множество утилит для статической сборки, например [pyinstaller](https://www.pyinstaller.org) или [py2exe](https://www.py2exe.org).

К сожалению, эти утилиты стабильно работают только в рамках одной системы, например, при попытке запустить бинарный файл, собраный на `windows 7`, на `windows 10` может возникнуть ошибка вида `magic *.dll file not found` или молчаливое падение программы.

Учитывая вышеописанную проблему, хочется использовать не статическую сборку, а оставить интерпретацию кода. В этом случае помимо основного приложения необходимо поставлять ещё
и скрипт для установки нужных зависимостей.

Для написания такого скрипта предлагается использовать [setuptools](https://setuptools.readthedocs.io/en/latest).
Это достаточно популярный метод распространения библиотек на `Python`, в котором очень много сложных зависимостей можно описать в одну строчку, например

```
install_requires=['kivy>=1.11.1', 'click']
```

В таком случае при вызове скрипта установки `setuptools` сам найдет все нужные пакеты и установит или обновит их:

```
# Обновление kivy с версии 1.11.1 до версии 2.0.0rc4
# Обновление происходит поскольку мы разрешаем версию >=1.11.1 и при установке происходит поиск
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

Поиск пакетов для установки происходит в [pypi](https://pypi.org), в котором уже собрано более 273634 различных проектов.

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

Процедура установки приложения описывается при помощи скрипта `setup.py`.
В данном репозитории уже написаны два примера - [для консольного приложения](https://github.com/chegoryu/PythonSetupExample/blob/master/console_example/setup.py) и [для приложения с GUI](https://github.com/chegoryu/PythonSetupExample/blob/master/gui_example/setup.py).

Ниже они будут разобраны подробнее.

Для запуска скриптов и приложений ниже показаны примеры команд для `unix` систем, для особенностей работы с `windows` есть отдельный раздел.

Чтобы скачать все примеры себе на компьютер, можно либо воспользоваться `git`, если он у вас настроен (команда `git clone git@github.com:chegoryu/PythonSetupExample.git`), либо скачать архив с репозиторием:

![how_to_download](https://github.com/chegoryu/PythonSetupExample/blob/master/readme_images/how_to_download.png)

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
    # Внимательный читатель может заметить, что отделение helpers.py в отдельную директорию
    # является избыточным. Это сдеалано специально, чтобы показать работу с двумя или несколькими
    # пакетами.
    packages=find_packages(),

    # Зависимости для приложения
    # В данном случае мы используем внешнюю библиотеку 'click'
    install_requires=['click'],

    # Точка входа в приложение
    # По умолчанию скрипты для запуска устанавливается в '/usr/local/bin' или аналогичные директории в других системах
    # Чтобы создать скрипт запуска, в установочной директории запустите './setup.py install --install-scripts .'
    # после этого скрипт запуска будет создан в каталоге установки
    # и может быть запущен как './console_example <args>'
    # Рекомендуется устанавливать скрипты в отдельную директорию './setup.py install --install-scripts ./scripts'
    # потому что в дополнение к основным скриптам могут быть установлены скрипты зависимостей,
    # это не заметно в случае с консольным приложением, но в случае примера приложения gui видно явно
    entry_points={
        'console_scripts': [
            'console_example=cli:cli'
        ],
    }
)
```

Как можно заметить, `setup.py` представляет собой вызов специальной функции из `setuptools` с правильными параметрами. Разберем их подробнее.

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

Первый это `name`, задающий общее имя нашего приложения. На него наложены некоторые ограничения, а именно, `name` должно состоять только из английских букв, цифр, символов `_`, `-`.

В качестве `name` рекомендуется указывать что-нибудь разумное, из чего можно понять что делает ваше приложение.

Второй это `version`, который должен удовлетворять [следующему формату](https://www.python.org/dev/peps/pep-0440).
В нашем случае версия не так важна, поэтому всегда можно указывать `'1.0'`, переустановки приложения с такой же версией проходят штатно.

В остальных же полях можно написать что угодно.

#### packages

```python
from setuptools import find_packages

...

packages=find_packages(),
```

Набор пакетов в вашем приложении. В целом это просто набор всех директорий, в которых находится код вашего приложения.

Например, для следующей структуры директорий надо указать `['cli', 'cli.helpers']`:

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

К счастью, есть фукнция `find_packages` которая сама может найти все пакеты в вашем приложении, лучше всего воспользоваться именно ей.

#### install_requires

```
install_requires=['click'],
```

Указание зависимостей нашего приложения.

Поиск пакетов для установки происходит в [pypi](https://pypi.org).

В данном случае мы используем [библиотеку click](https://pypi.org/project/click).

#### entry_points

```python
entry_points={
    'console_scripts': [
        'console_example=cli:cli'
    ],
}
```

Точки входа в приложение.

Точек входа может быть несколько, на каждую из них будет создан специальный скрипт запуска.
Например, в примере выше будет создан скрипт запуска который запускает функцию `cli` из папки `cli`.

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

Пусть в файле `path/to/file.py` находятся функции `run1` и `run2`, и мы хотим, чтобы при установке создавались скрипты `run_my_app_ver1`, `run_my_app_ver2`, которые запускают эти функции.

Также пусть у нас есть модуль `/path/to/module/__init__.py`, в котором есть класс `MyApp` со статической функцией `run_main_loop`,
и мы хотим, чтобы при установке создавался скрипт `run_my_app_ver3`, который запускает эту фукнцию.

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

Запуск является простой задачей, достаточно всего лишь выполнить `./setup.py install`, после чего установятся все необходимые пакеты.

К сожалению, скрипты для запуска установливаются в системные директории, например на `unix` системах они будут установленны куда-то в `/usr/local/bin`.

Чтобы нам было удобно ими пользоваться, их хочется установить (по факту создать) где-то рядом с местом, откуда мы все устанавливаем,
для этого надо запустить `./setup.py install --install-scripts .` и все будет создано в той же директории, где находится сейчас скрипт установки.

Подобное делать не рекомендуется, поскольку скриптов для запуска может быть очень много и они просто засорят текущую директорию, лучше всего использовать
какую-то отдельную, например, `scripts`, тогда команда установки будет выглядеть как `./setup.py install --install-scripts ./scripts`.

Иногда для установки нужны права `superuser`'а, так что придется запускать `sudo ./setup.py install --install-scripts ./scripts`.

Также не надо пугаться лишних файлов. Например, после установки консольного приложения там будут созданы некоторые дополнительные файлы:
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

Они создаются поскольку `setuptools` изначально был создан для распространения библиотек, для которого нужны вспомогательные файлы.

После установки консольное приложение можно запустить вот так (с учетом установки в `./scripts`):

```
[~/PythonSetupExample/console_example]$ ./scripts/console_example
Usage: console_example [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  sort  Sort numbers.
  sum   Sum numbers.
[~/PythonSetupExample/console_example]$ ./scripts/console_example sum 3 1 2
6
[~/PythonSetupExample/console_example]$ ./scripts/console_example sort 3 1 2
1 2 3
[~/PythonSetupExample/console_example]$ ./scripts/console_example sort 3 1 2 --reverse
3 2 1
```

### Пример с GUI

Отличий написания `setup.py` для работы с GUI почти нет.

Если сравнить `setup.py` [для консольного приложения](https://github.com/chegoryu/PythonSetupExample/blob/master/console_example/setup.py) и [для приложения с GUI](https://github.com/chegoryu/PythonSetupExample/blob/master/gui_example/setup.py),
то можно увидеть, что важное отличие только в `entry_points`, там вместо `console_scripts` написано `gui_scripts`:

```python
entry_points={
    'gui_scripts': [
        'gui_example=gui:main'
    ],
}
```

В конкретном примере при установке будет создано много лишних скриптов, все они создаются из-за зависимости от `kivy`:
```
[~/PythonSetupExample/gui_example]$ ls scripts
chardetect            garden.bat            pygmentize            rst2html4.py          rst2latex.py          rst2odt.py            rst2pseudoxml.py      rst2xetex.py          rstpep2html.py
garden                gui_example           rst2html.py           rst2html5.py          rst2man.py            rst2odt_prepstyles.py rst2s5.py             rst2xml.py
```

Нас интересует только скрипт `gui_example`, при его запуске должно появиться окно с одной кнопкой и подобный лог в консоли:
```
[~/PythonSetupExample/gui_example]$ ./scripts/gui_example
[INFO   ] [Logger      ] Record log in /Users/chegoryu/.kivy/logs/kivy_20-11-28_2.txt
[INFO   ] [Kivy        ] v2.0.0rc4, git-d74461b, 20201015
[INFO   ] [Kivy        ] Installed at "/usr/local/lib/python3.7/site-packages/Kivy-2.0.0rc4-py3.7-macosx-10.12-x86_64.egg/kivy/__init__.py"
[INFO   ] [Python      ] v3.7.0 (default, Jun 29 2018, 20:14:27)
[Clang 9.0.0 (clang-900.0.39.2)]
[INFO   ] [Python      ] Interpreter at "/usr/local/opt/python/bin/python3.7"
[INFO   ] [Factory     ] 186 symbols loaded
[INFO   ] [Image       ] Providers: img_tex, img_imageio, img_dds, img_sdl2 (img_pil, img_ffpyplayer ignored)
[INFO   ] [Text        ] Provider: sdl2
[INFO   ] [Window      ] Provider: sdl2
[INFO   ] [GL          ] Using the "OpenGL ES 2" graphics system
[INFO   ] [GL          ] Backend used <sdl2>
[INFO   ] [GL          ] OpenGL version <b'2.1 ATI-1.51.8'>
[INFO   ] [GL          ] OpenGL vendor <b'ATI Technologies Inc.'>
[INFO   ] [GL          ] OpenGL renderer <b'AMD Radeon Pro 555 OpenGL Engine'>
[INFO   ] [GL          ] OpenGL parsed version: 2, 1
[INFO   ] [GL          ] Shading version <b'1.20'>
[INFO   ] [GL          ] Texture max size <16384>
[INFO   ] [GL          ] Texture max units <16>
[INFO   ] [Window      ] auto add sdl2 input provider
[INFO   ] [Window      ] virtual keyboard not allowed, single mode, not docked
[INFO   ] [Base        ] Start application main loop
[INFO   ] [GL          ] NPOT texture support is available
[INFO   ] [Base        ] Leaving application in progress...
```

![gui_example](https://github.com/chegoryu/PythonSetupExample/blob/master/readme_images/gui_example.png)

### Особенности работы с windows

Чтобы запустить `setup.py` под `windows` с правильными параметрами, надо открыть консоль, для этого надо нажать `win + r`, в открывшемся окне набрать `cmd` и нажать `enter`:

![windows_run_cmd](https://github.com/chegoryu/PythonSetupExample/blob/master/readme_images/windows_run_cmd.png)

Далее надо перейти в директорию с нашим проектом, пусть это будет `C:\Programs\tmp\PythonSetupExample\console_example`,
тогда надо выполнить `cd C:\Programs\tmp\PythonSetupExample\console_example`

```
C:\>cd C:\Programs\tmp\PythonSetupExample\console_example

C:\Programs\tmp\PythonSetupExample\console_example>
```

Далее нам надо запустить скрипт установки, в отличие от `unix` систем в `windows` придется явно указать чем запускать наш скрипт, для этого надо выполнить `python setup.py install --install-scripts ./scripts` (возможно у вас будут какие-то расширения, которые позволят это выполнить без явного указания `python`, но тут показан метод, который работает без расширений поверх стандартной инсталции `python`).

```
C:\Programs\tmp\PythonSetupExample\console_example>python setup.py install --install-scripts ./scripts
```

<details>
  <summary>Полный вывод</summary>

```
C:\Programs\tmp\PythonSetupExample\console_example>python setup.py install --install-scripts ./scrip
running install
running bdist_egg
running egg_info
writing console_example.egg-info\PKG-INFO
writing dependency_links to console_example.egg-info\dependency_links.txt
writing entry points to console_example.egg-info\entry_points.txt
writing requirements to console_example.egg-info\requires.txt
writing top-level names to console_example.egg-info\top_level.txt
reading manifest file 'console_example.egg-info\SOURCES.txt'
writing manifest file 'console_example.egg-info\SOURCES.txt'
installing library code to build\bdist.win32\egg
running install_lib
running build_py
creating build\bdist.win32\egg
creating build\bdist.win32\egg\cli
copying build\lib\cli\cli.py -> build\bdist.win32\egg\cli
creating build\bdist.win32\egg\cli\helpers
copying build\lib\cli\helpers\helpers.py -> build\bdist.win32\egg\cli\helpers
copying build\lib\cli\helpers\__init__.py -> build\bdist.win32\egg\cli\helpers
copying build\lib\cli\__init__.py -> build\bdist.win32\egg\cli
byte-compiling build\bdist.win32\egg\cli\cli.py to cli.cpython-38.pyc
byte-compiling build\bdist.win32\egg\cli\helpers\helpers.py to helpers.cpython-38.pyc
byte-compiling build\bdist.win32\egg\cli\helpers\__init__.py to __init__.cpython-38.pyc
byte-compiling build\bdist.win32\egg\cli\__init__.py to __init__.cpython-38.pyc
creating build\bdist.win32\egg\EGG-INFO
copying console_example.egg-info\PKG-INFO -> build\bdist.win32\egg\EGG-INFO
copying console_example.egg-info\SOURCES.txt -> build\bdist.win32\egg\EGG-INFO
copying console_example.egg-info\dependency_links.txt -> build\bdist.win32\egg\EGG-INFO
copying console_example.egg-info\entry_points.txt -> build\bdist.win32\egg\EGG-INFO
copying console_example.egg-info\requires.txt -> build\bdist.win32\egg\EGG-INFO
copying console_example.egg-info\top_level.txt -> build\bdist.win32\egg\EGG-INFO
zip_safe flag not set; analyzing archive contents...
creating 'dist\console_example-1.0-py3.8.egg' and adding 'build\bdist.win32\egg' to it
removing 'build\bdist.win32\egg' (and everything under it)
Processing console_example-1.0-py3.8.egg
Removing c:\users\admin\appdata\local\programs\python\python38-32\lib\site-packages\console_example-1.0-py3.8.egg
Copying console_example-1.0-py3.8.egg to c:\users\admin\appdata\local\programs\python\python38-32\lib\site-packages
console-example 1.0 is already the active version in easy-install.pth
Installing console_example-script.py script to scripts
Installing console_example.exe script to scripts
Installing console_example.exe.manifest script to scripts

Installed c:\users\admin\appdata\local\programs\python\python38-32\lib\site-packages\console_example-1.0-py3.8.egg
Processing dependencies for console-example==1.0
Searching for click==8.0.0a1
Best match: click 8.0.0a1
Processing click-8.0.0a1-py3.8.egg
click 8.0.0a1 is already the active version in easy-install.pth

Using c:\users\admin\appdata\local\programs\python\python38-32\lib\site-packages\click-8.0.0a1-py3.8.egg
Finished processing dependencies for console-example==1.0
```

</details>

После этого в директорию scripts будут установлены наши скрипты для запуска:

```
C:\Programs\tmp\PythonSetupExample\console_example>cd scripts

C:\Programs\tmp\PythonSetupExample\console_example\scripts>dir
 Том в устройстве C имеет метку Windows10
 Серийный номер тома: DCBB-BB21

 Содержимое папки C:\Programs\tmp\PythonSetupExample\console_example\scripts

29.11.2020  19:41    <DIR>          .
29.11.2020  19:41    <DIR>          ..
29.11.2020  19:41               479 console_example-script.py
29.11.2020  19:41            65 536 console_example.exe
29.11.2020  19:41               650 console_example.exe.manifest
               3 файлов         66 665 байт
               2 папок  728 631 013 376 байт свободно

```

Как видно в отличие от `unix` было создано три файла.

Файл `.manifest` содержит какую-то информацию о скрипте, в целом нам этот файл не интересен:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity version="1.0.0.0"
                      processorArchitecture="X86"
                      name="console_example"
                      type="win32"/>
    <!-- Identify the application security requirements. -->
    <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
        <security>
            <requestedPrivileges>
                <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
            </requestedPrivileges>
        </security>
    </trustInfo>
</assembly>
```

Файл `.py`, который содержит знакомый нам код для запуска:

```python
#!C:\Users\admin\AppData\Local\Programs\Python\Python38-32\python.exe
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

И `.exe` файл для запуска.

Наше приложение можно запустить двумя способами:

1. При помощи `.exe` файла:

```
C:\Programs\tmp\PythonSetupExample\console_example\scripts>console_example.exe
Usage: console_example [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  sort  Sort numbers.
  sum   Sum numbers.

C:\Programs\tmp\PythonSetupExample\console_example\scripts>console_example.exe sum 3 1 2
6

C:\Programs\tmp\PythonSetupExample\console_example\scripts>console_example.exe sort 3 1 2
1 2 3

C:\Programs\tmp\PythonSetupExample\console_example\scripts>console_example.exe sort 3 1 2 --reverse
3 2 1
```

2. При помощи `.py` файла с явным указанием `python` для запуска:

```
C:\Programs\tmp\PythonSetupExample\console_example\scripts>python console_example-script.py
Usage: console_example [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  sort  Sort numbers.
  sum   Sum numbers.

C:\Programs\tmp\PythonSetupExample\console_example\scripts>python console_example-script.py sum 3 1 2
6

C:\Programs\tmp\PythonSetupExample\console_example\scripts>python console_example-script.py sort 3 1 2
1 2 3

C:\Programs\tmp\PythonSetupExample\console_example\scripts>python console_example-script.py sort 3 1 2 --reverse
3 2 1
```

Все эти скрипты можно попытаться запустить из проводника, но, к сожалению, единственное, что вы увидете, будет быстро мелькнувшая консоль.

![windows_file_explorer_console_example](https://github.com/chegoryu/PythonSetupExample/blob/master/readme_images/windows_file_explorer_console_example.png)

Но, к счачтью, совсем по другому обстоят дела с GUI приложением: там при установке появляются следующие файлы:

```
C:\Programs\tmp\PythonSetupExample\gui_example\scripts>dir
 Том в устройстве C имеет метку Windows10
 Серийный номер тома: DCBB-BB21

 Содержимое папки C:\Programs\tmp\PythonSetupExample\gui_example\scripts

29.11.2020  20:29    <DIR>          .
29.11.2020  20:29    <DIR>          ..
29.11.2020  20:29               451 chardetect-script.py
29.11.2020  20:29            65 536 chardetect.exe
29.11.2020  20:29               645 chardetect.exe.manifest
29.11.2020  20:29               230 garden
29.11.2020  20:29                25 garden.bat
29.11.2020  20:29               452 gui_example-script.pyw
29.11.2020  20:29            65 536 gui_example.exe
29.11.2020  20:29               646 gui_example.exe.manifest
29.11.2020  20:29               454 pygmentize-script.py
29.11.2020  20:29            65 536 pygmentize.exe
29.11.2020  20:29               645 pygmentize.exe.manifest
29.11.2020  20:29               244 pywin32_postinstall.py
29.11.2020  20:29               236 pywin32_testall.py
29.11.2020  20:29               228 rst2html.py
29.11.2020  20:29               230 rst2html4.py
29.11.2020  20:29               230 rst2html5.py
29.11.2020  20:29               230 rst2latex.py
29.11.2020  20:29               226 rst2man.py
29.11.2020  20:29               226 rst2odt.py
29.11.2020  20:29               248 rst2odt_prepstyles.py
29.11.2020  20:29               238 rst2pseudoxml.py
29.11.2020  20:29               224 rst2s5.py
29.11.2020  20:29               230 rst2xetex.py
29.11.2020  20:29               226 rst2xml.py
29.11.2020  20:29               234 rstpep2html.py
              25 файлов        203 406 байт
               2 папок  727 629 459 456 байт свободно

```

Если не учитывать файлы который появились из-за зависимости от `kivy`, то нас интересуют:

```
29.11.2020  20:29               452 gui_example-script.pyw
29.11.2020  20:29            65 536 gui_example.exe
29.11.2020  20:29               646 gui_example.exe.manifest
```

Как можно заметить основное отличие - это `.pyw` вместо `.py`. Это специальное расширение файла, которое означает запуск `python` скрипта без открытия консоли (играет роль только при запуске из проводника, при запуске из консоли сама консоль будет оставаться на месте).

При запуске из консоли в ней будет лог:

```
C:\Programs\tmp\PythonSetupExample\gui_example\scripts>python gui_example-script.pyw
[INFO   ] [Logger      ] Record log in C:\Users\admin\.kivy\logs\kivy_20-11-29_3.txt
[INFO   ] [deps        ] Successfully imported "kivy_deps.gstreamer" 0.3.1
[INFO   ] [deps        ] Successfully imported "kivy_deps.sdl2" 0.3.1
[INFO   ] [deps        ] Successfully imported "kivy_deps.glew" 0.3.0
[INFO   ] [deps        ] Successfully imported "kivy_deps.angle" 0.3.0
[INFO   ] [Kivy        ] v2.0.0rc4, git-d74461b, 20201015
[INFO   ] [Kivy        ] Installed at "c:\users\admin\appdata\local\programs\python\python37-32\lib\site-packages\kivy-2.0.0rc4-py3.7-win32.egg\kivy\__init__.py"
[INFO   ] [Python      ] v3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:01:55) [MSC v.1900 32 bit (Intel)]
[INFO   ] [Python      ] Interpreter at "C:\Users\admin\AppData\Local\Programs\Python\Python37-32\python.exe"
[INFO   ] [Factory     ] 186 symbols loaded
[INFO   ] [Image       ] Providers: img_tex, img_dds, img_sdl2 (img_pil, img_ffpyplayer ignored)
[INFO   ] [Text        ] Provider: sdl2
[INFO   ] [Window      ] Provider: sdl2
[INFO   ] [GL          ] Using the "OpenGL" graphics system
[INFO   ] [GL          ] GLEW initialization succeeded
[INFO   ] [GL          ] Backend used <glew>
[INFO   ] [GL          ] OpenGL version <b'4.6.0 NVIDIA 452.06'>
[INFO   ] [GL          ] OpenGL vendor <b'NVIDIA Corporation'>
[INFO   ] [GL          ] OpenGL renderer <b'GeForce RTX 2070 SUPER/PCIe/SSE2'>
[INFO   ] [GL          ] OpenGL parsed version: 4, 6
[INFO   ] [GL          ] Shading version <b'4.60 NVIDIA'>
[INFO   ] [GL          ] Texture max size <32768>
[INFO   ] [GL          ] Texture max units <32>
[INFO   ] [Window      ] auto add sdl2 input provider
[INFO   ] [Window      ] virtual keyboard not allowed, single mode, not docked
[INFO   ] [Base        ] Start application main loop
[INFO   ] [GL          ] NPOT texture support is available
[INFO   ] [Base        ] Leaving application in progress...
```

![windows_gui_example](https://github.com/chegoryu/PythonSetupExample/blob/master/readme_images/windows_gui_example.png)

Также можно запустить при помощи `.exe` или `.pyw` файла из проводника (возможно при выборе `.pyw` нужно будет указать, что надо запустить именно при помощи `python`, в моем случае по дефолту открылась `IDLE`, пришлось изменять способ запуска):

![windows_file_explorer_gui_example](https://github.com/chegoryu/PythonSetupExample/blob/master/readme_images/windows_file_explorer_gui_example.png)

## Как правильно распространять приложения

При написании приложения мало его только написать, ещё нужно написать документацию которая описывает:

1. Для чего слелано это приложение
2. Какие есть ограничения при его использовании (например, запускается только под `linux`)
3. Как правильно установить приложение (или проинициализировать окружение)
4. Как правильно запускать

Может быть эти пункты кажутся вам очевидными, но, к сожалению, это не так.
Иногда очень сложно разбираться в коде (даже в коде `setup.py`), чтобы понять как установить приложение. А как его правильно запускать обычно вообще невозможно понять.

Например, если ваше приложение использует то, что все скрипты для запуска лежат в `scripts`, тогда человек установивший скрипты в `/usr/local/bin`
не будет понимать почему у него ничего не работает. Может быть человек в какой-то момент догадается об этом, но потом окажется что перед первым запуском `./scripts/app` надо что-то
проинициализировать при помощи `./scripts/app --init`

Не надо никого заставлять гадать как это сделать, надо просто написать как можно более подробное описание всего процесса настройки и запуска, а также набор ограничений при работе.
