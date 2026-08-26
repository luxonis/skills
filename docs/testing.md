# Testing

These tests exercise the contracts that make the plugin useful when a customer starts with a
normal OAK request and does not study the skill list first.

Run the deterministic checks from the plugin root:

```bash
python3 tests/validate_static.py
```

The test layers are:

1. Static structure: eight skills, plugin identity, referenced files, scripts.
2. Script checks with local fakes and no hardware.
3. Fresh-agent behavior cases from `tests/prompts/`.
4. A future read-only device smoke test when an existing inspectable app is available.

Deterministic checks do not replace representative agent benchmarks, customer testing, or
real-device validation. No benchmark, fresh-agent, customer, or real-device result is included
in this branch. Future device testing must not deploy, stop, restart, reset, update, adopt,
flash, or change settings.
