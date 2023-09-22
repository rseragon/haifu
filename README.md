# haifu
Distributed Meta-Package Manager

## Installation
> (Supports Arch(`pyalpm`), Debian(`python-apt`) based distros)

Dependencies(for installation):
`python` >= 3.10
`poetry` >= 1.1

1. Install [python](https://www.python.org/), [poetry](https://python-poetry.org/)
2. clone and setup poetry env
```console
git clone https://github.com/rseragon/haifu && cd haifu/
```
Set up run dependencies
```console
python setup.py
```
```console
poetry install
```
get into poetry environment
```console
poetry shell
```

3. Run program
> The program consists of mainly 2 part i.e. the daemon the the daemon control cli

> To use the features of decentralized aspect of the program, YOU SHOULD KEEP THE DAEMON RUNNING!

In a poetry shell

Start the daemon using
```console
python haifu.py daemon start
```

4. And now you can run the queires and use the application

for eg:
search a package
```console
python haifu.py search zsh
```

Get package info
```console
python haifu.py info zsh
```

Install package 
```console
python haifu.py install zsh
```

Add peer to database list
```console
python haifu.py peer add <peer-ip> <peer-port>
```
