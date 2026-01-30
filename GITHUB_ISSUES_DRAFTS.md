# GitHub Issues - Ready to Submit

These are ready-to-copy GitHub issue descriptions for the Hive repository.

---

## Issue #1: Add mypy Type Checking to CI Pipeline

**Title**: `chore(ci): Add mypy type checking to CI pipeline`

**Labels**: `enhancement`, `ci/cd`, `code-quality`

**Description**:

### Problem

The codebase has moderate type hint coverage (~57% of Python files use type hints) but no automated type checking in CI. This means type safety issues can slip through code review and cause runtime errors.

Current state:
- `mypy` is listed in `core/requirements-dev.txt` but not used in CI
- No type checking configuration file
- Inconsistent type hint usage across modules

### Proposed Solution

Add mypy type checking to the CI pipeline to catch type errors before merge.

**Changes**:

1. Create `mypy.ini` configuration file:
```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True

# Start lenient, gradually tighten
check_untyped_defs = True
disallow_untyped_calls = False  # Enable later
disallow_untyped_defs = False   # Enable later

# Type-check specific packages
files = core/framework, tools/src/aden_tools

[mypy-tests.*]
ignore_errors = True
```

2. Add mypy job to `.github/workflows/ci.yml`:
```yaml
type-check:
  name: Type Checking (mypy)
  runs-on: ubuntu-latest

  steps:
    - uses: actions/checkout@v4

    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        pip install -e ./core
        pip install mypy

    - name: Run mypy
      run: mypy --config-file mypy.ini
```

3. Fix immediate type errors in critical modules (if any found)

4. Update `CONTRIBUTING.md` with type checking guidelines

### Benefits

- ✅ Catch type errors before code review
- ✅ Improve IDE autocomplete and refactoring
- ✅ Reduce runtime errors from type mismatches
- ✅ Better developer experience
- ✅ Foundation for stricter type checking in future

### Implementation Plan

- [ ] Create `mypy.ini` with lenient initial settings
- [ ] Add mypy CI job
- [ ] Fix any type errors blocking CI
- [ ] Document type checking requirements in CONTRIBUTING.md
- [ ] (Future) Gradually tighten mypy settings

### Estimated Effort

2-3 hours

### Related Issues

Part of improving code quality and production readiness (see ROADMAP.md).

---

### I'm happy to implement this if the maintainers approve. I can submit a PR within 1-2 days.

---

## Issue #2: Add Test Coverage Reporting with Codecov Integration

**Title**: `test: Add test coverage reporting with Codecov integration`

**Labels**: `enhancement`, `testing`, `ci/cd`

**Description**:

### Problem

Currently, there's **no visibility into test coverage**. While the project has ~18 test files with 191+ test functions, we don't know:
- What percentage of code is covered by tests
- Which modules lack test coverage
- Whether PRs increase or decrease coverage

This makes it difficult to:
- Identify untested code paths
- Prevent coverage regressions
- Set quality standards for contributors

### Proposed Solution

Add test coverage reporting with Codecov integration to track and visualize coverage over time.

**Changes**:

1. **Add pytest-cov configuration** to `core/pyproject.toml`:
```toml
[tool.pytest.ini_options]
addopts = """
    --cov=framework
    --cov-report=xml
    --cov-report=html
    --cov-report=term-missing
"""

[tool.coverage.run]
source = ["framework"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
]

[tool.coverage.report]
fail_under = 70
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

2. **Add pytest-cov to dev dependencies**:
```txt
# core/requirements-dev.txt
pytest>=8.0
pytest-cov>=4.1.0
pytest-asyncio>=0.23.0
```

3. **Update CI workflow** (`.github/workflows/ci.yml`):
```yaml
test:
  name: Run Tests with Coverage
  runs-on: ubuntu-latest

  steps:
    - uses: actions/checkout@v4

    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        pip install -e ./core
        pip install -e ./tools
        pip install -r core/requirements-dev.txt

    - name: Run tests with coverage
      run: |
        cd core
        pytest --cov=framework --cov-report=xml --cov-report=term

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./core/coverage.xml
        flags: core-framework
        name: codecov-core
        fail_ci_if_error: false  # Start lenient

    - name: Generate coverage badge
      run: |
        coverage-badge -o coverage.svg -f
