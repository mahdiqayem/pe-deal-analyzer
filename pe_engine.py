# pe_engine.py — pure functions, no Streamlit imports

import numpy_financial as npf
import pandas as pd

def project_revenue(entry_revenue, growth_rate, years):
    revenues = [entry_revenue]
    for year in range(1, years + 1):
        revenues.append(revenues[-1] * (1 + growth_rate))
    return revenues

def project_ebitda(revenues, ebitda_margin):
    ebitda_list = []
    for revenue in revenues:
        ebitda_list.append(revenue * ebitda_margin)
    return ebitda_list

def exit_valuation(exit_ebitda, exit_multiple) -> float:
    """Exit value = EBITDA * multiple."""
    return exit_ebitda * exit_multiple

def investor_proceeds(exit_value, ownership_pct) -> float:
    return exit_value * ownership_pct

def moic(proceeds, investment):
    if investment == 0:
        raise ValueError("Investment must be greater than zero.")
    return proceeds / investment

def irr(cash_flows: list[float]) -> float:
    return npf.irr(cash_flows)                

def run_deal(investment, ownership_pct, entry_revenue, ebitda_margin,
             growth_rate, exit_multiple, holding_period) -> dict:
    revenues = project_revenue(entry_revenue, growth_rate, holding_period)
    ebitda_list = project_ebitda(revenues, ebitda_margin)
    exit_ebitda = ebitda_list[-1]
    exit_value = exit_valuation(exit_ebitda, exit_multiple)
    proceeds = investor_proceeds(exit_value, ownership_pct)
    cash_flows = [-investment] + [0] * (holding_period - 1) + [proceeds]
    return {
        "revenues": revenues,
        "ebitda": ebitda_list,
        "exit_ebitda": exit_ebitda,
        "exit_value": exit_value,
        "proceeds": proceeds,
        "moic": moic(proceeds, investment),
        "irr": irr(cash_flows),
        "cash_flows": cash_flows,
    }

SCENARIOS = {
    "bear": {"growth_rate": 0.05, "exit_multiple": 6},
    "base": {"growth_rate": 0.15, "exit_multiple": 8},
    "bull": {"growth_rate": 0.25, "exit_multiple": 10},
}

def run_scenarios(investment, ownership_pct, entry_revenue, ebitda_margin, holding_period):
    results = {}
    for scenario, assumptions in SCENARIOS.items():
        results[scenario] = run_deal(
            investment=investment,
            ownership_pct=ownership_pct,
            entry_revenue=entry_revenue,
            ebitda_margin=ebitda_margin,
            growth_rate=assumptions["growth_rate"],
            exit_multiple=assumptions["exit_multiple"],
            holding_period=holding_period,
        )
    return results


def sensitivity_analysis(investment, ownership_pct, entry_revenue, ebitda_margin,
                          holding_period, growth_rates, exit_multiples, metric="moic"):
    grid = pd.DataFrame(index=growth_rates, columns=exit_multiples, dtype=float)
    for growth_rate in growth_rates:
        for exit_multiple in exit_multiples:
            result = run_deal(
                investment=investment,
                ownership_pct=ownership_pct,
                entry_revenue=entry_revenue,
                ebitda_margin=ebitda_margin,
                growth_rate=growth_rate,
                exit_multiple=exit_multiple,
                holding_period=holding_period
            )
            grid.loc[growth_rate, exit_multiple] = result[metric]
    return grid