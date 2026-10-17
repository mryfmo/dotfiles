# T15 amendment 2 learning

[memory:failure] Recognizing a managed program by its first token still drops user behavior chained after that program. Wrapper-only preservation is insufficient for a whole hook command object.

[memory:decision] For the specified managed bare-script commands, require exactly one remaining token after optional interpreter stripping. Preserve any additional arguments or shell chain as unmanaged. The chain regression fails before that one-line correction and all20 tests pass afterward; keep the wrapper, argument and interpreter cases in the same regression method. Commit current source-validation proof in the task root and state post-publication CI/Bot separately.

[memory:failure] Post-publication reproduction found the current task contract still deletes compact chains and same-basename custom commands. Stop after surviving P1 and ask for the operator/specification decision; passing the named regression is not full preservation evidence.
