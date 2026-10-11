# Optional integrations: guided extension labs

All commands run from the extracted course root. Below, PY means the environment
Python: `.venv/bin/python` on Unix or `.\.venv\Scripts\python.exe` on Windows.
Replace PY with that actual path; it is not a built-in command.
These examples were syntax-checked, not live-tested against providers or cloud.
Install only the week's dependency. Do not install all frameworks into one large
uncontrolled environment. Save exact successful versions using `PY -m pip freeze`
and keep separate CPU/GPU or integration lockfiles where needed.

## Week 6: HTTP API
```text
PY -m pip install -r requirements-api.txt
PY -m uvicorn integrations.api_app:app --host 127.0.0.1 --port 8000
```
Open http://127.0.0.1:8000/docs and http://127.0.0.1:8000/health.
The seeded in-memory DB is recreated per request. This is intentional for initial
read-only labs, not a persistent service. Replace it in labs 06B and 19B.

## Week 8: OpenAI or Anthropic
```text
PY -m pip install openai
PY -m pip install anthropic
```
Configure OPENAI_API_KEY and OPENAI_MODEL or ANTHROPIC_API_KEY and ANTHROPIC_MODEL
using your local secret manager or terminal environment. Choose a model currently
available to your own account; none is assumed in the pack. Example PowerShell
model configuration: `$env:OPENAI_MODEL = "your-available-model-id"`.
Call from a local Python file:
```python
from integrations.provider_adapters import ask
print(ask("openai", "Explain what a SQL JOIN does in one sentence."))
```
Switch provider to anthropic for the second lab. Keys are read by the SDKs.
This can incur charges. Use synthetic prompts and inspect provider usage records.
Add streaming, refusal/stop handling, schema validation and bounded retry tests as
separate extensions. Log sanitized metadata, not keys or confidential prompts.

## Weeks 10-11: Hugging Face and PyTorch
Use the official PyTorch installation selector for your CPU/GPU platform.
Install transformers in that environment, set HF_MODEL to a reviewed small
text-classification model, optionally pin HF_REVISION to a commit, then run:
```text
PY -m integrations.hf_classifier
PY -m integrations.torch_demo
```
Model downloads require network and disk space. Read the model card, license and
hardware requirements before downloading. These labs do not require training an LLM.

## Weeks 13-15: vectors and LangChain
Follow R8 for PostgreSQL/pgvector setup. Keep embeddings plus source/access metadata,
add an organization filter, and compare retrieval with the offline lexical baseline.
Follow R9 for the current LangChain retrieval abstractions. No deprecated chain
class is required. Your deliverable is an equivalent tested retriever, not an import
that happens to succeed. Preserve source identity and scoped queries.

## Week 18: MCP
The provided import uses the official Python SDK's v1 FastMCP interface. In a fresh
integration environment, install `mcp>=1,<2` and confirm current v1 docs. If you
choose a newer major SDK, adapt the server using its migration documentation.
Run it as a module through a compatible local client using command PY and arguments
`-m integrations.mcp_server`, with the working directory set to the course root.
A directly launched stdio server may wait quietly for a client; that is not failure.
Do not send debug prints to stdout. Verify discovery and tool calls through the
actual MCP connection, not by directly importing search_guidance.

## Week 19: container
```text
docker build -t servicedesk-course .
docker run --rm -p 8000:8000 servicedesk-course
```
The image contains the synthetic teaching API. It is not the final secure capstone.
For the cloud port contract the process reads PORT, defaulting to 8000.
Use a tested exact dependency lock and an image digest for your release packet.

## Weeks 20-21: cloud, evaluation, analytics
Use COURSE.md labs 20A-21B and official references R13-R17. Implement authentication,
external persistence, request limits, secrets, and rollback before the live pilot.
DeepEval semantic metrics can call a paid evaluator model; measure that usage too.
Start analytics in local JSONL, then choose PostHog or Amplitude and confirm current
SDK initialization and event-call signatures. Keep your own event contract stable.
No cloud resource, analytics account, live evaluation, or paid API call was created
or executed while preparing this course.
