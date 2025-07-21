
def strategy(cointegrated_pairs, zscores, hedge_ratios, close_prices):
    """
    Executes the pairs trading strategy using z-scores as entry and exit signals and the price spread to determine share quantities for long and short positions.
    
    Parameters:
        cointegrated_pairs (list of tuples): A list of tuples containing the cointegrated combinations.
        zscores (pd.DataFrame): A DataFrame containing each cointegrated combination and a series of their corresponding z-scores gatheres, indexed by date with combinations as columns.
        hedge_ratios (dict): A dictionary containing each combination as the key and their corresponding hedge ratio, which was found using OLS.
        close_prices (pd.DataFrame): Historical adjusted close price data, indexed by dates with assets as columns.
    
    Returns:
        pd.Series: A series of the value of the portfolio, indexed by date.
    """
    import pandas as pd

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
        units = pair_capital_split/unit_cost

        # sharesA and sharesB represent position sizes
        sharesA = units
        sharesB = hedge_ratio * units

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
                sharesA -= units
                sharesB += hedge_ratio * units
                short_spread = True
                days_in_trade = 0
            
            # Exit short position if abs(z-score) < 0.05 and short position has lasted at least 3 days.
            elif abs(zscore) < 0.05 and short_spread and days_in_trade >= 3:
                sharesA += units
                sharesB -= hedge_ratio * units
                short_spread = False
                days_in_trade = 0

            # Enter long position if z-score < -2 and not currently in a trade.
            elif zscore < -2 and not long_spread and not short_spread:
                sharesA += units
                sharesB -= hedge_ratio * units
                long_spread = True
                days_in_trade = 0
            
            # Exit long position if abs(z-score) < 0.05 and long position lasted at least 3 days.
            elif abs(zscore) < 0.05 and long_spread and days_in_trade >=3:
                sharesA -= units
                sharesB += hedge_ratio * units
                long_spread = False
                days_in_trade = 0
            
            # Exit long position and enter the short position if z-score > 2 and long position has lasted at least 3 days.
            elif zscore > 2 and long_spread and days_in_trade >= 3:
                sharesA -= units
                sharesB += hedge_ratio * units
                long_spread = False

                sharesA -= units
                sharesB += hedge_ratio * units
                short_spread = True
                days_in_trade = 0
            
            # Exit short position and enter the long position if z-score < -2 and long position has lasted at least 3 days.
            elif zscore < -2 and short_spread and days_in_trade >= 3:
                sharesA += units
                sharesB -= hedge_ratio * units
                short_spread = False

                sharesA += units
                sharesB -= hedge_ratio * units 
                long_spread = True
                days_in_trade = 0
                  
            pair_portfolio_value[day] = sharesA * assetA_close_prices.loc[day] + sharesB * assetB_close_prices.loc[day]
        
        pair_portfolio_value_series = pd.Series(pair_portfolio_value)
        pair_value_list.append(pair_portfolio_value_series)
    portfolio_value = sum(pair_value_list)
    portfolio_value.to_csv('results/portfolio_values.csv')
    return portfolio_value