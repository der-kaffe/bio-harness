# Future memory strategy

The candidate does not enable memory.

## Suitable memory

- Stable personal preferences that apply across projects.
- Repeated, low-risk interaction preferences that are expensive to restate.
- Auxiliary reminders whose source and fallibility are clear.

## Unsuitable memory

- Project facts, accepted requirements, specifications, or decisions.
- Current task/run state, test results, incident state, or release status.
- Secrets, credentials, personal data without a defined need, or copied external facts.
- Proposed decisions presented as accepted truth.
- Any rule that must apply deterministically.

## Contradiction handling

Versioned authoritative project sources outrank memory. Current repository evidence establishes what exists and may reveal drift; it does not silently override the approved target. If memory conflicts with an authoritative source, ignore it for the decision, report the conflict when material, and correct/remove the stale memory through an explicit control rather than rewriting project truth.

## Activation criteria

Evaluate activation only after observing real cross-project use. Require evidence of repeated useful recall, a review of local storage/privacy, clear per-chat controls, an inspection/removal process, and tests that stale memory does not override project context. Start narrowly and retain the ability to disable generation and use independently.
