# Exact supplemental factual prompt

This is a blinded supplemental check for `orch-factual`. Do not inspect other benchmark output, modify files, or call subagents. Apply correctness before efficiency. Return one JSON object with exactly `id`, `answer`, `path`, and `rationale`. Answer whether JSON object member/key order is semantically significant according to the JSON data model, while distinguishing that textual order may still be preserved or observed by particular parsers/APIs. Use `id` = `orch-factual`. Do not mention or infer your own model.
