"""
Formatters Utility Module

Provides reusable formatting functions for output display.
"""

from typing import Union


def format_bytes(bytes_value: Union[int, float], precision: int = 2) -> str:
    """
    Format bytes into human-readable format.
    
    Args:
        bytes_value: Size in bytes
        precision: Decimal precision
        
    Returns:
        Formatted string (e.g., "1.50 GB")
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    size = float(bytes_value)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.{precision}f} {units[unit_index]}"


def format_cost(cost: Union[int, float], currency: str = "USD") -> str:
    """
    Format cost value for display.
    
    Args:
        cost: Cost value
        currency: Currency code
        
    Returns:
        Formatted cost string (e.g., "$12.50 USD")
    """
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥'
    }
    
    symbol = symbols.get(currency, currency + ' ')
    return f"{symbol}{cost:.2f}"


def format_percentage(value: Union[int, float], precision: int = 2) -> str:
    """
    Format percentage value.
    
    Args:
        value: Percentage value
        precision: Decimal precision
        
    Returns:
        Formatted percentage string (e.g., "25.50%")
    """
    return f"{value:.{precision}f}%"


def format_duration(days: int) -> str:
    """
    Format duration in days to human-readable format.
    
    Args:
        days: Number of days
        
    Returns:
        Formatted duration string
    """
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''}"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''}"
    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months != 1 else ''}"
    else:
        years = days // 365
        return f"{years} year{'s' if years != 1 else ''}"
