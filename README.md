# Password manager

Capstone project.

Name to be changed soon. 

## Team 

- Nguyen Le
- Enrico Jan Salapong 
- Austin Kim
- Brock Gieszl 

## Project structure

Reference: [Structuring Your Project](https://docs.python-guide.org/writing/structure/#:~:text=Structuring%20Your%20Project%20%C2%B6%201%20Structure%20of%20the,...%2010%20Vendorizing%20Dependencies%20%C2%B6%20More%20items...%20)

```txt
.
├── docs
├── .github
│   └── workflows
│       └── main.yml
├── .gitignore
├── LICENSE
├── pm
│   ├── core.py
│   ├── cryptography.py
│   ├── __init__.py
│   ├── storage.py
│   └── ui.py
├── pm.py
├── README.md
├── requirements.txt
└── tests
    ├── test_core.py
    ├── test_cryptography.py
    ├── test_storage.py
    └── test_ui.py
```

| Name | Type | Desc | 
---|---|---
`docs/` | folder | Contains documentation about packages.
`.github/` | folder | GitHub Actions 
`pm/` | folder | Main package, short for "password manager." Subject to renaming pending decision. 
`pm.py` | file | Entry point. Run this to start the program. Subject to renaming pending decision.
`requirements.txt` | file | Requirements file for *Pip*. Ingested automatically to handle dependencies during CI/CD. 
`tests/` | folder | Test files go here. 

