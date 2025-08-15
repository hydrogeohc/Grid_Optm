"""
AIQ Function Registration for Grid Optimization
Registers grid optimization functions for use with NVIDIA AIQ toolkit
"""

import logging
from typing import Any, Dict
from datetime import datetime

from grid_optimization.integrations.aiq_integration import (
    optimize_grid_region,
    get_optimization_status,
    analyze_grid_metrics
)

logger = logging.getLogger(__name__)


async def optimize_grid(region: str = "us-west") -> str:
    """
    Optimize power grid for a specific region.
    
    Args:
        region: Grid region to optimize (us-west, us-east, us-central, pgae)
        
    Returns:
        Formatted string with optimization results
    """
    try:
        result = await optimize_grid_region(region)
        
        if result["status"] == "success":
            return f"""
🔧 Grid Optimization Complete for {region}

✅ Status: {result['status'].title()}
⚡ Loss Reduction: {result.get('loss_reduction', 'N/A')}%
💰 Cost Savings: ${result.get('cost_savings', 'N/A'):,.2f}
⏱️ Optimization Time: {result.get('optimization_time', 'N/A')}
🔄 Next Maintenance: {result.get('next_maintenance', 'Not scheduled')}

Optimal Configuration: {result.get('optimal_config', 'N/A')}
Timestamp: {result['timestamp']}
"""
        else:
            return f"❌ Optimization failed for {region}: {result.get('message', 'Unknown error')}"
            
    except Exception as e:
        logger.error(f"Grid optimization function error: {e}")
        return f"❌ Error optimizing grid for {region}: {str(e)}"


async def show_last_optimization(region: str = "us-west") -> str:
    """
    Show the latest optimization results for a region.
    
    Args:
        region: Grid region to check (us-west, us-east, us-central, pgae)
        
    Returns:
        Formatted string with current status and last optimization data
    """
    try:
        status = await get_optimization_status(region)
        
        if status.get("status") == "error":
            return f"❌ Could not retrieve status for {region}: {status.get('message', 'Unknown error')}"
        
        return f"""
📊 Grid Status for {region}

🟢 Current Status: {status.get('current_status', 'Unknown')}
⚡ Current Load: {status.get('current_load', 'N/A')} MW
🔋 Total Capacity: {status.get('total_capacity', 'N/A')} MW  
📈 Efficiency: {status.get('efficiency', 'N/A')}%
🚨 Active Alerts: {status.get('active_alerts', 0)}

🕐 Last Optimization: {status.get('last_optimization', 'Never')}
📅 Next Scheduled: {status.get('next_scheduled', 'Not scheduled')}
📈 Historical Data Points: {status.get('data_points', 0)}

Updated: {status.get('timestamp', 'N/A')}
"""
        
    except Exception as e:
        logger.error(f"Status check function error: {e}")
        return f"❌ Error checking status for {region}: {str(e)}"


async def current_datetime() -> str:
    """
    Get current date and time for timestamping grid operations.
    
    Returns:
        Current datetime as formatted string
    """
    now = datetime.now()
    return f"📅 Current time: {now.strftime('%Y-%m-%d %H:%M:%S')} (Local Time)"


# Function registry for AIQ toolkit
GRID_FUNCTIONS = {
    "optimize_grid": optimize_grid,
    "show_last_optimization": show_last_optimization, 
    "current_datetime": current_datetime
}


def register_grid_functions():
    """Register all grid functions with AIQ toolkit."""
    logger.info(f"Registered {len(GRID_FUNCTIONS)} grid optimization functions")
    return GRID_FUNCTIONS