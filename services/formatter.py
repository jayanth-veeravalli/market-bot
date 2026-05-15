from models.options import OptionsResult, PutOption

MAX_ROWS_PER_MSG = 15

TABLE_HEADER = (
    f"{'Stk':>6} {'Bid':>5} {'Ask':>5} {'Mid':>5} {'Lst':>5} {'Dlt':>5} {'IV':>4}\n"
    f"{'─' * 41}\n"
)


def _format_row(p: PutOption) -> str:
    delta_str = f"{p.delta:+.2f}" if p.delta is not None else "  N/A"
    iv_str = f"{p.iv * 100:.1f}%" if p.iv is not None else " N/A"
    last_str = f"{p.last_price:.2f}" if p.last_price is not None else "  N/A"
    return (
        f"{p.strike:>6.2f} {p.bid:>5.2f} {p.ask:>5.2f} {p.midpoint:>5.2f} "
        f"{last_str:>5} {delta_str:>5} {iv_str:>4}\n"
    )


def _table_messages(label: str, puts: list[PutOption]) -> list[str]:
    if not puts:
        return [f"**{label}**\n```\nNo contracts found in this range.\n```"]

    messages = []
    for i in range(0, len(puts), MAX_ROWS_PER_MSG):
        chunk = puts[i:i + MAX_ROWS_PER_MSG]
        part = i // MAX_ROWS_PER_MSG + 1
        total = (len(puts) + MAX_ROWS_PER_MSG - 1) // MAX_ROWS_PER_MSG
        title = label if total == 1 else f"{label} (part {part}/{total})"
        rows = "".join(_format_row(p) for p in chunk)
        messages.append(f"**{title}**\n```\n{TABLE_HEADER}{rows}```")

    return messages


def format_result(result: OptionsResult) -> list[str]:
    if result.error:
        return [f"❌ **{result.ticker}** — Error: {result.error}"]

    low = result.current_price * 0.70
    high = result.current_price * 0.80
    header = (
        f"**{result.ticker}** @ ${result.current_price:.2f}  "
        f"_(strikes ${low:.0f}–${high:.0f})_"
    )

    messages = [header]
    messages += _table_messages(f"{result.ticker} — Current Week", result.current_week)
    messages += _table_messages(f"{result.ticker} — Next Week", result.next_week)
    return messages
