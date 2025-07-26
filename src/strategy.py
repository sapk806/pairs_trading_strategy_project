import pandas as pd

def strategy(cointegrated_pairs: list[tuple[str, str]], zscores: pd.DataFrame, hedge_ratios: dict[tuple[str, str], float], close_prices: pd.DataFrame):
    """
    Simulates a pairs trading strategy using z-score thresholds to generate long/short signals and compute daily portfolio value.
    
    Args:
        cointegrated_pairs (list[tuple[str, str]]): A list of tuples containing the cointegrated combinations that pass the correlation and p-value threshold. 
        zscores (pd.DataFrame): A DataFrame where each column corresponds to a cointegrated pair, and contains the z-score time series of their spread.
        hedge_ratios (dict[tuple[str, str], float]): A dictionary where each key corresponds to the cointegrated pair and the value corresponds to their corresponding hedge ratio. Calculated from OLS regression.
        close_prices (pd.DataFrame): Historical adjusted close price data, indexed by dates with assets as columns.
    
    Returns:
        pd.Series: A series of the value of the portfolio, indexed by date.
    """

    capital = 10000
    pair_capital_split = capital/len(cointegrated_pairs)
    pair_value_list = []

    for combination in cointegrated_pairs:
        pair_portfolio_value = {}

        assetA = combination[0]
        assetB = combination[1]
        hedge_ratio = hedge_ratios[combination]

        assetA_close_prices = close_prices[assetA]
        assetB_close_prices = close_prices[assetB]

        # Calculate initial cost of the spread.
        unit_cost = assetA_close_prices.iloc[0] + hedge_ratio * assetB_close_prices.iloc[0]
        unitsA = pair_capital_split/unit_cost

        # sharesA and sharesB represent position sizes
        sharesA = unitsA
        sharesB = hedge_ratio * unitsA

        pair_portfolio_value[close_prices.index[0]] = sharesA * assetA_close_prices.iloc[0] + sharesB * assetB_close_prices.iloc[0]

        short_spread = False
        long_spread = False
        
        days_in_trade = 0
        # Loop through each day and evaluate z-score signals.
        for day in zscores.index[1:]:
            zscore = zscores[combination].loc[day]
            
            if short_spread or long_spread:
                days_in_trade +=1
            
            # Enter short position if z-score > 2 and not currently in a trade.
            if zscore > 2 and not short_spread and not long_spread:
                sharesA -= unitsA
                sharesB += hedge_ratio * unitsA
                short_spread = True
                days_in_trade = 0
            
            # Exit short position if abs(z-score) < 0.05 and short position has lasted at least 3 days.
            elif abs(zscore) < 0.05 and short_spread and days_in_trade >= 3:
                sharesA += unitsA
                sharesB -= hedge_ratio * unitsA
                short_spread = False
                days_in_trade = 0

            # Enter long position if z-score < -2 and not currently in a trade.
            elif zscore < -2 and not long_spread and not short_spread:
                sharesA += unitsA
                sharesB -= hedge_ratio * unitsA
                long_spread = True
                days_in_trade = 0
            
            # Exit long position if abs(z-score) < 0.05 and long position lasted at least 3 days.
            elif abs(zscore) < 0.05 and long_spread and days_in_trade >=3:
                sharesA -= unitsA
                sharesB += hedge_ratio * unitsA
                long_spread = False
                days_in_trade = 0
            
            # Exit long position and enter the short position if z-score > 2 and long position has lasted at least 3 days.
            elif zscore > 2 and long_spread and days_in_trade >= 3:
                sharesA -= unitsA
                sharesB += hedge_ratio * unitsA
                long_spread = False

                sharesA -= unitsA
                sharesB += hedge_ratio * unitsA
                short_spread = True
                days_in_trade = 0
            
            # Exit short position and enter the long position if z-score < -2 and long position has lasted at least 3 days.
            elif zscore < -2 and short_spread and days_in_trade >= 3:
                sharesA += unitsA
                sharesB -= hedge_ratio * unitsA
                short_spread = False

                sharesA += unitsA
                sharesB -= hedge_ratio * unitsA
                long_spread = True
                days_in_trade = 0
                  
            pair_portfolio_value[day] = sharesA * assetA_close_prices.loc[day] + sharesB * assetB_close_prices.loc[day]
        
        pair_portfolio_value_series = pd.Series(pair_portfolio_value)
        pair_value_list.append(pair_portfolio_value_series)
    portfolio_value = sum(pair_value_list)
    portfolio_value.to_csv('results/portfolio_values.csv')
    return portfolio_value