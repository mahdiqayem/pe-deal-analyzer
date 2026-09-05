import numpy_financial as npf
npf.irr([-2_000_000, 0, 0, 0, 0, 8_045_429])

# pe_engine.py — pure functions, no Streamlit imports

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
        "irr": irr(cash_flows)
    }