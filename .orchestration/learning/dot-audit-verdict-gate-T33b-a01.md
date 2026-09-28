# T33b learning triage

## Candidates

1. When a gate greps model output for a marker that also appears in the
   prompt, anchor the match to whole lines. The prompt is echoed inline, so
   `` `Verdict: blocked` `` sits mid-sentence, while a real verdict is a line
   of its own. Test with the echoed prompt present.
2. "Final line" gates on LLM CLI output should take the *last matching*
   line, not the literal last line. Review output can repeat the final
   message or append metadata.

## Promotion

None. These are candidates only.
