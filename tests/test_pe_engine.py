import pytest
from pe_engine import run_deal, moic, run_scenarios


def test_run_deal_matches_hand_calculation():
    result = run_deal(
        investment=2_000_000,
        ownership_pct=0.20,
        entry_revenue=10_000_000,
        ebitda_margin=0.25,
        growth_rate=0.15,
        exit_multiple=8,
        holding_period=5,
    )
    assert result["exit_ebitda"] == pytest.approx(5_028_393, rel=1e-3)
    assert result["moic"] == pytest.approx(4.02, rel=1e-2)
    assert result["irr"] == pytest.approx(0.321, abs=0.002)
    assert result["exit_value"] == pytest.approx(40_227_144, rel=1e-3)


def test_moic_raises_on_zero_investment():
    with pytest.raises(ValueError):
        moic(proceeds=1000, investment=0)


def test_scenarios_ordered_correctly():
    results = run_scenarios(
        investment=2_000_000,
        ownership_pct=0.20,
        entry_revenue=10_000_000,
        ebitda_margin=0.25,
        holding_period=5,
    )
    assert results["bear"]["moic"] < results["base"]["moic"] < results["bull"]["moic"]
    assert results["bear"]["irr"] < results["base"]["irr"] < results["bull"]["irr"]