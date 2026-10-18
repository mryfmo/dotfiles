---
{
  "format": 1,
  "task": "test",
  "head": "HEAD",
  "pr": 1,
  "ledger":
    [
      { "id": 4244128846, "class": "class-count-scope" },
      { "id": 4244175775, "class": "class-count-scope" },
      { "id": "audit:3a54d34:2", "class": "class-count-scope" },
      { "id": 4244248692, "class": "threat-row-outside-paths" }
    ],
  "searches":
    [{ "class": "class-count-scope", "records": ["M-20261012-3.md"] }],
  "replans":
    {
      "class-count-scope":
        {
          "specification": "the class is the finding's, not the review's",
          "design": "one ledger row per finding",
          "implementation": "the gate counts the rows",
          "verification": "the S6 fixture"
        }
    }
}
---

# Acceptance: test (S6 fixture, the search entry present)
