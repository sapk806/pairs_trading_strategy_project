def pair_selection(universe, close_prices):
    """
    Finds the Pearson correlation coefficient for each pair and uses the result to filter pairs for cointegration tests.

    Parameters:
        universe (list of str): A list of ticker symbols. 
        close_prices (pd.DataFrame): A DataFrame containing each asset from the universe and their close prices, indexed by date

    Returns:
        list of tuples: A list of tuples containing the cointegrated combinations.
    """
    from itertools import combinations
    import pandas as pd
    from statsmodels.tsa.stattools import coint

    combinations_list = list(combinations(universe, 2))
    
    correlated_pairs = {}
    for combination in combinations_list:
        assetA = combination[0]
        assetB = combination[1]

        assetA_close_price = close_prices[assetA]
        assetB_close_price = close_prices[assetB]

        correlation = assetA_close_price.corr(assetB_close_price)
        if correlation >=0.89:
            correlated_pairs[combination] = correlation

    cointegrated_pairs = []
    for combination in correlated_pairs:
        assetA = combination[0]
        assetB = combination[1]

        assetA_close_price = close_prices[assetA]
        assetB_close_price = close_prices[assetB]

        pvalue = coint(assetA_close_price, assetB_close_price)[1]
        if pvalue <= 0.05:
            cointegrated_pairs.append((assetA, assetB))
    
    cointegrated_pairs_df = pd.DataFrame(cointegrated_pairs, columns = ['Asset A', 'Asset B'])
    cointegrated_pairs_df.to_csv('results/cointegrated_pairs.csv')
    
    return cointegrated_pairs
    

