# T42 learning triage

## Candidates

1. **Validator pins are auth-mode dependent.** Model pins in
   `validate-agent-assets.py` implicitly assume the Codex auth mode: a model
   valid under API-key auth can be rejected under ChatGPT login. When a pin
   changes because of auth, name the auth mode and the decision date in the
   pin message, as done here.
2. **Pin the effort alongside the model.** The negative test now covers the
   previous model, so a revert of the manifest alone fails validation
   instead of silently restoring a model the CLI rejects.

## Promotion

None. These are candidates only.
