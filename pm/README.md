# Packages 

Project-modules go in here. 

## To folder or not to folder 

Reference: [Python Packages](https://python.land/project-structure/python-packages)

Currently, all modules are defined as files:

```txt
pm
├── __init__.py
├── core.py
├── cryptography.py
├── storage.py
└── ui.py
```

If the project gets complex enough, we can turn them into sub-packages instead: 

```txt
pm
├── __init__.py
├── core
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── cryptography
...
```

## Contents 

| Name | Desc | 
---|---
`__init__.py` | See [Regular packages](https://docs.python.org/3/reference/import.html#regular-packages)
`core.py` | Core module
`cryptography.py` | Handles cryptographic functions 
`storage.py` | Handles database interactions 
`ui.py` | Provides UI stuff
