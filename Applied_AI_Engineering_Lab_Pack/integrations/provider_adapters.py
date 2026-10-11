"""Optional live calls: requires SDK, keys, model IDs, and paid account access.
Illustrative adapters; not live-tested. Explicit SDK retry limits avoid hidden retries.
"""
import os
import time


def ask(provider, question):
    started=time.perf_counter()
    policy="Answer briefly. If evidence is missing, say so."
    if provider == "openai":
        from openai import OpenAI
        model=os.environ["OPENAI_MODEL"]
        response=OpenAI(timeout=30.0,max_retries=0).responses.create(
            model=model, instructions=policy, input=question,
            max_output_tokens=300)
        text=response.output_text
        usage=response.usage.model_dump() if response.usage else None
        request_id=getattr(response,"_request_id",None)
    elif provider == "anthropic":
        from anthropic import Anthropic
        model=os.environ["ANTHROPIC_MODEL"]
        response=Anthropic(timeout=30.0,max_retries=0).messages.create(
            model=model, system=policy, max_tokens=300,
            messages=[{"role":"user","content":question}])
        text="\n".join(block.text for block in response.content if block.type == "text")
        usage=response.usage.model_dump() if response.usage else None
        request_id=getattr(response,"_request_id",None)
    else:
        raise ValueError("unknown provider")
    return {"text":text,"model":model,"usage":usage,
            "request_id":request_id,"latency_ms":round((time.perf_counter()-started)*1000)}
