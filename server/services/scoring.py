from typing import Dict, Tuple

# weight presets
PRESETS = {
    'default': {'growth': 0.4, 'profit': 0.4, 'info': 0.2},
}

def normalize(value: float, min_val: float, max_val: float) -> float:
    return max(0.0, min(100.0, (value - min_val) / (max_val - min_val) * 100))

def compute_score(official: dict, preset: str) -> Tuple[float, Dict[str, float]]:
    """
    official: JSON from fetch_official()
    preset: key into PRESETS
    """
    data = official['GET_STATS_DATA']['STATISTICAL_DATA']['RESULTS_OVER_TIME']['TIME_PERIOD']
    # Assume last two entries are [ ..., prev, latest ]
    prev, latest = data[-2], data[-1]

    # parse values (strings → floats)
    sales_prev = float(prev['C1'])
    sales_latest = float(latest['C1'])
    profit_latest = float(latest['C2'])
    info_score = float(latest.get('C3', 1.0))  # default to 1.0 if missing

    # compute growth rate (%)
    growth_rate_pct = (sales_latest - sales_prev) / sales_prev * 100

    # normalize each metric to 0–100
    growth_norm = normalize(growth_rate_pct, -50, 50)      # allow -50% to +50%
    profit_norm = normalize(profit_latest * 100, 0, 30)    # profit margin from 0–30%
    info_norm = normalize(info_score * 100, 0, 100)        # completeness 0–1 → 0–100

    weights = PRESETS.get(preset, PRESETS['default'])
    total = (
        growth_norm * weights['growth'] +
        profit_norm * weights['profit'] +
        info_norm * weights['info']
    )
    return round(total, 1), {
        'growth': round(growth_norm, 1),
        'profit': round(profit_norm, 1),
        'info': round(info_norm, 1),
    }

def rank_from_score(score: float) -> str:
    if score >= 80:
        return 'S'
    if score >= 60:
        return 'A'
    if score >= 40:
        return 'B'
    if score >= 20:
        return 'C'
    return 'D'
