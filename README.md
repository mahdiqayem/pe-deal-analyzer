<div align="center">

# Private Equity Deal Analyzer

**An interactive tool for modeling private equity returns — deal-level analysis, scenario comparison, and sensitivity testing in the browser.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)

[**Live Demo**](#) · [Features](#features) · [Methodology](#methodology) · [Architecture](#architecture) · [Run Locally](#running-locally)

</div>

---

## Overview

Enter a set of deal assumptions — investment size, ownership stake, revenue, margins, growth, exit multiple, holding period — and immediately see the projected investment outcome.

The analyzer calculates **MOIC** and **IRR**, compares **Bear / Base / Bull** scenarios side by side, and maps how returns shift across combinations of growth and exit-multiple assumptions.

> **Screenshot coming soon** — a preview of the running application will be added here.

---

## Features

| | Feature | What it does |
|---|---|---|
| **1** | **Single-deal analysis** | Projects revenue, EBITDA, exit valuation, investor proceeds, MOIC, and IRR from a set of assumptions |
| **2** | **Scenario modeling** | Compares Bear, Base, and Bull cases across different growth rates and exit multiples |
| **3** | **Sensitivity analysis** | Maps MOIC across a grid of growth-rate and exit-multiple combinations, as both a table and a heatmap |
| **4** | **Cash flow visualization** | Charts the investment outflow and exit proceeds across the holding period |

---

## Methodology

### MOIC vs IRR

The analyzer reports both metrics because they answer different questions.

**MOIC (Multiple on Invested Capital)** measures how many times the original investment is returned. A 2.5x MOIC means a \$1 million investment generates \$2.5 million of proceeds.

**IRR (Internal Rate of Return)** measures the annualized return, accounting for the timing of cash flows. This matters because receiving \$2.5 million after two years is materially different from receiving the same amount after seven.

> **MOIC tells you how much you made. IRR tells you how efficiently you made it.**

### Exit Valuation

Exit value is estimated using an EBITDA exit multiple:

```
Exit Value = Exit EBITDA × Exit Multiple
```

Revenue is projected forward at the assumed growth rate, and EBITDA is derived from the assumed margin. The investor's share of the exit is:

```
Investor Proceeds = Exit Value × Ownership Percentage
```

These proceeds, together with the initial investment, form the cash flow series used to calculate MOIC and IRR.

### Bear, Base, and Bull Cases

| Scenario | Growth Rate | Exit Multiple | Represents |
| :------- | ----------: | ------------: | :--------- |
| **Bear** | 5% | 6x | Weaker operating performance and a softer valuation environment |
| **Base** | 15% | 8x | The central set of assumptions |
| **Bull** | 25% | 10x | Stronger company performance and more favorable valuations |

Both assumptions move together by design: investment returns are driven by **how the business performs** *and* **how much buyers are willing to pay for that performance**.

### Sensitivity Analysis

The sensitivity grid shows how MOIC changes across combinations of growth rates and exit multiples — growth rates as rows, exit multiples as columns, with each cell holding the MOIC for that pairing.

Rendered as a heatmap, it makes the shape of the return profile immediately visible: which assumptions move returns most, and where the deal stops being attractive.

---

## Limitations & Assumptions

This tool models a deal as a simplified, all-equity investment. The following are deliberate scope decisions for this version — each is a meaningful driver of returns in real transactions.

<details>
<summary><strong>What this model does not capture</strong></summary>

<br>

* **No leverage.** Private equity buyouts are typically financed partly with debt raised against the target company, and paying that debt down over the holding period is a major contributor to equity returns. This model assumes the investment is funded entirely with equity.
* **No interim cash flows.** Dividends, distributions, and recapitalizations during the holding period are not modeled — all value is assumed to be realized at exit.
* **No fees or carried interest.** Management fees, carry, and transaction costs are excluded, so returns are gross rather than net to a limited partner.
* **Constant operating assumptions.** Revenue growth and EBITDA margin are held flat across the holding period rather than varying year by year.
* **Single exit event.** One clean exit at the end of the holding period, at the specified EBITDA multiple.

</details>

**Planned for v2:** a debt schedule with interest and amortization, year-by-year operating assumptions, and a fee/carry layer to produce net returns.

---

## Architecture

The project separates the **calculation engine** from the **user interface**.

```
pe-deal-analyzer/
├── pe_engine.py        # Pure calculation functions — no Streamlit imports
├── app.py              # Streamlit UI — inputs, layout, charts
├── tests/
│   └── test_pe_engine.py
├── requirements.txt
└── README.md
```

### `pe_engine.py`

Core financial logic as pure Python functions, with zero Streamlit imports:

`project_revenue` · `project_ebitda` · `exit_valuation` · `investor_proceeds` · `moic` · `irr` · `run_deal` · `run_scenarios` · `sensitivity_analysis`

Because the engine has no dependency on the interface, it can be tested in isolation and reused by any front end — a notebook, a CLI, an API, or a different UI framework entirely.

### `app.py`

The Streamlit layer: user inputs and validation, deal results, scenario comparison, the sensitivity table and heatmap, and all charts. It calls the engine and renders the output — it contains no financial logic of its own.

---

## Tech Stack

| Tool | Role |
| :--- | :--- |
| **Python** | Core language |
| **pandas** | DataFrames and the sensitivity grid |
| **numpy-financial** | IRR calculation |
| **Streamlit** | Interactive web application |
| **Plotly** | Charts and heatmap |
| **pytest** | Automated testing |

---

## Running Locally

**1. Clone the repository**

```bash
git clone https://github.com/mahdiqayem/pe-deal-analyzer.git
cd pe-deal-analyzer
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate
```

<details>
<summary>On Windows</summary>

<br>

```bash
python -m venv venv
venv\Scripts\activate
```

</details>

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the app**

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Testing

```bash
python -m pytest
```

The suite verifies the core financial calculations against hand-computed values, checks that scenario ordering behaves correctly (Bear < Base < Bull), validates the shape and values of the sensitivity grid, confirms that invalid inputs raise rather than fail silently, and checks the cash flow series that drives the visualizations.
