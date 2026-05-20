# Risk Analysis Project

This project converts the original `chp_1.ipynb` notebook into a reusable Python application. It contains two analyses:

- Risk-return portfolio simulation with a Plotly best-fit visualization.
- Adverse-selection insurance model with Matplotlib supply and demand curves.

The code is organized for Git-based development with reusable modules, configuration classes, tests, and a command-line entry point.

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
│   └── risk_analysis
│       ├── __init__.py
│       ├── adverse_selection.py
│       ├── risk_return.py
│       └── visualization.py
└── tests
    ├── __init__.py
    ├── test_adverse_selection.py
    └── test_risk_return.py
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

From the project root, run:

```bash
python -m src.main
```

The application writes visual outputs to the `outputs/` directory:

- `outputs/risk_return.html`
- `outputs/adverse_selection.png`

## Run Tests

```bash
pytest
```

## Configuration

Default parameters live in `src/config/settings.py`. Adjust `RiskReturnConfig` and `AdverseSelectionConfig` to change portfolio size, simulation counts, random seeds, population size, insurance loss costs, and model assumptions.
