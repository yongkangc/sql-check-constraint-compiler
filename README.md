# sql-check-constraint-compiler

SQL Check Constraint Compiler

## Running the Application

```bash
python main.py
```

### CLI Commands

```bash
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.
  --translate TEXT  Translate existing CHECK constraints into triggers and
                    stored functions.
  --test_performance TEXT  Run performance tests on the translated constraints.

```

## Setup

1. Create Virtual Environment

```bash
python3 -m venv venv
```

2. Activating Virtual Environment

On Windows:

```bash

.\venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

3. Installing Dependencies

```bash
pip install -r requirements.txt
```

## Project Structure

```markdown
pgCheck/
├── pgcheck/
│ ├── **init**.py
│ ├── cli.py
│ ├── connection.py
│ ├── translator.py
│ ├── performance.py
│ ├── lexer.py
│ ├── parser.py
│ ├── utils.py
│ └── types.py
├── tests/
│ ├── **init**.py
│ ├── test_cli.py
│ ├── test_connection.py
│ ├── test_translator.py
│ ├── test_performance.py
│ ├── test_lexer.py
│ └── test_parser.py
├── data/
│ └── sample_queries.sql
├── .env
├── requirements.txt
└── main.py
```

- pgcheck/ - The main package for the application.
- tests/ - Contains all unit tests.
- data/ - Sample data or SQL queries for testing and benchmarking.
- .env - Environment variables for database connection or other configurations.
- requirements.txt - All the project dependencies.
- main.py - The entry point of the application that invokes the CLI.

## Dependencies

- Typer: For CLI
