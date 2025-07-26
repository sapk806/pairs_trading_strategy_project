import pandas as pd
import matplotlib.pyplot as plt

def plot_portfolio(portfolio_values: pd.Series, highest_values: pd.Series):
    """
    Plots portfolio value over time, shading drawdowns in red when the portfolio value is less than the running maximum.
    Saves the plot to 'plots/portfolio_plot.png'
    
    Args:
        portfolio_values (pd.Series): Series containing the value of the portfolio, indexed by date.
        highest_values (pd.Series): Series containing the highest value at each index, which is by date.

    Returns:
        None
    """


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


