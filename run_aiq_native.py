#!/usr/bin/env python3
"""
Run AIQ Grid Optimization with Native Framework
Bypasses LangChain compatibility issues by using AIQ's native LLM integration
"""

import os
import sys
import asyncio
from typing import Dict, Any
from pathlib import Path

# Add AIQ toolkit to Python path
sys.path.insert(0, "/Users/hydrogeo/Downloads/Grid_Optmize/.venv/lib/python3.12/site-packages")

from aiq.builder.workflow_builder import WorkflowBuilder
from aiq.llm.openai_llm import OpenAIModelConfig
from grid_optimization.integrations.llm_config import create_grid_llm_config
from grid_optimization.integrations.aiq_integration import (
    optimize_grid_region,
    get_optimization_status,
    analyze_grid_metrics
)


async def create_native_aiq_config() -> Dict[str, Any]:
    """Create AIQ configuration that uses native framework instead of LangChain."""
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    
    config = {
        "general": {
            "use_uvloop": True
        },
        "functions": {
            "current_datetime": {
                "_type": "grid_optimization.integrations.aiq_functions/current_datetime",
                "description": "Get current date and time for grid optimization timestamping"
            },
            "optimize_grid": {
                "_type": "grid_optimization.integrations.aiq_functions/optimize_grid", 
                "description": "Optimize power grid for specified region"
            },
            "show_last_optimization": {
                "_type": "grid_optimization.integrations.aiq_functions/show_last_optimization",
                "description": "Display latest optimization results for a region"
            }
        },
        "llms": {
            "grid_llm": {
                "_type": "openai",
                "model_name": "gpt-4o-mini",
                "temperature": 0.1,
                "max_tokens": 2048,
                "api_key": api_key
            }
        },
        "workflow": {
            "_type": "function_calling_agent",  # Use native AIQ agent instead of react_agent
            "tool_names": [
                "optimize_grid",
                "show_last_optimization", 
                "current_datetime"
            ],
            "llm_name": "grid_llm",
            "verbose": True,
            "system_message": """You are a grid optimization assistant. You can:
1. Optimize power grids using optimize_grid
2. Show optimization results using show_last_optimization  
3. Get current time using current_datetime

Available regions: us-west, us-east, us-central, pgae"""
        }
    }
    
    return config


async def run_grid_optimization():
    """Run grid optimization using native AIQ configuration."""
    try:
        # Create native configuration
        config_dict = await create_native_aiq_config()
        
        print("🔧 Starting AIQ Grid Optimization with native configuration...")
        print(f"Using model: {config_dict['llms']['grid_llm']['model_name']}")
        
        # Build and run workflow
        async with WorkflowBuilder.from_config(config_dict) as builder:
            workflow = await builder.get_workflow()
            
            print("✅ AIQ workflow initialized successfully!")
            print("Available functions:")
            for func_name in config_dict["functions"]:
                print(f"  - {func_name}: {config_dict['functions'][func_name]['description']}")
            
            # Interactive loop
            while True:
                try:
                    user_input = input("\n💬 Enter your grid optimization request (or 'quit' to exit): ")
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    if not user_input.strip():
                        continue
                        
                    print("🤖 Processing request...")
                    response = await workflow.ainvoke({"input": user_input})
                    print(f"📊 Response: {response}")
                    
                except KeyboardInterrupt:
                    print("\n👋 Interrupted by user")
                    break
                except Exception as e:
                    print(f"❌ Error processing request: {e}")
                    
    except Exception as e:
        print(f"❌ Failed to initialize AIQ workflow: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Set up event loop
    if os.name == 'nt':  # Windows
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    exit_code = asyncio.run(run_grid_optimization())
    exit(exit_code)