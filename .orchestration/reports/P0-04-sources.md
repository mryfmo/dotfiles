# P0-04 primary-source evidence

Retrieved: 2026-09-23 (all items). Method: WebFetch of the URL shown (WebSearch used only to locate pages; one PDF parsed locally with `pdftotext` after WebFetch saved it). Quotes are verbatim from the fetched page as returned by the fetch tool. Anything not quoted here was not confirmed; "not stated" means the fetched page did not contain the answer.

## 1. Cucumber Gherkin Reference (Rule, tags, `# language:`, Scenario Outline/Examples, Background)

URL: https://cucumber.io/docs/gherkin/reference/ (tags detail: https://cucumber.io/docs/cucumber/api/)
Retrieved: 2026-09-23
Quote:
> The (optional) `Rule` keyword has been part of Gherkin since v6. The purpose of the `Rule` keyword is to represent one _business rule_ that should be implemented. It provides additional information for a feature. A `Rule` is used to group together several scenarios that belong to this _business rule_. A `Rule` should contain one or more scenarios that illustrate the particular rule.

> Background is also supported at the `Rule` level

> A `# language:` header on the first line of a feature file tells Cucumber what spoken language to use.

> The `Scenario Outline` keyword can be used to run the same `Scenario` multiple times, with different combinations of values.

> A `Scenario Outline` must contain one or more `Examples` (or `Scenarios`) section(s).

> A `Background` allows you to add some context to the scenarios that follow it. It can contain one or more `Given` steps.

> You can place tags above `Feature` to group related features, independent of your file and directory structure.

From https://cucumber.io/docs/cucumber/api/ (Tags section):
> A feature or scenario can have as many tags as you like. Separate them with spaces.

> Tags are inherited by child elements. So, tags that are placed above a `Feature` will be inherited by `Rule`, `Scenario`, `Scenario Outline`, or `Examples`.

> It is _not_ possible to place tags above `Background` or steps (`Given`, `When`, `Then`, `And` and `But`).

Notes: Tag placement: Feature, Rule, Scenario, Scenario Outline, Examples. Example tags shown on the page: `@billing @bicker @annoy`, `@fast`, `@wip and not @slow`, `@smoke and @fast`, `@gui or @database`. **Allowed characters / whether hyphens are permitted in tag names: not stated** on either page (no hyphenated tag example was found either). Status: ok except the hyphen question (not stated).

## 2. gherkin-official on PyPI

URL: https://pypi.org/project/gherkin-official/
Retrieved: 2026-09-23
Quote:
> gherkin-official 42.0.1

> Released: Aug 5, 2026

> Requires: Python >=3.10

Notes: Latest version 42.0.1, released 2026-08-05, Python >=3.10. Status: ok.

## 3. pytest-bdd docs (Rule, tags→markers, `--strict-markers`, version)

