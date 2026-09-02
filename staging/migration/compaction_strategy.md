# Compaction strategy

Keep Codex 0.152.0 compaction defaults. No custom token threshold, scope, prompt, or compaction hook is justified yet.

Methodological rule: **durable information must be externalized before context loss matters**.

- Critical facts belong in the source-of-truth register.
- Accepted/proposed choices belong in the decision register.
- Required behavior belongs in specifications.
- Current resumable work belongs in run state.
- Significant completed history belongs in progress.

Conversation summaries and compaction output are navigation aids, not authoritative storage. A future pre-compaction hook may be evaluated only if repeated evidence shows sessions lose critical resumable state and a safe, non-fabricating check can detect that condition. It must not autoaccept decisions or overwrite human content.
