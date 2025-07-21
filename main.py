from config import CONFIG
from src.gather_data import gather_data
from src.pair_selection import pair_selection
from src.pair_data import pair_data
from src.strategy import strategy
from src.performance_metrics import performance_metrics
from src.plot_portfolio import plot_portfolio

def main():
    start_date = CONFIG['start_date']
    end_date = CONFIG['end_date']
    universe = CONFIG['universe']

    close_prices = gather_data(universe = universe, start_date = start_date, end_date = end_date)
    cointegrated_pairs = pair_selection(universe = universe, close_prices = close_prices)
    z_score_df, hedge_ratio_dict = pair_data(cointegrated_pairs = cointegrated_pairs, close_prices = close_prices)
    portfolio_values = strategy(cointegrated_pairs = cointegrated_pairs, zscores = z_score_df, hedge_ratios = hedge_ratio_dict, close_prices = close_prices)
    cumulative_return, volatility, sharpe_ratio, max_drawdown, sortino_ratio, max_values, CAGR = performance_metrics(portfolio_values = portfolio_values)
    plot_portfolio(portfolio_values = portfolio_values, highest_values = max_values)

    print('REPORT:')
    print(f"Cumulative Return: {round(cumulative_return * 100, 2)}%")
    print(f"CAGR: {round(CAGR * 100, 2)}%")
    print(f"Volatility: {round(volatility * 100, 2)}%")
    print(f"Max Drawdown: {round(max_drawdown * 100, 2)}%")
    print(f"Sharpe Ratio: {round(sharpe_ratio, 2)}")
    print(f"Sortino Ratio: {round(sortino_ratio, 2)}")


if __name__ == '__main__':
    main()