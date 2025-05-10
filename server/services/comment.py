# server/services/comment.py

from typing import Dict

async def make_comment(
    company: str,
    score: float,
    rank: str,
    breakdown: Dict[str, float],
    context: str
) -> str:
    """
    Generate a comment string for the company profile, combining score, rank,
    breakdown of metrics, and qualitative context.
    """
    lines = [
        f"会社名: {company}",
        f"総合スコア: {score} ({rank}ランク)",
        f"内訳 — 成長率: {breakdown.get('growth', 0.0):.1f}, "
        f"利益率: {breakdown.get('profit', breakdown.get('margin', 0.0)):.1f}, "
        f"情報充実度: {breakdown.get('info', 0.0):.1f}",
        "",
        "【背景情報】",
        context or "情報が取得できませんでした。"
    ]
    return "\n".join(lines)
