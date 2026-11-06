# Needs validation: dotfiles at 8bcf3de4cc773a6d4ad428ac92c27c0233df4818

No `needs_validation` record is in this run's `findings.json`.

The store's prior `needs_validation` record `dsh-profile:web-search-routes-to-the-official-api` (`sweeps/U227-785658d1`) is carried into this run's ledger as an unvalidated candidate with proposed verdict rejected. U227f disables both rows it named, by their base-bundle ids, and the upstream web seam fails closed on the unregistered provider (`REPORT.md` section 5b).

Two facts behind that refutation are upstream source read locally rather than observed: cordis applying a `disabled: true` row by id, and the seam's selection rule. The prior record's own local plan would confirm both in the required sandbox:
1. Install the pinned harness in a scratch HOME, with only loopback networking.
2. Print the composed thak tree.
3. Run one turn whose stub answers with a `web_search` call, with `DEEPSEEK_API_KEY=dummy` and `DEEPSEEK_SEARCH_BASE_URL` at a second loopback stub.
4. Expect that stub to receive no request.

The carried identity candidate (`REPORT.md` section 5a) is not a `needs_validation` record either. Its decisive facts are source-visible; what it lacks is an independent verifier. One fact stays owner-observed: whether the origin repository is public.
