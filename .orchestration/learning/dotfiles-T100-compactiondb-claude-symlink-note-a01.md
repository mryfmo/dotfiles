# T100 learning triage

No-follow directory construction includes the project .claude directory. A symlink there fails before health storage exists, so non-enforcing hook exception handling cannot record diagnostics there. Document this alongside the storage safety guarantee and test the outermost directory as well as nested storage. Validated by the path tests; no rule promotion.
