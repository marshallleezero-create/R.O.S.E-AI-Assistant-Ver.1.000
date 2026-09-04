# Tools

Tools are modular capabilities that ROSE can execute.

## Built-in Tools

ROSE includes these tools out of the box:

### Data & Analysis

| Tool | Purpose |
|------|---------|
| `run_simulation` | Execute simulations with parameter sweeps |
| `analyze_image` | Vision-based analysis and interpretation |
| `describe_dataset` | Statistical summaries and exploration |
| `linear_regression` | Predictive modeling |
| `generate_hypotheses` | LLM-driven hypothesis generation |
| `log_experiment` | Store results with full metadata |

### System & Integration

| Tool | Purpose |
|------|---------|
| `read_file` | Load data from files |
| `write_file` | Save results to files |
| `web_search` | Internet information retrieval |
| `run_command` | Execute shell commands |
| `list_files` | Directory listing and file exploration |

## Calling Tools

### Via Chat API

```bash
POST /api/chat/completions
{
  "message": "Run a simulation with param=0.5",
  "session_id": "sess-123"
}

# ROSE automatically decides which tool to use
```

### Via Tool API

```bash
POST /tools/run_simulation
{
  "model": "my_model.py",
  "param": 0.5,
  "iterations": 100
}
```

## Creating Custom Tools

Tools are Python functions registered with decorators.

### Simple Tool

```python
# tools/my_tool.py
from rose.tool import register_tool

@register_tool
def my_tool(input_data: str) -> str:
    """A simple tool.
    
    Args:
        input_data: Input string
        
    Returns:
        Processed string
    """
    return f"Processed: {input_data}"
```

### Advanced Tool

```python
# tools/advanced_tool.py
from rose.tool import register_tool, tool_param
from typing import Optional

@register_tool
def analyze_results(
    data: list,
    method: str = "mean",
    confidence: float = 0.95
) -> dict:
    """Analyze experimental results.
    
    Args:
        data: List of numeric values
        method: Statistical method (mean, median, mode)
        confidence: Confidence level for intervals
        
    Returns:
        Dictionary with statistics
    """
    import statistics
    
    if method == "mean":
        value = statistics.mean(data)
    elif method == "median":
        value = statistics.median(data)
    else:
        value = statistics.mode(data)
    
    return {
        "value": value,
        "count": len(data),
        "method": method,
        "confidence": confidence
    }
```

## Tool Registry

All tools are registered in `tools/__init__.py`:

```python
# tools/__init__.py
from .my_tool import my_tool
from .advanced_tool import analyze_results
from .simulations import run_simulation

__all__ = [
    "my_tool",
    "analyze_results",
    "run_simulation"
]
```

## Tool Discovery

List available tools:

```bash
GET /tools
```

Response:
```json
{
  "tools": [
    {
      "name": "run_simulation",
      "description": "Execute a simulation",
      "params": {...},
      "return_type": "dict"
    },
    ...
  ]
}
```

Get tool schema:

```bash
GET /tools/run_simulation/schema
```

## Tool Parameters

Define tool inputs with Pydantic models:

```python
from pydantic import BaseModel, Field

class SimulationParams(BaseModel):
    model: str = Field(..., description="Path to model file")
    iterations: int = Field(default=100, ge=1, le=10000)
    learning_rate: float = Field(default=0.01, gt=0)
    
@register_tool
def run_simulation(params: SimulationParams) -> dict:
    """Run simulation with parameters."""
    # Implementation
    pass
```

## Error Handling

Tools should handle errors gracefully:

```python
@register_tool
def safe_tool(data: str) -> dict:
    """A tool with error handling."""
    try:
        result = process(data)
        return {"success": True, "result": result}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": "Unexpected error"}
```

## Tool Testing

Test your tools:

```python
# tests/test_tools.py
from tools.my_tool import my_tool

def test_my_tool():
    result = my_tool("hello")
    assert result == "Processed: hello"
```

---

**Next:** [Plugin System](plugins.md)
