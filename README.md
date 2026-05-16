# testing_login
# Selenium Python Automation Framework

## Tech Stack

- Python
- Selenium
- Pytest
- Page Object Model (POM)

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Tests

```bash
pytest -v
```

---

## Generate HTML Report

```bash
pytest --html=report.html
```

---

## Project Structure

- pages/ -> Page Object classes
- tests/ -> Test cases
- utils/ -> Utilities and configuration

---

## Features

- Page Object Model
- Pytest Framework
- Parameterized Testing
- Logging
- ChromeDriver Auto Management
- Scalable Architecture

  selenium-framework/
│
├── pages/
│   └── login_page.py
│
├── tests/
│   └── test_login.py
│
├── utils/
│   ├── driver_factory.py
│   └── config.py
│
├── requirements.txt
├── pytest.ini
└── README.md
