"""
scoring.py

企業の健康度スコアを算出するための関数群
"""

def normalize_growth_rate(rate_pct: float) -> float:
    """
    売上や従業員増減率などの前年比率を0–100に正規化。
    - rate_pct: % 表記の数字（例: +10.0, -5.0）
    - -20% → 0点, +20% → 100点, 線形補間
    """
    # clamp rate_pct to [-20, +20]
    capped = max(-20.0, min(rate_pct, 20.0))
    # -20→0, +20→100
    score = (capped + 20) * 2.5
    return round(score, 1)


def normalize_profit_margin(margin_pct: float) -> float:
    """
    一人当たり利益や営業利益率などの数値を0–100に正規化。
    - margin_pct: % 表記の数字（例: 15.0）
    - 0%→0点, 20%以上→100点, 線形補間
    """
    capped = max(0.0, min(margin_pct, 20.0))
    score = (capped / 20.0) * 100
    return round(score, 1)


def normalize_text_length(text: str, max_chars: int = 500) -> float:
    """
    Wikipediaの抜粋文字数を0–100に正規化。
    - text: HTMLタグを含まないプレーンテキスト
    - max_chars: 100点とみなす文字数の閾値
    - 0文字→0点, max_chars以上→100点
    """
    length = len(text)
    capped = min(length, max_chars)
    score = (capped / max_chars) * 100
    return round(score, 1)


def compute_overall_score(metrics: dict, weights: dict) -> float:
    """
    各指標と重みから加重平均で全体スコアを算出。
    - metrics: {'growth': 80.0, 'margin': 50.0, 'info': 90.0}
    - weights: {'growth': 0.4, 'margin': 0.4, 'info': 0.2}
    """
    total = 0.0
    wsum = 0.0
    for key, weight in weights.items():
        val = metrics.get(key)
        if val is None:
            continue
        total += val * weight
        wsum += weight
    if wsum == 0:
        return 0.0
    return round(total / wsum, 1)


def rank_from_score(score: float) -> str:
    """
    スコアからランク（A,B,C,D）を返す。
    """
    if score >= 85:
        return 'A'
    if score >= 70:
        return 'B'
    if score >= 50:
        return 'C'
    return 'D'
