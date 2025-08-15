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


async def create_native_aiq_config():
    """Create AIQ configuration using proper OpenAI model config."""
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    
    # Create OpenAI model config
    llm_config = OpenAIModelConfig(
        api_key=api_key,
        model_name="gpt-4o-mini",
        temperature=0.1,
        max_tokens=2048
    )
    
    return llm_config


async def run_grid_optimization():
    """Run grid optimization using native AIQ configuration."""
    try:
        # Create LLM configuration
        llm_config = await create_native_aiq_config()
        
        print("🔧 Starting AIQ Grid Optimization with native configuration...")
        print(f"Using model: {llm_config.model_name}")
        
        # Import our functions
        from grid_optimization.integrations.aiq_functions import GRID_FUNCTIONS
        
        print("✅ AIQ configuration created successfully!")
        print("Available functions:")
        for func_name, func in GRID_FUNCTIONS.items():
            print(f"  - {func_name}: {func.__doc__.split('.')[0] if func.__doc__ else 'Grid function'}")
        
        # Check if running interactively
        import sys
        if sys.stdin.isatty():
            # Interactive loop - call functions directly
            while True:
                try:
                    user_input = input("\n💬 Enter your grid optimization request (or 'quit' to exit): ")
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    if not user_input.strip():
                        continue
                    
                    print("🤖 Processing request...")
                    
                    # Simple keyword matching to demonstrate functionality
                    if "time" in user_input.lower() or "datetime" in user_input.lower():
                        result = await GRID_FUNCTIONS["current_datetime"]()
                        print(f"📊 Response: {result}")
                    elif "optimize" in user_input.lower():
                        # Extract region if mentioned, default to us-west
                        region = "us-west"
                        for r in ["us-east", "us-central", "pgae"]:
                            if r in user_input.lower():
                                region = r
                                break
                        result = await GRID_FUNCTIONS["optimize_grid"](region)
                        print(f"📊 Response: {result}")
                    elif "status" in user_input.lower() or "show" in user_input.lower():
                        # Extract region if mentioned, default to us-west
                        region = "us-west"
                        for r in ["us-east", "us-central", "pgae"]:
                            if r in user_input.lower():
                                region = r
                                break
                        result = await GRID_FUNCTIONS["show_last_optimization"](region)
                        print(f"📊 Response: {result}")
                    else:
                        print(f"📊 Available commands: optimize [region], status [region], time")
                        print(f"📊 Available regions: us-west, us-east, us-central, pgae")
                    
                except KeyboardInterrupt:
                    print("\n👋 Interrupted by user")
                    break
                except Exception as e:
                    print(f"❌ Error processing request: {e}")
        else:
            print("📊 Running in non-interactive mode. Use command line arguments:")
            print("📊 Available commands: optimize [region], status [region], time")
            print("📊 Available regions: us-west, us-east, us-central, pgae")
            
            # Handle command line arguments
            if len(sys.argv) > 1:
                command = " ".join(sys.argv[1:]).lower()
                if "time" in command or "datetime" in command:
                    result = await GRID_FUNCTIONS["current_datetime"]()
                    print(f"📊 Response: {result}")
                elif "optimize" in command:
                    region = "us-west"
                    for r in ["us-east", "us-central", "pgae"]:
                        if r in command:
                            region = r
                            break
                    result = await GRID_FUNCTIONS["optimize_grid"](region)
                    print(f"📊 Response: {result}")
                elif "status" in command or "show" in command:
                    region = "us-west"
                    for r in ["us-east", "us-central", "pgae"]:
                        if r in command:
                            region = r
                            break
                    result = await GRID_FUNCTIONS["show_last_optimization"](region)
                    print(f"📊 Response: {result}")
            else:
                # Demo run with time command
                result = await GRID_FUNCTIONS["current_datetime"]()
                print(f"📊 Demo - Current time: {result}")
                
    except Exception as e:
        print(f"❌ Failed to initialize AIQ configuration: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Set up event loop
    if os.name == 'nt':  # Windows
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    exit_code = asyncio.run(run_grid_optimization())
    exit(exit_code)