from models.options import OptionsResult, PutOption

MAX_LENGTH = 1900


def _put_rows(puts: list[PutOption]) -> str:
    if not puts:
        return "  No contracts found in this range.\n"
    header = f"  {'Strike':>8}  {'Expiry':<12}  {'Bid':>6}  {'Ask':>6}  {'Mid':>6}  {'Delta':>6}  {'IV':>6}\n"
    divider = "  " + "-" * 62 + "\n"
    rows = ""
    for p in puts:
        delta_str = f"{p.delta:+.3f}" if p.delta is not None else "   N/A"
        iv_str = f"{p.iv * 100:.1f}%" if p.iv is not None else "  N/A"
        rows += (
            f"  {p.strike:>8.2f}  {str(p.expiry):<12}  "
            f"{p.bid:>6.2f}  {p.ask:>6.2f}  {p.midpoint:>6.3f}  "
            f"{delta_str:>6}  {iv_str:>6}\n"
        )
    return header + divider + rows


def format_result(result: OptionsResult) -> str:
    if result.error:
        return f"❌ **{result.ticker}** — Error: {result.error}"

    low = result.current_price * 0.70
    high = result.current_price * 0.80

    msg = (
        f"**{result.ticker}** @ ${result.current_price:.2f}  "
        f"_(strikes ${low:.0f}–${high:.0f})_\n\n"
        f"**Current Week:**\n"
        f"```\n{_put_rows(result.current_week)}```\n"
        f"**Next Week:**\n"
        f"```\n{_put_rows(result.next_week)}```"
    )

    if len(msg) > MAX_LENGTH:
        msg = msg[:MAX_LENGTH] + "\n_... truncated_"

    return msg
