def plot_portfolio(portfolio_values, highest_values):
    """
    Creates a plot of the value of the portfolio vs. date, with the max drawdown shaded between the current price and the maximum when current price is lower than the maximum.

    Paramters:
        portfolio_value (pd.Series): A series containing the value of the portfolio, indexed by date.
        highest_values (pd.Series): pd.Series: A series containing the highest value at each index, which is by date.

    Return:
        None
    """

    import matplotlib.pyplot as plt

    plt.figure(figsize = (12, 6))
    plt.plot(portfolio_values.index, portfolio_values, label = 'Portfolio Values')
    plt.fill_between(portfolio_values.index, highest_values, portfolio_values, where = portfolio_values < highest_values, color = 'red', alpha = 0.2, label = 'Drawdowns')
    
    plt.grid(True)
    plt.legend()
    
    plt.xlabel('Date')
    plt.ylabel('Portfolio Values ($)')
    plt.title('Portfolio Values with Drawdowns')

    plt.savefig("plots/portfolio_plot.png", dpi=300, bbox_inches='tight')

    plt.show()


