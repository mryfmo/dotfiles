// Stands in for omp 18.11.3's src/discovery/index.ts in the test that runs the real bun: the registry's
// `getAllProvidersInfo()`, reduced to the provider ids omp-run.sh reads.
export function getAllProvidersInfo(): { id: string }[] {
	return [{ id: "native" }, { id: "agents" }, { id: "cline" }];
}
