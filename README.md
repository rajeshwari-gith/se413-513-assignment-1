# Assignment 1 — Course Registration System

Tests for `src/registration.py` (starter code, not modified).

## Setup

```
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install pytest
```

## Run the tests

All tests:

```
pytest
```

Only some tests:

```
pytest -m positive
pytest -m negative
pytest -m boundary
```

## Independent tests

Each test uses its own inputs. Fixtures give every test a new copy of the data,
and the temporary file is deleted after each test.

## Results

All 43 tests pass. See `test_results.txt`.

The analysis is in `ANALYSIS.md`.
