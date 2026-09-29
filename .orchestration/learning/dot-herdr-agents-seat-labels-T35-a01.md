# T35 learning triage

1. **Map a role to the exact seat, not the whole team.** Mapping every team member to the worker role made detection ambiguous in the live team. The spec named the precise seat; follow it literally.
2. **When an upstream component renames identifiers** (here, herdr agent names), audit every lookup that used them. Attach still used `herdr agent get` after the label-based fix.
3. **A baseline swap must not change file modes.** Restore with `cat src > dst` (or `git show … > dst`) and never `chmod`. The mode flip slipped into two branches.
4. **The independent review found real defects** for the fourth task in a row. Keep it before every RESULT.

## Promotion

None. These are candidates only; promotion is the orchestrator's call.

## Revision 2

5. **Never source a config file in the caller's scope from a helper.** It silently overrides explicit env. Use a subshell or function-local variables, as the resolvers already do.
6. **Role selection must follow the documented identity grammar,** which allows solo and `-aNNN` names. Do not infer roles from a suffix pattern.
