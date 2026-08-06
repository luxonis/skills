# Current Luxonis context

Use live sources for version-sensitive Luxonis decisions.

## Source priority

1. Luxonis MCP tools for platform overview, docs, examples, and models.
2. Exact example source or model metadata returned by MCP.
3. `https://docs.luxonis.com/llms.txt` and its current linked pages.
4. Installed `oakctl`, DepthAI, ModelConverter, and other CLI/package versions and help.
5. A shallow `oak-examples` `main` checkout for exact source scaffolding.
6. Model memory only for stable general reasoning.

Never use memory alone for exact DepthAI APIs, supported nodes, device-family behavior, current
commands, model compatibility, or conversion flags.

## MCP discovery sequence

Use the currently exposed Luxonis MCP tool names and schemas rather than assuming remembered names.
The normal intent is:

1. Get a platform overview only when orientation is needed.
2. Find candidate examples, then retrieve the exact selected example.
3. Search models, then retrieve exact candidate metadata.
4. Search docs, then retrieve the pages that support the selected topology and APIs.

Record missing tools or conflicting sources. Do not silently substitute memory.

## Durable fallback

When allowed, reuse `~/.luxonis/agent-context/` for shared Luxonis source caches. Record source URL,
commit/version, retrieval date, and whether the cache is current or fallback. Keep reference
checkouts immutable and copy the chosen example into the project before editing it.

If shared context is unavailable, use a project-external temporary checkout or current web source.
Do not turn an edited customer project into the canonical example reference.

Project-specific decisions belong in `DEVICE.md`, `POC_PLAN.md`, `MODEL_CONVERSION.md`, and
`evidence/`, not in the shared cache.
