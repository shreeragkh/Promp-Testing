MODEL = "claude-haiku-4-5-20251001"  # fast + cheap for experiments

CUSTOM_CSS = """
<style>
.score-box {
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: 500;
    display: inline-block;
    margin: 4px 4px 4px 0;
}
.score-high  { background: #d4edda; color: #155724; }
.score-mid   { background: #fff3cd; color: #856404; }
.score-low   { background: #f8d7da; color: #721c24; }
.strategy-tag {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #6c757d;
    margin-bottom: 4px;
}
.winner-banner {
    background: #d4edda;
    color: #155724;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: 500;
    font-size: 14px;
    margin-top: 12px;
}
</style>
"""
