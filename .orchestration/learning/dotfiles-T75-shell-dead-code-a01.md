# Learning triage: dotfiles-T75-shell-dead-code-a01

Candidates only; nothing is promoted.

1. **"Unreferenced" needs every loader in the search.** Sheldon plugin tomls load files by directory (`local = …`) plus `use = [...]`. A grep for a file's own name misses loaders that reference its directory, which is how chezmoi-notify looked unreferenced.
2. **Deleting a chezmoi source leaves the deployed target.** Plan a `.chezmoiremove` entry together with the deletion, or name it as a follow-up when that file is out of scope.
3. **Moving test pins needs a stand-in.** When a deleted file served as the "representative" fixture in bats manifests, swap in another file with the same deploy scope (here `server/ssh_agent.sh`) rather than dropping the assertion.
