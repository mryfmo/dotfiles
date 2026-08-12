# T44 learning triage

Explicit marker extraction is reliable when marker discovery and content boundaries are separate operations: enumerate bracket spans first, then derive tag-form content from adjacent marker positions. Keyword heuristics must run on residual prose so explicit content cannot be duplicated or downgraded into session-scoped candidates.

English best-effort keyword extraction needs ASCII sentence boundaries; splitting only on full-width punctuation silently turns an entire English prompt into one candidate.
