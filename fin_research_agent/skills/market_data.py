import yfinance as ticker_util
import pandas as pd
import json
from typing import List, Dict, Any

def get_stock_stats(symbol: str) -> str:
    """
    Fetches real-time financial statistics for a given stock ticker.
    Args:
        symbol (str): String representing the stock ticker symbol (e.g., 'AAPL', 'NVDA', 'QQQ').
    Returns:
         A JSON string containing current price, P/E ratio, market cap, and price changes.
         e.g., {"symbol": "NVDA", "current_price": 177.82, "price_change_percent": -3.01079, "pe_ratio": 36.21589, "market_cap": 4321915437056, "currency": "USD"}
    """
    try:
        stock = ticker_util.Ticker(symbol)
        info = stock.info
        
        # Extract relevant statistics
        stats = {
            "symbol": symbol,
            "current_price": info.get("currentPrice"),
            #"day_high": info.get("dayHigh"),
            #"day_low": info.get("dayLow"),
            #"price_change": info.get("regularMarketChange"),
            "price_change_percent": info.get("regularMarketChangePercent"),
            "pe_ratio": info.get("trailingPE"),
            #"forward_pe_ratio": info.get("forwardPE"),
            #"eps": info.get("trailingEps"),
            #"forward_eps": info.get("forwardEps"),
            "market_cap": info.get("marketCap"),
            #"fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            #"fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "currency": info.get("currency")
        }        
        return json.dumps(stats)
    except Exception as e:
        return json.dumps({"error": str(e)})
    
def get_sector_performance(tickers: List[str]) -> str:
    """
    Compare the last month performance across multiple stock tickers to identifiy resilience.
    Args:
        tickers (List[str]): A list of stock ticker symbols (e.g., ['AAPL', 'NVDA', 'QQQ']).
    Returns:
        A JSON string with the percentage change for each ticker over the last month.
        e.g., {"AAPL": {"start_price": 274.62, "end_price": 257.46, "change_percent": -6.25}, "NVDA": {"start_price": 190.04, "end_price": 177.82, "change_percent": -6.43}, "QQQ": {"start_price": 614.32, "end_price": 599.75, "change_percent": -2.37}}
    """
    results = {}
    try:
        data = ticker_util.download(tickers, period="1mo", interval="1d", progress=False)

        if data.empty:
            return json.dumps({t: {"error": "No data available"} for t in tickers})

        close_prices = data['Close']  # MultiIndex DataFrame: one column per ticker

        # Normalize: if a single ticker was passed, squeeze to a DataFrame with ticker as column name
        if isinstance(close_prices, pd.Series):
            close_prices = close_prices.to_frame(name=tickers[0])

        for symbol in tickers:
            if symbol not in close_prices.columns:
                results[symbol] = {"error": "Ticker not found"}
                continue

            prices = close_prices[symbol].dropna()

            if len(prices) < 2:
                results[symbol] = {"error": "Insufficient data"}
                continue

            start_price = float(prices.iloc[0])
            end_price = float(prices.iloc[-1])
            change_percent = ((end_price - start_price) / start_price) * 100

            results[symbol] = {
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "change_percent": round(change_percent, 2)
            }

    except Exception as e:
        return json.dumps({"error": str(e)})

    return json.dumps(results)
    
