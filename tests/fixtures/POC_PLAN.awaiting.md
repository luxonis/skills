# POC plan

Status: awaiting-plan-approval
Revision: 1

## Outcome

Read a barcode on each representative carton and emit its decoded value once.

## Proposed pipeline

```mermaid
flowchart LR
  Camera --> Decoder --> Deduplicate --> Output
```

## Working-demo checks

- Decode all five supported fixture codes in three repeat runs.
- Emit each observed carton once.