URL: https://pytest-bdd.readthedocs.io/en/latest/ (version from https://pypi.org/project/pytest-bdd/)
Retrieved: 2026-09-23
Quote:
> Rule keyword can be used in feature files (see [Rule](https://cucumber.io/docs/gherkin/reference/#rule))

> pytest-bdd uses pytest markers as a *storage* of the tags for the given scenario test, so we can use standard test selection

> The feature and scenario markers are not different from standard pytest markers, and the `@` symbol is stripped out automatically to allow test selector expressions.

> Note that if you use pytest with the `--strict-markers` option, all Gherkin tags mentioned in the feature files should be also in the `markers` setting of the `pytest.ini` config.

Notes: The docs landing page shows no explicit version number ("stable" badge only). PyPI: pytest-bdd 8.1.0, Released Dec 5, 2024. Status: ok.

## 4. mutmut 3 docs (what is mutated / trampoline, `[tool.mutmut]`, version)

URL: https://mutmut.readthedocs.io/ and https://mutmut.readthedocs.io/en/latest/ ; README: https://raw.githubusercontent.com/boxed/mutmut/main/README.rst ; version: https://pypi.org/project/mutmut/
Retrieved: 2026-09-23
Quote:
> By default mutmut mutates all python files in *source_paths*.

> The entire node (including all children) is skipped and no trampoline is generated

> Skipping an entire function or class – place the pragma inline on the definition line.

> Skipping only the body of a function – place the pragma on its own line inside the function.

> Every line between the markers (inclusive) is suppressed. This works inside functions, classes, or at module level, and ignores indentation entirely.

Configuration example (verbatim from docs):
> ```toml
> [tool.mutmut]
> source_paths = [ "src/" ]
> pytest_add_cli_args_test_selection= [ "tests/" ]
> ```

> Mutmut's main process imports pytest and runs your test suite to collect stats, then forks one child per mutant.

PyPI:
> mutmut 3.8.0

> Released: Sep 12, 2026

> Requires: Python >=3.10

Notes: Config keys listed on the docs page: `source_paths`, `pytest_add_cli_args_test_selection`, `also_copy`, `max_stack_depth`, `only_mutate`, `do_not_mutate`, `mutate_only_covered_lines`, `type_check_command`, `debug`, `use_setproctitle`, `process_isolation`, `forkserver_warmup`, `preload_modules_file`. The keys `paths_to_mutate`, `tests_dir` and `runner` are NOT mentioned on the current docs page (the current key is `source_paths`). The word "trampoline" appears only in the pragma text quoted above; **an explicit statement that module-level constants/assignments are not mutated (the trampoline design rationale) is not stated** in the fetched docs or README. Status: ok (config, version); not stated (module-level-constant mutation rule).

## 5. coverage.py (branch coverage, JSON report fields, combined percent)

URL: https://coverage.readthedocs.io/en/latest/branch.html ; https://coverage.readthedocs.io/en/latest/commands/cmd_json.html ; https://coverage.readthedocs.io/en/latest/config.html ; source: https://raw.githubusercontent.com/nedbat/coveragepy/master/coverage/jsonreport.py and https://raw.githubusercontent.com/nedbat/coveragepy/master/coverage/results.py
Retrieved: 2026-09-23
Quote (branch.html):
> Where a line in your program could jump to more than one next line, coverage.py tracks which of those destinations are actually visited.

> To measure branch coverage, run coverage.py with the `--branch` flag: `coverage run --branch myprog.py`

> When you report on the results with `coverage report` or `coverage html`, the percentage of branch possibilities taken will be included in the percentage covered total for each file.

> The coverage percentage for a file is the actual executions divided by the execution opportunities. Each line in the file is an execution opportunity, as is each branch destination.

Quote (config.html, `[json]`):
> Settings particular to JSON reporting. The settings in the `[report]` section also apply to JSON output, where appropriate. Added in version 5.0.

Quote (coverage/jsonreport.py, master):
> ```python
> "covered_lines": nums.n_executed,
> "num_statements": nums.n_statements,
> "percent_covered": nums.pc_covered,
> "percent_covered_display": nums.pc_covered_str,
> "missing_lines": nums.n_missing,
> "excluded_lines": nums.n_excluded,
> "percent_statements_covered": nums.pc_statements,
> "percent_statements_covered_display": nums.pc_statements_str,
> ```
> ```python
> "num_branches": nums.n_branches,
> "num_partial_branches": nums.n_partial_branches,
> "covered_branches": nums.n_executed_branches,
> "missing_branches": nums.n_missing_branches,
> "percent_branches_covered": nums.pc_branches,
> "percent_branches_covered_display": nums.pc_branches_str,
> ```

Quote (coverage/results.py, master):
> ```python
> @property
> def ratio_covered(self) -> tuple[int, int]:
>     """Return a numerator and denominator for the coverage ratio."""
>     numerator = self.n_executed + self.n_executed_branches
>     denominator = self.n_statements + self.n_branches
>     return numerator, denominator
> ```
> ```python
> @property
> def pc_covered(self) -> float:
>     """Returns a single percentage value for coverage."""
>     return self._percent(*self.ratio_covered)
> ```

Notes: The cmd_json.html page documents only CLI options (`-o`, `--pretty-print`, `--fail-under`, `--include`, `--omit`, `--show-contexts`); the JSON field list is **not documented on the docs pages** and was taken from the source. `percent_covered` = (executed statements + executed branches) / (statements + branches), i.e. it combines lines and branches when branch data exists; `percent_statements_covered` / `percent_branches_covered` are the separate figures. PyPI: coverage 7.16.1, Released Sep 13, 2026. Status: ok (fields from source; docs page not stated).

## 6. Hypothesis (`derandomize`, `database`, reproducibility, `.hypothesis`)

URL: https://hypothesis.readthedocs.io/en/latest/reference/api.html ; https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html (https://hypothesis.readthedocs.io/en/latest/settings.html and .../database.html fetched but returned empty bodies)
Retrieved: 2026-09-23
Quote (reference/api.html):
> derandomize: If True, seed Hypothesis' random number generator using a hash of the test function, so that every run will test the same set of test cases until you update Hypothesis, Python, or the test function.

> database: An instance of ExampleDatabase in which we will save failing test cases, and from which we will load previous failing test cases.

Quote (tutorial/replaying-failures.html):
> When a test fails, Hypothesis automatically saves the failure so it can be replayed later.

> Hypothesis saves failures to the `settings.database` setting. By default, this is a `DirectoryBasedExampleDatabase` in the local `.hypothesis` directory.

> On future runs, Hypothesis retries any failing inputs (in `Phase.explain`) before generating new inputs (in `Phase.generate`)

Notes: The api page (paraphrased by the fetch tool, not verbatim) says `derandomize` defaults to False and is set to True under CI, and that with no database configured a `DirectoryBasedExampleDatabase` is created in `.hypothesis/examples`, falling back to in-memory if that location is unwritable; `database=None` disables persistence. The legacy URLs `settings.html` and `database.html` rendered empty (treat as unreachable). PyPI: hypothesis 6.168.1, Released Sep 23, 2026. Status: ok.

## 7. pytest (`--strict-markers`, markers in pyproject.toml, JUnit `time`)

URL: https://docs.pytest.org/en/stable/how-to/mark.html ; https://docs.pytest.org/en/stable/reference/customize.html ; https://docs.pytest.org/en/stable/how-to/output.html
Retrieved: 2026-09-23
Quote (how-to/mark.html):
> When the `strict_markers` configuration option is set, any unknown marks applied with the `@pytest.mark.name_of_the_mark` decorator will trigger an error.

> You can register custom marks in your configuration file like this:
> ```
> [pytest]
> markers = [
> "slow: marks tests as slow (deselect with '-m \"not slow\"')",
> "serial",
> ]
> ```
> ```
> [pytest]
> addopts = ["--strict-markers"]
> markers = [
> "slow: marks tests as slow (deselect with '-m \"not slow\"')",
> "serial",
> ]
> ```

> Note that everything past the `:` after the mark name is an optional description.

Quote (reference/customize.html):
> Use `[tool.pytest.ini_options]` for INI-style configuration (supported since pytest 6.0):
> ```
> # pyproject.toml
> [tool.pytest.ini_options]
> minversion = "6.0"
> addopts = "-ra -q"
> testpaths = [
> "tests",
> "integration",
> ]
> ```

Quote (how-to/output.html):
> JUnit XML specification seems to indicate that "time" attribute should report total test execution times, including setup and teardown. It is the default pytest behavior.

> To report just call durations instead, configure the `junit_duration_report` option like this
> ```
> [pytest]
> junit_duration_report = "call"
> ```

Notes: The `[pytest]` TOML examples on mark.html are the native `[pytest]` table of pytest 9 (`pytest.toml`); `[tool.pytest.ini_options]` in pyproject.toml is the INI-style equivalent. PyPI: pytest 9.1.1, Released Jun 19, 2026. Status: ok.

## 8. Grafana k6 (constant-arrival-rate, thresholds with tags, dropped_iterations, ramp-up, open vs closed)

URL: https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/constant-arrival-rate/ ; https://grafana.com/docs/k6/latest/using-k6/thresholds/ ; https://grafana.com/docs/k6/latest/using-k6/metrics/reference/ ; https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/dropped-iterations/ ; https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/arrival-rate-vu-allocation/ ; https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/ ; https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ramping-arrival-rate/ ; https://grafana.com/docs/k6/latest/testing-guides/test-types/load-testing/
Retrieved: 2026-09-23
Quote (constant-arrival-rate):
> an open-model executor, meaning iterations start independently of system response.

> duration — Total scenario duration (excluding `gracefulStop`).
> rate — Number of iterations to start during each `timeUnit` period.
> preAllocatedVUs — Number of VUs to pre-allocate before test start to preserve runtime resources.
> timeUnit — Period of time to apply the `rate` value. (default `"1s"`)
> maxVUs — Maximum number of VUs to allow during the test run.

Quote (thresholds):
> ```javascript
> export const options = {
>   thresholds: {
>     'http_req_duration{type:API}': ['p(95)<500'],
>     'http_req_duration{type:staticContent}': ['p(95)<200'],
>   },
> };
> ```

Quote (metrics reference):
> dropped_iterations — The number of iterations that weren't started due to lack of VUs (for the arrival-rate executors) or lack of time (expired maxDuration in the iteration-based executors).

Quote (dropped-iterations):
> Sometimes, a scenario can't run the expected number of iterations. k6 tracks the number of unsent iterations in a counter metric, `dropped_iterations`.

> Dropped iterations usually happen for one of two reasons: The executor configuration is insufficient. The SUT can't handle the configured VU arrival rate.

> consider what an acceptable rate of dropped iterations is (the *error budget*). To assert that the SUT responds within this error budget, you can use the `dropped_iterations` metric in a Threshold.

Quote (arrival-rate-vu-allocation):
> Allocating VUs has CPU and memory costs, and allocating VUs as the test runs can overload the load generator and skew results.

> If the executor has insufficient VUs, k6 emits a `dropped_iterations` metric for each iteration that it can't run.

Quote (open-vs-closed):
> In a closed model, the execution time of each iteration dictates the number of iterations executed in your test. The next iteration doesn't start until the previous one finishes.

> The open model decouples VU iterations from the iteration duration. The response times of the target system no longer influence the load on the target system.

Quote (ramping-arrival-rate):
> With the `ramping-arrival-rate` executor, k6 starts iterations at a variable rate. It is an open-model executor, meaning iterations start independently of system response.

> stages — Array of objects that specify the target number of iterations to ramp up or down to.

Quote (load-testing guide, ramp-up):
> Gradually increase load to the target average. That is, use a *ramp-up period*.

> It gives your system time to warm up or auto-scale to handle the traffic.

> ```
> stages: [
>     { duration: '5m', target: 100 }, // traffic ramp-up from 1 to 100 users over 5 minutes.
>     { duration: '30m', target: 100 }, // stay at 100 users for 30 minutes
>     { duration: '5m', target: 0 }, // ramp-down to 0 users
>   ],
> ```

Notes: Threshold expression form is `"<aggregation_method> <operator> <value>"`; sub-metric form is `'metric_name{tag_name:tag_value}'` (so `http_req_duration{op:decide}` follows the documented pattern). Load-testing guide also says the ramp-up "usually lasts between 5% and 15% of the total test duration". Status: ok.

## 9. Playwright (Best Practices isolation; Authentication storageState per worker vs per test)

URL: https://playwright.dev/docs/best-practices ; https://playwright.dev/docs/auth
Retrieved: 2026-09-23
Quote (best-practices):
> Each test should be completely isolated from another test and should run independently with its own local storage, session storage, data, cookies etc.

> Test isolation improves reproducibility, makes debugging easier and prevents cascading test failures.

Quote (auth):
> Tests can load existing authenticated state. This elimination of need to authenticate in every test speeds up test execution.

> Create `tests/auth.setup.ts` that will prepare authenticated browser state for all other tests.

> All testing projects should use the authenticated state as `storageState`.

> We will authenticate once per worker process, each with a unique account.

Notes: The auth page's "Basic: shared account in all tests" uses a setup project + `storageState`; "Moderate: one account per parallel worker" uses `testInfo.parallelIndex` as the per-worker identifier; the multiple-roles section sets `storageState` per test file / test group. Status: ok.

## 10. MADR 4.0.0 (front matter fields and sections)

URL: https://adr.github.io/madr/ ; https://raw.githubusercontent.com/adr/madr/4.0.0/template/adr-template.md
Retrieved: 2026-09-23
Quote (adr.github.io/madr):
> 2024-09-17: Release of MADR 4.0.0

Quote (template, 4.0.0 tag, verbatim front matter and headings):
> ```
> ---
> # These are optional metadata elements. Feel free to remove any of them.
> status: "{proposed | rejected | accepted | deprecated | … | superseded by ADR-0123"
> date: {YYYY-MM-DD when the decision was last updated}
> decision-makers: {list everyone involved in the decision}
> consulted: {list everyone whose opinions are sought (typically subject-matter experts); and with whom there is a two-way communication}
> informed: {list everyone who is kept up-to-date on progress; and with whom there is a one-way communication}
> ---
> # {short title, representative of solved problem and found solution}
> ## Context and Problem Statement
> ## Decision Drivers            <!-- optional -->
> ## Considered Options
> ## Decision Outcome
> ### Consequences               <!-- optional -->
> ### Confirmation               <!-- optional -->
> ## Pros and Cons of the Options <!-- optional -->
> ## More Information            <!-- optional -->
> ```

Notes: Front matter fields: `status`, `date`, `decision-makers`, `consulted`, `informed` (all optional). Decision Outcome line: `Chosen option: "{title of option 1}", because {justification...}`. Consequences use `* Good, because` / `* Bad, because`; option pros/cons additionally use `* Neutral, because`. Status: ok.

## 11. Azure Well-Architected ADR guidance (append-only, supersede)

URL: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
Retrieved: 2026-09-23 (page ms.date 2026-04-10)
Quote:
> The ADR serves as an append-only log. Don't go back and edit accepted records. If a decision changes, write a new record that supersedes the original and link the two together. This approach preserves the history of your thinking and makes it clear when and why the direction shifted.

> Status, such as *Proposed*, *Accepted*, or *Superseded*. Tracking status makes the current state of each decision clear, especially as the number of decisions grows.

Notes: Page also lists record elements: problem statement with context, options considered, decision outcome (tradeoffs, confidence level), status. Status: ok.

## 12. EARS (Alistair Mavin) requirement templates

URL: https://alistairmavin.com/ears/
Retrieved: 2026-09-23
Quote:
> Ubiquitous: The <system name> shall <system response>
> State driven: While <precondition(s)>, the <system name> shall <system response>
> Event driven: When <trigger>, the <system name> shall <system response>
> Optional feature: Where <feature is included>, the <system name> shall <system response>
> Unwanted behaviour: If <trigger>, then the <system name> shall <system response>
> Complex: While <precondition(s)>, When <trigger>, the <system name> shall <system response>

Notes: Six templates as listed on the page. Status: ok.

## 13. Python `tomllib` (added 3.11); PEP 723 `requires-python`

URL: https://docs.python.org/3/library/tomllib.html ; https://peps.python.org/pep-0723/
Retrieved: 2026-09-23
Quote (tomllib):
> Added in version 3.11.

> This module provides an interface for parsing TOML 1.0.0 (Tom's Obvious Minimal Language, https://toml.io).

Quote (PEP 723):
> `requires-python`: A string that specifies the Python version(s) with which the script is compatible. The value of this field MUST be a valid version specifier.

> `dependencies`: A list of strings that specifies the runtime dependencies of the script. Each entry MUST be a valid PEP 508 dependency.

> ```
> # /// script
> # requires-python = ">=3.11"
> # dependencies = [
> #   "requests<3",
> #   "rich",
> # ]
> # ///
> ```

Notes: Status: ok.

## 14. Mermaid (accTitle/accDescr, diagram keywords, securityLevel, latest version)

URL: https://mermaid.js.org/config/accessibility.html ; https://mermaid.js.org/intro/syntax-reference.html ; https://mermaid.js.org/syntax/stateDiagram.html ; https://mermaid.js.org/config/schema-docs/config.html ; https://registry.npmjs.org/mermaid/latest ; https://github.com/mermaid-js/mermaid/releases (https://www.npmjs.com/package/mermaid returned HTTP 403)
Retrieved: 2026-09-23
Quote (accessibility):
> The **accessible title** is specified with the **accTitle** _keyword_, followed by a colon (`:`), and the string value for the title.

> The **single line accessible description** is specified with the **accDescr** _keyword_, followed by a colon (`:`), followed by the string value for the description.

> A **multiple line accessible description** _does not have a colon (`:`) after the accDescr keyword_ and is surrounded by curly brackets (`{}`).

Quote (syntax-reference / stateDiagram): keywords shown on the pages: `flowchart`, `sequenceDiagram`, `erDiagram`; state diagram page's first example begins
> ```
> stateDiagram-v2
>     [*] --> Still
> ```
> and the older form is introduced with "Older renderer:" followed by a block beginning `stateDiagram`.

Quote (securityLevel, config schema):
> Level of trust for parsed diagram
> strict — (**default**) HTML tags in the text are encoded and click functionality is disabled.
> loose — HTML tags in text are allowed and click functionality is enabled.
> antiscript — HTML tags in text are allowed (only script elements are removed), and click functionality is enabled.
> sandbox — With this security level, all rendering takes place in a sandboxed iframe. This prevent any JavaScript from running in the context. This may hinder interactive functionality of the diagram, like scripts, popups in the sequence diagram, or links to other tabs or targets, etc.

Quote (npm registry `mermaid/latest`):
> "version": "12.0.0"

Notes: GitHub releases page lists `mermaid@12.0.0` dated "10 Sep 07:33" (year not printed on the page; the release notes describe ELK as bundled default layout engine and a Node 22.12+ requirement). Status: ok.

## 15. ISTQB CTFL v4.0 test levels

URL: https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/ (landing page; no list) → syllabus PDF https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf (fetched, then parsed with `pdftotext`)
Retrieved: 2026-09-23
Quote (syllabus v4.0.1, 2024-09-15, section 2.2.1 "Test Levels", page 28):
> In this syllabus, the following five test levels are described:
> • Component testing (also known as unit testing) focuses on testing components in isolation. [...]
> • Component integration testing (also known as unit integration testing) focuses on testing the interfaces and interactions between components. [...]
> • System testing focuses on the overall behavior and capabilities of an entire system or product, often including functional testing of end-to-end tasks and the non-functional testing of quality characteristics. [...]
> • System integration testing focuses on testing the interfaces of the system under test and other systems and external services. [...]
> • Acceptance testing focuses on validation and on demonstrating readiness for deployment, which means that the system fulfills the user's business needs. [...]

Notes: The certification landing page itself only names the section "Test Levels & Test Types" and links "ISTQB CTFL Syllabus v4.0.1"; the list is in the PDF (footer: "v4.0.1 ... 2024-09-15"). Status: ok.

## 16. Latest versions (PyPI / npm)

Retrieved: 2026-09-23. PyPI values are the version and "Released:" date printed on the project page. npm values are `version` from `https://registry.npmjs.org/<pkg>/latest`; the npmjs.com pages returned HTTP 403 and the full registry documents were truncated before the `time` map, so npm publish dates are taken from the project's GitHub releases page where the page printed a date string (year is not printed on those pages).

| Package | Source URL | Version | Date as shown |
|---|---|---|---|
| pytest | https://pypi.org/project/pytest/ | 9.1.1 | Jun 19, 2026 |
| hypothesis | https://pypi.org/project/hypothesis/ | 6.168.1 | Sep 23, 2026 |
| pytest-bdd | https://pypi.org/project/pytest-bdd/ | 8.1.0 | Dec 5, 2024 |
| coverage | https://pypi.org/project/coverage/ | 7.16.1 | Sep 13, 2026 |
| mutmut | https://pypi.org/project/mutmut/ | 3.8.0 | Sep 12, 2026 |
| playwright (python) | https://pypi.org/project/playwright/ | 1.63.0 | Sep 15, 2026 |
| testcontainers (python) | https://pypi.org/project/testcontainers/ | 4.15.0 | Jul 24, 2026 |
| pact-python | https://pypi.org/project/pact-python/ | 3.4.1 | Sep 17, 2026 |
| schemathesis | https://pypi.org/project/schemathesis/ | 4.28.0 | Sep 22, 2026 |
| import-linter | https://pypi.org/project/import-linter/ | 2.15 | Sep 4, 2026 |
| time-machine | https://pypi.org/project/time-machine/ | 3.5.1 | Sep 8, 2026 |
| inspect-ai | https://pypi.org/project/inspect-ai/ | 0.3.268 | Sep 22, 2026 |
| deepeval | https://pypi.org/project/deepeval/ | 4.2.5 | Sep 22, 2026 |
| gherkin-official | https://pypi.org/project/gherkin-official/ | 42.0.1 | Aug 5, 2026 |
| @playwright/test | https://registry.npmjs.org/@playwright/test/latest | 1.63.0 | not stated (registry `time` truncated; GitHub releases tag v1.63.0, date not reliably read) |
| @cucumber/cucumber | https://registry.npmjs.org/@cucumber/cucumber/latest ; https://github.com/cucumber/cucumber-js/releases | 13.2.1 | "04 Aug 07:19" (GitHub releases; year not printed) |
| vitest | https://registry.npmjs.org/vitest/latest | 5.0.1 | not stated (registry `time` truncated) |
| fast-check | https://registry.npmjs.org/fast-check/latest ; https://github.com/dubzzz/fast-check/releases | 4.10.2 | "19:31" on Sep 19 per GitHub releases (year not printed) |
| @stryker-mutator/core | https://registry.npmjs.org/@stryker-mutator/core/latest ; https://github.com/stryker-mutator/stryker-js/releases | 10.0.0 | "14 Aug 16:46" (GitHub releases; year not printed) |
| promptfoo | https://registry.npmjs.org/promptfoo/latest ; https://github.com/promptfoo/promptfoo/releases | 0.123.1 | Sep 18 per GitHub releases (year not printed) |
| @axe-core/playwright | https://registry.npmjs.org/@axe-core/playwright/latest ; https://github.com/dequelabs/axe-core-npm/releases | 4.13.0 | "17:24 UTC" Aug 11 per GitHub releases (year not printed) |
| dependency-cruiser | https://registry.npmjs.org/dependency-cruiser/latest | 18.4.0 | not stated (registry `time` truncated) |
| mermaid | https://registry.npmjs.org/mermaid/latest ; https://github.com/mermaid-js/mermaid/releases | 12.0.0 | "10 Sep 07:33" (GitHub releases; year not printed) |

Notes: Version strings are reliable (direct `latest` documents). For npm publish dates, cite only the version unless a later task re-fetches `time[<version>]` (e.g. `npm view <pkg> time --json`). The fetch tool's year guesses for GitHub release pages were inconsistent and are deliberately omitted.

## Status table

| Item | Topic | Status |
|---|---|---|
| 1 | Gherkin reference (Rule, `# language:`, Outline/Examples, Background) | ok; tag character set / hyphens: not stated |
| 2 | gherkin-official PyPI | ok |
| 3 | pytest-bdd docs | ok (docs page shows no version; version from PyPI) |
| 4 | mutmut 3 docs | ok (config keys, version); module-level-constant mutation rule / trampoline rationale: not stated |
| 5 | coverage.py branch + JSON | ok (JSON fields from source code; not documented on docs pages) |
| 6 | Hypothesis settings/database | ok via reference/api.html + tutorial; legacy settings.html / database.html: unreachable (empty body) |
| 7 | pytest markers / JUnit time | ok |
| 8 | k6 | ok |
| 9 | Playwright | ok |
| 10 | MADR 4.0.0 | ok |
| 11 | Azure WAF ADR | ok |
| 12 | EARS | ok |
| 13 | tomllib / PEP 723 | ok |
| 14 | Mermaid | ok (npmjs.com page: unreachable 403; version from registry + GitHub releases) |
| 15 | ISTQB CTFL v4.0 test levels | ok (from syllabus PDF v4.0.1; landing page: not stated) |
| 16 | Latest versions | ok for all version strings; npm publish dates: partially not stated (see table) |
