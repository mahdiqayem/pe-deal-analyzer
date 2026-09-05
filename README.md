# Private Equity Deal Analyzer

A Python-based tool for analyzing private equity deals through deal-level returns, scenario modeling, sensitivity analysis, and cash flow visualization.

## What It Does

The Private Equity Deal Analyzer lets a user enter a set of deal assumptions and immediately see the potential investment returns. It calculates MOIC and IRR, compares Bear/Base/Bull scenarios, and shows how returns change under different growth and exit-multiple assumptions.

## Live Demo

**[Live Demo — coming soon](#)**

## Screenshot

*Screenshot of the running Streamlit application coming soon.*

## Features

* **Single-deal analysis** — Calculate projected revenue, EBITDA, exit valuation, investor proceeds, MOIC, and IRR from a set of assumptions.
* **Scenario modeling** — Compare Bear, Base, and Bull cases with different growth rates and exit multiples.
* **Sensitivity analysis** — Evaluate how MOIC changes across combinations of growth rates and exit multiples, shown as both a table and a heatmap.
* **Cash flow visualization** — Visualize the investment and exit proceeds across the holding period.

## Methodology

### MOIC vs IRR

The analyzer uses both MOIC and IRR because they answer different questions about an investment.

**MOIC (Multiple on Invested Capital)** measures how many times the original investment is returned. A 2.5x MOIC means a $1 million investment generates $2.5 million of proceeds.

**IRR (Internal Rate of Return)** measures the annualized return while taking the timing of cash flows into account. This matters because receiving $2.5 million after two years is materially different from receiving the same amount after seven years.

MOIC tells you how much you made. IRR tells you how efficiently you made it. Using both provides a more complete view of investment performance.

### Exit Valuation

The model estimates the company's exit value using an EBITDA exit multiple:

```
Exit Value = Exit EBITDA × Exit Multiple
```

Revenue is projected forward using the assumed growth rate, and EBITDA is calculated using the assumed EBITDA margin.

The investor's proceeds are then determined by applying their ownership percentage to the exit value:

```
Investor Proceeds = Exit Value × Ownership Percentage
```

These proceeds, together with the initial investment, form the cash flow series used to calculate MOIC and IRR.

### Bear, Base, and Bull Cases

The scenario model varies two assumptions:

| Scenario | Growth Rate | Exit Multiple |
| -------- | ----------: | ------------: |
| **Bear** |          5% |            6x |
| **Base** |         15% |            8x |
| **Bull** |         25% |           10x |

The **Base case** represents the central set of assumptions.

The **Bear case** assumes slower business growth and a lower valuation multiple, representing a weaker operating and market environment.

The **Bull case** assumes stronger growth and a higher valuation multiple, representing stronger company performance and more favorable valuation conditions.

Changing both assumptions together is intentional: investment returns can be affected by both how the business performs and how much buyers are willing to pay for that performance.

### Sensitivity Analysis

The sensitivity grid shows how the deal's MOIC changes across different combinations of growth rates and exit multiples.

Growth rates form the rows, exit multiples form the columns. Each cell represents the MOIC produced by running the deal under that specific combination of assumptions.

The heatmap makes it easier to identify which assumptions have the greatest effect on returns, and where the investment becomes more or less attractive.

## Limitations & Assumptions

This tool models a deal as a simplified, all-equity investment. The following are deliberate scope decisions for this version, not oversights — each one is a meaningful driver of returns in real transactions:

* **No leverage.** Private equity buyouts are typically financed partly with debt raised against the target company, and paying that debt down over the holding period is a major contributor to equity returns. This model assumes the investment is funded entirely with equity.
* **No interim cash flows.** Dividends, distributions, and recapitalizations during the holding period are not modeled. All value is assumed to be realized at exit.
* **No fees or carried interest.** Management fees, carry, and transaction costs are excluded, so returns are gross rather than net to a limited partner.
* **Constant operating assumptions.** Revenue growth and EBITDA margin are held flat across the holding period rather than varying year by year.
* **Single exit event.** The model assumes one clean exit at the end of the holding period, at the specified EBITDA multiple.

A future version would add a debt schedule with interest and amortization, year-by-year operating assumptions, and a fee/carry layer to produce net returns.

## Architecture

The project separates the financial calculation engine from the user interface.

### `pe_engine.py`

Contains the core financial calculations as pure Python functions, with zero Streamlit imports. The engine handles:

* Revenue projections
* EBITDA projections
* Exit valuation
* Investor proceeds
* MOIC
* IRR
* Scenario analysis
* Sensitivity analysis

Keeping these calculations independent from the interface means the engine can be tested and reused independently of Streamlit.

### `app.py`

Contains the Streamlit user interface. It handles:

* User inputs and validation
* Displaying deal results
* Scenario comparison
* Sensitivity table and heatmap
* Charts and visualizations

This separation keeps the project easier to test, maintain, and extend.

## Tech Stack

* **Python**
* **pandas** — DataFrames and sensitivity analysis
* **numpy-financial** — IRR calculation
* **Streamlit** — Interactive web application
* **Plotly** — Data visualization
* **pytest** — Automated testing

## Running Locally

Clone the repository:

```bash
git clone https://github.com/mahdiqayem/pe-deal-analyzer.git
cd pe-deal-analyzer
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Testing

Run the automated test suite with:

```bash
python -m pytest
```

The tests verify the behavior of the core financial calculation functions and the outputs produced by `run_deal()`, including the cash flow series used by the application visualizations.
