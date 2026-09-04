#!/usr/bin/env python3
"""
ROSE Setup Wizard

Interactive CLI tool to configure ROSE for your environment.
Generates config.yaml, secrets.env, and directory structure.
"""

import os
import json
from pathlib import Path
from typing import Optional


CONFIG_PATH = Path("config.yaml")
SECRETS_PATH = Path("secrets.env")
PLUGIN_DIR = Path("plugins")
DATA_DIR = Path("data")


def ask(prompt: str, default: Optional[str] = None) -> str:
    """Prompt user for input with optional default."""
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    return input(f"{prompt}: ").strip()


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Prompt user for yes/no answer."""
    default_str = "yes" if default else "no"
    response = input(f"{prompt} ({default_str}): ").strip().lower()
    if response in ("y", "yes"):
        return True
    elif response in ("n", "no"):
        return False
    return default


def step(msg: str) -> None:
    """Print step header."""
    print(f"\n{'=' * 50}")
    print(f"  {msg}")
    print(f"{'=' * 50}\n")


def write_config(config: dict) -> None:
    """Write configuration to YAML file."""
    import yaml
    
    with CONFIG_PATH.open("w") as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"✔ Configuration saved to {CONFIG_PATH}")


def write_secrets(secrets: dict) -> None:
    """Write secrets to .env file."""
    with SECRETS_PATH.open("w") as f:
        for key, value in secrets.items():
            f.write(f"{key}={value}\n")
    
    # Set restrictive permissions
    SECRETS_PATH.chmod(0o600)
    print(f"✔ Secrets saved to {SECRETS_PATH} (mode 0600)")
    print("  ⚠️  Keep this file safe! Never commit to version control.")


def create_dirs() -> None:
    """Create required directories."""
    for directory in [PLUGIN_DIR, DATA_DIR]:
        directory.mkdir(exist_ok=True)
        print(f"✔ Created directory: {directory}")


def create_example_plugin() -> None:
    """Create an example plugin structure."""
    example_dir = PLUGIN_DIR / "example_plugin"
    example_dir.mkdir(exist_ok=True)
    
    # plugin.json
    plugin_json = {
        "name": "Example Plugin",
        "version": "1.0.0",
        "author": "Your Name",
        "description": "An example plugin template",
        "entry_point": "plugin.py"
    }
    
    with (example_dir / "plugin.json").open("w") as f:
        json.dump(plugin_json, f, indent=2)
    
    # plugin.py
    plugin_py = '''"""Example ROSE plugin."""
from rose.plugin import RosePlugin, tool


class ExamplePlugin(RosePlugin):
    """An example plugin for ROSE."""
    
    name = "Example Plugin"
    version = "1.0.0"
    
    @tool
    def my_tool(self, input_data: str) -> str:
        """A simple example tool.
        
        Args:
            input_data: Input string
            
        Returns:
            Processed string
        """
        return f"Processed: {input_data}"
    
    @tool
    def calculate(self, a: float, b: float, operation: str = "add") -> float:
        """Perform a calculation.
        
        Args:
            a: First number
            b: Second number
            operation: add, subtract, multiply, divide
            
        Returns:
            Result of operation
        """
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b if b != 0 else float("nan")
        return 0


def setup(rose_app):
    """Initialize plugin in ROSE."""
    return ExamplePlugin()
'''
    
    with (example_dir / "plugin.py").open("w") as f:
        f.write(plugin_py)
    
    # requirements.txt
    with (example_dir / "requirements.txt").open("w") as f:
        f.write("# Add plugin dependencies here\n")
    
    print(f"✔ Created example plugin: {example_dir}")
    print(f"  See {example_dir}/plugin.py to get started")


def main() -> None:
    """Run the setup wizard."""
    
    print("\n" + "=" * 50)
    print("  🌹 ROSE Setup Wizard")
    print("=" * 50)
    print("\nThis wizard will configure ROSE for your environment.")
    print("Press Ctrl+C to cancel at any time.\n")
    
    # Database Configuration
    step("Database Configuration")
    print("ROSE stores experiments in a database.")
    print("Options: PostgreSQL (recommended), SQLite (local dev)")
    
    db_type = ask("Database type (postgresql/sqlite)", "postgresql").lower()
    
    if db_type == "postgresql":
        db_host = ask("PostgreSQL host", "localhost")
        db_port = ask("PostgreSQL port", "5432")
        db_name = ask("Database name", "rose_db")
        db_user = ask("Database user", "rose")
        db_pass = ask("Database password", "rose")
        db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    else:
        db_url = "sqlite:///./data/rose.db"
        print(f"✔ Using SQLite: {db_url}")
    
    # LLM Configuration
    step("LLM Provider Configuration")
    print("ROSE can use local or cloud language models.")
    print("Options: ollama (local, free), openai, claude")
    
    llm_provider = ask("LLM provider (ollama/openai/claude)", "ollama").lower()
    
    llm_url = ""
    llm_key = ""
    
    if llm_provider == "ollama":
        llm_url = ask("Ollama server URL", "http://localhost:11434")
        print("✔ Using local Ollama")
        print("  Install from: https://ollama.ai")
    elif llm_provider == "openai":
        llm_url = "https://api.openai.com/v1"
        llm_key = ask("OpenAI API key (sk-...)")
    elif llm_provider == "claude":
        llm_url = "https://api.anthropic.com"
        llm_key = ask("Claude API key")
    
    # Vision & Voice
    step("Vision & Voice (Optional)")
    
    vision_enabled = ask_yes_no("Enable vision support?", True)
    vision_url = ""
    vision_key = ""
    
    if vision_enabled:
        vision_provider = ask("Vision provider (openai/local)", "openai")
        if vision_provider == "openai":
            vision_url = "https://api.openai.com/v1/vision"
            vision_key = ask("Vision API key (usually same as LLM)")
        else:
            vision_url = ask("Local vision API URL", "http://localhost:8002")
    
    whisper_enabled = ask_yes_no("Enable Whisper (speech-to-text)?", True)
    whisper_cmd = ""
    
    if whisper_enabled:
        whisper_cmd = ask("Whisper command", "whisper")
        print("  Install: pip install openai-whisper")
    
    piper_enabled = ask_yes_no("Enable Piper (text-to-speech)?", True)
    piper_cmd = ""
    
    if piper_enabled:
        piper_cmd = ask("Piper command", "piper")
        print("  Install: pip install piper-tts")
    
    # Autonomy Mode
    step("Autonomy Mode (Optional)")
    print("Autonomy mode allows ROSE to independently plan and execute research.")
    print("This requires careful configuration and monitoring.")
    
    autonomy_enabled = ask_yes_no("Enable autonomous research mode?", False)
    autonomy_max_iter = "10"
    human_approval = "true"
    
    if autonomy_enabled:
        autonomy_max_iter = ask("Max autonomy iterations", "10")
        human_approval = "true" if ask_yes_no("Require human approval?", True) else "false"
    
    # API Configuration
    step("API Configuration")
    api_host = ask("API host", "0.0.0.0")
    api_port = ask("API port", "8000")
    api_debug = ask_yes_no("Enable debug mode?", False)
    
    # Prepare configuration
    config = {
        "database": {
            "url": db_url,
            "echo": api_debug
        },
        "llm": {
            "provider": llm_provider,
            "url": llm_url,
            "api_key": llm_key if llm_key else "${LLM_API_KEY}"
        },
        "vision": {
            "enabled": vision_enabled,
            "provider": "openai" if vision_enabled else None,
            "url": vision_url,
            "api_key": vision_key if vision_key else "${VISION_API_KEY}"
        },
        "voice": {
            "whisper_enabled": whisper_enabled,
            "whisper_command": whisper_cmd,
            "piper_enabled": piper_enabled,
            "piper_command": piper_cmd
        },
        "autonomy": {
            "enabled": autonomy_enabled,
            "max_iterations": int(autonomy_max_iter),
            "human_approval_required": human_approval == "true"
        },
        "api": {
            "host": api_host,
            "port": int(api_port),
            "debug": api_debug
        }
    }
    
    secrets = {}
    if llm_key:
        secrets["LLM_API_KEY"] = llm_key
    if vision_key:
        secrets["VISION_API_KEY"] = vision_key
    
    # Summary
    step("Configuration Summary")
    print(f"Database:      {db_type}")
    print(f"LLM Provider:  {llm_provider}")
    print(f"Vision:        {'✔' if vision_enabled else '✗'}")
    print(f"Voice:         {'✔' if whisper_enabled or piper_enabled else '✗'}")
    print(f"Autonomy:      {'✔' if autonomy_enabled else '✗'}")
    print(f"API:           http://{api_host}:{api_port}")
    
    # Write files
    step("Writing Configuration Files")
    write_config(config)
    if secrets:
        write_secrets(secrets)
    else:
        print(f"✔ No secrets to save (using defaults)")
    
    # Create directories
    step("Creating Directories")
    create_dirs()
    create_example_plugin()
    
    # Completion
    step("🎉 Setup Complete!")
    print("ROSE is ready to run!\n")
    print("Next steps:")
    print("  1. Review config.yaml")
    print("  2. Start the backend:  uvicorn main:app --reload")
    print("  3. Start LLM proxy:    uvicorn llm_server:app --port 8001")
    print("  4. Open dashboard:     http://localhost:8000")
    print("\nFor detailed docs, see:")
    print("  • docs/getting-started.md")
    print("  • docs/architecture.md")
    print("  • docs/tools.md\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled.")
        exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        exit(1)
