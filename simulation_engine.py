import numpy as np

def simulate_loop_position(
    initial_capital=100.0,
    ltv_target=0.925,
    days=365,
    supply_apr=0.165,
    borrow_apr_normal=0.12,
    borrow_apr_high=0.21,
    high_periods=None
):
    if high_periods is None:
        high_periods = [(30, 44), (120, 134), (250, 264)]

    leverage = 1 / (1 - ltv_target)
    borrow_multiple = leverage - 1

    def apr_to_daily(apr):
        return (1 + apr) ** (1/365) - 1

    supply_daily = apr_to_daily(supply_apr)
    borrow_daily_normal = apr_to_daily(borrow_apr_normal)
    borrow_daily_high = apr_to_daily(borrow_apr_high)

    supply = initial_capital * leverage
    borrow = initial_capital * borrow_multiple

    net_position = []
    supply_curve = []
    borrow_curve = []

    for day in range(days):
        daily_borrow_rate = borrow_daily_normal
        for start, end in high_periods:
            if start <= day <= end:
                daily_borrow_rate = borrow_daily_high
                break

        supply *= (1 + supply_daily)
        borrow *= (1 + daily_borrow_rate)

        net_position.append(supply - borrow)
        supply_curve.append(supply)
        borrow_curve.append(borrow)

    return (
        np.arange(days),
        np.array(net_position),
        np.array(supply_curve),
        np.array(borrow_curve)
    )
