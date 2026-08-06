# Conversion gates

Stop **blocked** when any required gate fails:

1. Source artifact is missing, corrupt, or not the approved revision.
2. Target RVC platform is unknown.
3. License approval or required cloud-upload approval is absent.
4. Input/preprocessing or output/parser contract is unknown.
5. Current supported-operator documentation contradicts the source graph.
6. Required credentials or target prerequisites are unavailable.
7. Produced archive lacks the expected target executable, input, head, parser, or label order.
8. Representative source-versus-converted inference is invalid.
9. INT8 misses the approved post-conversion quality gate.

Do not lower a gate silently, substitute another model, or retry unchanged commands indefinitely.
