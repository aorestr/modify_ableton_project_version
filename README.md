# MODIFY ABLETON PROJECT VERSION

Script that modifies the version of an **Ableton** project. Useful when trying to work
with a project in a newer version than yours.

````
usage: main.py [-h] [--xml] als_file ableton_version_to_set

Script to change an Ableton project version

positional arguments:
  als_file              Relative or absolute path to Ableton project '.als' file.It's been tested only with Ableton 10.0.5 and 11.2.11 projects.
  ableton_version_to_set
                        Version of Ableton that you would like the '.als' file to be set.

options:
  -h, --help            show this help message and exit
  --xml                 If set, it does not remove the .xml file from the '.als' once created.
````

It's been tested with:
* **Ableton 10.0.5**/**Ableton 11.2.11**
* **Python 3.10.0**