```

4. **Add coverage badge to README.md**:
```markdown
[![codecov](https://codecov.io/gh/adenhq/hive/branch/main/graph/badge.svg)](https://codecov.io/gh/adenhq/hive)
```

5. **Create Codecov configuration** (`.codecov.yml`):
```yaml
coverage:
  status:
    project:
      default:
        target: 70%  # Start with 70%, increase over time
        threshold: 2%  # Allow 2% decrease
    patch:
      default:
        target: 80%  # New code should have higher coverage

comment:
  layout: "reach,diff,flags,tree"
  behavior: default

ignore:
  - "*/tests/*"
  - "*/test_*.py"
  - "examples/*"
```

### Benefits

- ✅ **Visibility**: See exactly what code is tested
- ✅ **Quality Gate**: Prevent merging untested code
- ✅ **Trend Analysis**: Track coverage over time
- ✅ **PR Comments**: Codecov bot comments on PRs with coverage impact
- ✅ **Badge**: Show coverage badge in README for transparency
- ✅ **Identify Gaps**: Easy to find modules that need more tests

### Expected Results

Based on preliminary analysis:
- **Current estimated coverage**: 60-70% (need to measure)
- **Target coverage**: 80%+ for core framework
- **High-priority modules to test**:
  - `core/framework/graph/flexible_executor.py`
  - `core/framework/runtime/agent_runtime.py`
  - `core/framework/llm/litellm.py`
  - MCP server integration

### Example Output

After implementation, every PR will show:
```
Coverage report:
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
framework/graph/flexible_executor.py   234     45    81%
framework/runtime/agent_runtime.py     189     12    94%
framework/llm/litellm.py              156     78    50%  ⚠️ Low coverage
--------------------------------------------------------
TOTAL                                 2341    456    81%
```

### Implementation Plan

- [ ] Add pytest-cov configuration
- [ ] Update CI workflow with coverage steps
- [ ] Set up Codecov account and token (maintainers)
- [ ] Add coverage badge to README
- [ ] Document coverage requirements in CONTRIBUTING.md
- [ ] (Future) Increase minimum coverage threshold

### Estimated Effort

3-4 hours (1 hour if maintainers provide Codecov token)

### Related Issues

Part of improving testing infrastructure and production readiness.

---

### I'm happy to implement this if approved. The Codecov integration requires a CODECOV_TOKEN secret in GitHub Actions - I can set up everything else and the maintainers can add the token.

---

## Issue #3: Fix Documentation - Tool Count Inconsistency

**Title**: `docs: Fix MCP tools count inconsistency and create tool inventory`

**Labels**: `documentation`, `bug`

**Description**:

### Problem

The README.md claims "**19 MCP tools**" for agent capabilities, but the actual count appears to be **~10-12 tools** based on the `tools/src/aden_tools/tools/` directory structure.

This creates:
- ❌ User confusion
- ❌ Reduced trust in documentation
- ❌ Unclear tool capabilities

**Current claim** (README.md line 84):
```markdown
This installs:
- **framework** - Core agent runtime and graph executor
- **aden_tools** - 19 MCP tools for agent capabilities  ⚠️ Incorrect count
- All required dependencies
```

**Actual tools found** (preliminary audit):
```
tools/src/aden_tools/tools/
├── file_system_toolkits/
│   ├── apply_diff_tool.py
│   ├── apply_patch_tool.py
│   ├── execute_command_tool.py
│   ├── grep_search_tool.py
│   ├── list_dir_tool.py
│   ├── view_file_tool.py
│   └── write_to_file_tool.py      # 7 tools
├── web_search_tool/               # 1 tool
├── web_scrape_tool/               # 1 tool
├── pdf_read_tool/                 # 1 tool
└── example_tool/                  # 1 template tool

Total: ~10-11 actual tools (need to verify subdirectories)
```

**Discrepancy**: 19 claimed vs ~11 actual = **8 missing tools** or incorrect count

### Proposed Solution

1. **Audit all tools** - Complete inventory of implemented tools
2. **Update documentation** - Correct tool count everywhere
3. **Create tool catalog** - Comprehensive list with descriptions
4. **Clarify roadmap** - Distinguish implemented vs planned tools

**Changes**:

1. **Audit and document all tools** in new file `docs/tools-catalog.md`:
```markdown
# Aden Tools Catalog

## File System Tools (7)

### 1. apply_diff
**Description**: Apply a unified diff to a file
**Input**: `file_path`, `diff_content`
**Output**: `success`, `modified_content`
**Example**:
\`\`\`python
{
  "file_path": "app.py",
  "diff_content": "--- app.py\n+++ app.py\n..."
}
\`\`\`

### 2. apply_patch
**Description**: Apply a patch file to modify files
...

(Continue for all 11 tools)
```

2. **Update README.md** with accurate count:
```markdown
This installs:
- **framework** - Core agent runtime and graph executor
- **aden_tools** - 11 MCP tools for agent capabilities  ✓ Accurate count
- All required dependencies

## Available Tools

Hive includes 11 production-ready MCP tools:

**File Operations (7)**: `apply_diff`, `apply_patch`, `execute_command`, `grep_search`, `list_dir`, `view_file`, `write_to_file`

**Web Tools (2)**: `web_search`, `web_scrape`

**Document Processing (1)**: `pdf_read`

**Template (1)**: `example_tool` (for creating custom tools)

See [Tools Catalog](docs/tools-catalog.md) for complete documentation.
```

3. **Update tools/README.md** with tool inventory

4. **Update ROADMAP.md** to clarify tool status:
```markdown
### Essential Tools
- [x] **File Use Tool Kit** (7 tools implemented)
  - [x] apply_diff, apply_patch, execute_command
  - [x] grep_search, list_dir, view_file, write_to_file
- [ ] **Memory Tools**
  - [x] STM Layer Tool (basic implementation)
  - [x] LTM Layer Tool (RLM - basic implementation)
  - [ ] Semantic search integration (planned)
- [ ] **Infrastructure Tools**
  - [x] Runtime Log Tool
  - [ ] Audit Trail Tool (planned)
  - [x] Web Search (implemented)
  - [x] Web Scraper (implemented)
  - [ ] Recipe for "Add your own tools" (documentation needed)
```

5. **Add tool discovery test** to verify count:
```python
# tools/tests/test_tool_inventory.py
def test_tool_count_matches_documentation():
    """Ensure documented tool count matches actual implementation."""
    from aden_tools import get_available_tools

    tools = get_available_tools()

    # Update this number when adding new tools
    EXPECTED_TOOL_COUNT = 11

    assert len(tools) == EXPECTED_TOOL_COUNT, (
        f"Tool count mismatch: found {len(tools)}, "
        f"expected {EXPECTED_TOOL_COUNT}. "
        f"Update documentation if tools were added/removed."
    )
```

### Benefits

- ✅ Accurate documentation
- ✅ User trust restored
- ✅ Clear tool inventory for users
- ✅ Foundation for tool documentation
- ✅ Automated test prevents future drift

### Implementation Plan

- [ ] Complete tool audit
- [ ] Create `docs/tools-catalog.md` with all tools
- [ ] Update README.md with correct count
- [ ] Update tools/README.md
- [ ] Update ROADMAP.md to clarify tool status
- [ ] Add test to verify count matches docs
- [ ] Verify all tools are actually working (run their tests)

### Estimated Effort

1-2 hours

### Related Issues

Part of documentation cleanup and user experience improvement.

---

### I can submit this as a PR today if approved. It's a quick fix that improves user trust.

---

## Issue #4: 🚀 Implement Local GPU Inference Provider for Cost-Efficient Agent Deployment

**Title**: `feat(llm): Add LocalGPUProvider for local GPU-accelerated inference`

**Labels**: `enhancement`, `performance`, `llm`, `high-impact`

**Description**:

### Problem

Currently, Hive only supports **cloud-based LLM inference** via APIs (OpenAI, Anthropic, Google Gemini). This creates several limitations for production deployments:

**Cost Limitations**:
- Cloud inference costs $0.01-$0.10 per 1K tokens
- High-volume agent deployments can cost hundreds to thousands per day
- Example: 1M tokens/day = $10-$100/day = $300-$3000/month

**Performance Limitations**:
- Rate limits constrain agent throughput (e.g., OpenAI: 10K RPM)
- Network latency adds 200-500ms per request
- No control over inference speed

**Privacy/Security Concerns**:
- Sensitive data sent to third-party APIs
- Cannot deploy in air-gapped environments
- Regulatory compliance issues (GDPR, HIPAA)

**Example User Impact**:
A customer service agent handling 10K tickets/day:
- Cloud API cost: ~$50/day ($1,500/month)
- Rate limits require multiple API keys
- 2-5 second response times due to network latency

### Proposed Solution

Implement **LocalGPUProvider** - a new LLM provider that runs inference locally on GPU using optimized backends (vLLM, llama.cpp, TensorRT-LLM).

**Key Benefits**:
- 💰 **10-100x cost reduction** ($0.0001 vs $0.01-$0.10 per 1K tokens)
- 🚀 **Higher throughput** - No rate limits, batch processing
- 🔒 **Privacy** - Data stays local, no third-party API calls
- ⚡ **Lower latency** - 0.3-0.5s vs 1-3s (local GPU vs cloud API)
- 📶 **Offline operation** - Works without internet connectivity

**Cost Comparison** (1M tokens):
| Provider | Cost | Latency (p50) | Rate Limit |
|----------|------|---------------|------------|
| Claude 3 Haiku (API) | $10 | 1.2s | 10K RPM |
| GPT-3.5 Turbo (API) | $1 | 0.8s | 10K RPM |
| **Llama-3-8B (Local GPU)** | **$0.10** | **0.3s** | **∞** |

### Technical Design

**New Module**: `core/framework/llm/local_gpu.py`

**Architecture**:
```
┌─────────────────────────────────────────────┐
│          LocalGPUProvider                   │
├─────────────────────────────────────────────┤
│  - Implements LLMProvider interface         │
│  - Supports multiple backends:              │
│    • vLLM (highest throughput)             │
│    • llama.cpp (best compatibility)        │
│    • TensorRT-LLM (NVIDIA-optimized)       │
│  - Batch inference for parallel nodes      │
│  - Streaming support                       │
│  - Memory-efficient quantization           │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────┬────────────────┬──────────────┐
│    vLLM      │  llama.cpp     │ TensorRT-LLM │
│ (Production) │  (Development) │  (Research)  │
└──────────────┴────────────────┴──────────────┘
                    │
                    ▼
           ┌──────────────────┐
           │  GPU (CUDA/ROCm) │
           │  RTX 3090/4090   │
           │  A100, H100      │
           └──────────────────┘
```

**Key Features**:

1. **Multiple Backend Support**:
```python
# vLLM for production (highest throughput)
provider = LocalGPUProvider(
    model_path="meta-llama/Llama-3-8B-Instruct",
    backend="vllm",
    gpu_memory_fraction=0.9,
    max_batch_size=32
)

# llama.cpp for development (GGUF models)
provider = LocalGPUProvider(
    model_path="/models/llama-3-8b-instruct-q8_0.gguf",
    backend="llama-cpp",
    gpu_id=0
)
```

2. **Batch Inference** (key performance feature):
```python
# Process multiple agent requests in single GPU batch
requests = [
    {"messages": [{"role": "user", "content": "Task 1"}]},
    {"messages": [{"role": "user", "content": "Task 2"}]},
    # ... 32 requests total
]

responses = await provider.complete_batch(requests)
# Returns 32 responses in ~0.5s (vs 32s sequential)
```

3. **Memory-Efficient Quantization**:
- INT8 quantization: 2x memory reduction, <1% accuracy loss
- INT4 quantization: 4x memory reduction, ~2-3% accuracy loss
- Enables running larger models on consumer GPUs

4. **Streaming Support**:
```python
async for token in provider.stream_complete(messages):
    print(token, end="", flush=True)
    # Real-time agent responses
```

### Implementation Plan

**Phase 1: Core Infrastructure (Week 1)**
- [ ] Create `LocalGPUProvider` class implementing `LLMProvider` interface
- [ ] Implement llama.cpp backend (simplest to start)
- [ ] Add unit tests for provider functionality
- [ ] Document setup guide for GPU dependencies

**Phase 2: Production Features (Week 2)**
- [ ] Implement vLLM backend (highest performance)
- [ ] Add batch inference support
- [ ] Add streaming response support
- [ ] Integrate with FlexibleExecutor for parallel node execution

**Phase 3: Optimization & Polish (Week 3)**
- [ ] Add TensorRT-LLM backend (optional, for NVIDIA GPUs)
- [ ] Performance benchmarking suite
- [ ] Memory profiling and optimization
- [ ] Production deployment guide

**Phase 4: Documentation & Examples (Week 4)**
- [ ] Comprehensive setup guide for different GPU types
- [ ] Example agents using local GPU inference
- [ ] Cost comparison calculator
- [ ] Troubleshooting guide

### Files to Create/Modify

**New Files**:
- `core/framework/llm/local_gpu.py` - Main implementation
- `core/framework/llm/backends/vllm_backend.py` - vLLM wrapper
- `core/framework/llm/backends/llamacpp_backend.py` - llama.cpp wrapper
- `core/framework/llm/backends/tensorrt_backend.py` - TensorRT wrapper
- `core/tests/test_local_gpu_provider.py` - Unit tests
- `docs/local-gpu-inference.md` - Setup and usage guide
- `examples/local_gpu_agent.py` - Example agent
- `benchmarks/test_llm_inference.py` - Performance benchmarks

**Modified Files**:
- `core/framework/llm/__init__.py` - Export LocalGPUProvider
- `core/framework/llm/provider.py` - Add batch interface to LLMProvider
- `core/requirements.txt` - Add optional GPU dependencies
- `README.md` - Document local GPU support

### Dependencies

Add to `core/requirements.txt`:
```txt
# Optional GPU inference backends (install based on use case)
# vllm>=0.3.0; sys_platform=="linux"  # Production (Linux only)
# llama-cpp-python>=0.2.0  # Development (cross-platform)
# tensorrt>=8.6.0; sys_platform=="linux"  # Research (NVIDIA only)
```

Users install based on their backend:
```bash
# For vLLM (production)
pip install vllm

# For llama.cpp (development)
pip install llama-cpp-python

# For GPU-enabled llama.cpp
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
```

### Example Usage

**Agent Configuration**:
```json
{
  "llm_config": {
    "provider": "local-gpu",
    "model_path": "meta-llama/Llama-3-8B-Instruct",
    "backend": "vllm",
    "gpu_id": 0,
    "gpu_memory_fraction": 0.9,
    "max_batch_size": 32,
    "quantization": "int8"
  }
}
```

**Python Code**:
```python
from framework.llm import LocalGPUProvider
from framework.runner import AgentRunner

# Initialize provider
llm_provider = LocalGPUProvider(
    model_path="meta-llama/Llama-3-8B-Instruct",
    backend="vllm"
)

# Use in agent
agent = AgentRunner.from_file("agent.json", llm_provider=llm_provider)
result = agent.run({"input": "Process this ticket..."})
```

### Performance Benchmarks (Expected)

**Single Request Latency**:
| Provider | Latency (p50) | Latency (p95) |
|----------|---------------|---------------|
| Claude API | 1.2s | 2.5s |
| Local GPU (vLLM) | 0.3s | 0.5s |
| **Improvement** | **4x faster** | **5x faster** |

**Batch Throughput** (100 requests):
| Provider | Total Time | Cost |
|----------|------------|------|
| Claude API (sequential) | 120s | $0.50 |
| Claude API (rate limited) | 60s | $0.50 |
| Local GPU (batched) | 5s | $0.001 |
| **Improvement** | **12-24x faster** | **500x cheaper** |

### Hardware Requirements

**Minimum**:
- GPU: NVIDIA RTX 3060 (12GB VRAM) or AMD RX 6800 XT
- RAM: 16GB system RAM
- Storage: 10GB for model weights
- OS: Linux (Ubuntu 20.04+) or Windows 11

**Recommended**:
- GPU: NVIDIA RTX 4090 (24GB VRAM) or A100 (40GB)
- RAM: 32GB+ system RAM
- Storage: 50GB SSD for models
- OS: Ubuntu 22.04 LTS

**Model Size Guide**:
| Model | Quantization | VRAM Needed | Recommended GPU |
|-------|--------------|-------------|-----------------|
| Llama-3-8B | INT8 | 8GB | RTX 3060 12GB |
| Llama-3-8B | FP16 | 16GB | RTX 4080 16GB |
| Llama-3-70B | INT4 | 40GB | A100 40GB |
| Llama-3-70B | INT8 | 80GB | 2x A100 40GB |

### Success Criteria

- [ ] LocalGPUProvider passes all LLMProvider interface tests
- [ ] Supports both vLLM and llama.cpp backends
- [ ] Batch inference works with parallel node execution
- [ ] Performance benchmarks show >10x cost reduction vs cloud
- [ ] Latency benchmarks show 3-5x improvement over cloud APIs
- [ ] Documentation includes setup guide for RTX 30xx/40xx GPUs
- [ ] Example agent successfully runs with local GPU inference
- [ ] Memory usage profiled and optimized (no leaks)

### Risks & Mitigation

**Risk 1**: GPU setup complexity
- **Mitigation**: Comprehensive setup guide, support for cloud VM images

**Risk 2**: Model compatibility issues
- **Mitigation**: Start with well-tested models (Llama-3, Mistral), document compatibility

**Risk 3**: Performance not as expected
- **Mitigation**: Benchmarking suite validates performance claims

**Risk 4**: Memory issues on consumer GPUs
- **Mitigation**: Quantization support, model size recommendations

### Future Enhancements

- Support for model quantization (AWQ, GPTQ, GGUF)
- Multi-GPU support (model parallelism, pipeline parallelism)
- KV cache persistence across requests (faster multi-turn)
- Speculative decoding for latency reduction
- Integration with llama.cpp's CUDA/ROCm/Metal backends

### Related Issues

- Addresses cost concerns for high-volume deployments
- Enables air-gapped deployments
- Foundation for #6 (parallel node execution optimization)
- Supports #5 (performance benchmarking)

---

### I'm uniquely qualified to implement this feature given my experience building llcuda, a CUDA-first Python SDK for GPU-accelerated LLM inference. I've already implemented similar batch inference, quantization, and memory management features.

**Timeline**: 3-4 weeks for full implementation
**Effort**: 20-30 hours total

I can start immediately if this is approved. Happy to discuss the design and gather requirements.

---

## Next Steps

1. **Submit Issues #1-3 immediately** (quick wins to build trust)
2. **Discuss Issue #4 with maintainers** (get buy-in on GPU feature)
3. **Begin prototyping LocalGPUProvider** while waiting for approval
4. **Monitor Discord for feedback** and adjust priorities

These issues are ready to copy/paste into GitHub. I recommend submitting #1-3 today to start building credibility.
