# Validation: dot-main-push-guard-revert-T60-a01

## Task validation commands on the final head (verbatim)

```
$ git log --oneline origin/main..HEAD
8259cf5c fix(herdr-agents): keep stub cleanup inside the common git dir; fresh boundary branches
4445917b fix(herdr-agents): remove only the exact retired stub, at the configured hooks path
560df81b chore(orchestration): retire the main-push guard; the GitHub ruleset is the boundary
$ git diff origin/main --stat
 README.md                                          |  14 +-
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   4 +-
 .../dot_config/claude/rules/agmsg-orchestration.md |   2 +-
 home/dot_local/bin/common/executable_herdr-agents  | 187 +++---------
 tests/unit/test_agmsg_orchestration_docs.py        |   2 +-
 tests/unit/test_herdr_agents.py                    | 313 +++++----------------
 6 files changed, 121 insertions(+), 401 deletions(-)
(exit 0)
$ grep -rn 'ORCH_PUSH_MAIN\|main-push-guard\|main_push_guard\|orch-push-main' home scripts tests Makefile README.md AGENTS.md docs; echo "exit=$?"   # residuals: see report section 1
home/dot_local/bin/common/executable_herdr-agents:1579:        rm -f -- "${hook}" "${common_dir}/orch-push-main.log"
tests/unit/test_herdr_agents.py:1330:        '# herdr-agents main-push guard: written by herdr-agents --bootstrap-agmsg; the checks live in herdr-agents --main-push-guard.\n'
tests/unit/test_herdr_agents.py:1332:        'if [[ -x ${guard} && "$("${guard}" --help 2> /dev/null)" == *--main-push-guard* ]]; then\n'
tests/unit/test_herdr_agents.py:1333:        '    exec "${guard}" --main-push-guard "$@"\n'
tests/unit/test_herdr_agents.py:1339:        "        printf 'pre-push: no herdr-agents with --main-push-guard is installed (run make update), so this push to main is refused\\n' >&2\n"
tests/unit/test_herdr_agents.py:1368:                log = self.workdir / ".git/orch-push-main.log"
tests/unit/test_herdr_agents.py:1391:                log = self.workdir / ".git/orch-push-main.log"
exit=0
$ make unit-test
Ran 709 tests in 159.070s

OK (skipped=2)
(exit 0)
$ make validate-agent-assets
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-main-push-guard-revert-T60-a01.md
agent asset validation ok
(exit 0)
$ mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents
(exit 0)
$ shellcheck home/dot_local/bin/common/executable_herdr-agents; bash -n home/dot_local/bin/common/executable_herdr-agents
(exit 0)
$ gh pr checks 231
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37083311850/job/111088316006	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37083311840/job/111088316190	
private-bootstrap (ubuntu-24.04, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37083311840/job/111088316199	
private-bootstrap (ubuntu-24.04, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37083311840/job/111088316194	
public-bootstrap (macos-14, client)	pass	10m53s	https://github.com/mryfmo/dotfiles/actions/runs/37083311840/job/111088316213	
test (macos-14, client)	pass	5m13s	https://github.com/mryfmo/dotfiles/actions/runs/37083311850/job/111088351096	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37083311850/job/111088352080	
public-bootstrap (ubuntu-24.04, client)	pass	6m49s	https://github.com/mryfmo/dotfiles/actions/runs/37083311840/job/111088316192	
public-bootstrap (ubuntu-24.04, server)	pass	5m59s	https://github.com/mryfmo/dotfiles/actions/runs/37083311840/job/111088316047	
test (ubuntu-24.04, client)	pass	7m5s	https://github.com/mryfmo/dotfiles/actions/runs/37083311850/job/111088351115	
test (ubuntu-24.04, server)	pass	4m17s	https://github.com/mryfmo/dotfiles/actions/runs/37083311850/job/111088351168	
test (ubuntu-26.04, client)	pass	7m2s	https://github.com/mryfmo/dotfiles/actions/runs/37083311850/job/111088351117	
validate	pass	15s	https://github.com/mryfmo/dotfiles/actions/runs/37083311830/job/111088315944	
(exit 0)
$ gh api repos/mryfmo/dotfiles/pulls/231 --jq '.mergeable_state'
blocked
$ gh api repos/mryfmo/dotfiles/pulls/231 --jq '.head.sha, .base.sha'; git rev-parse origin/main   # branch up to date with main
8259cf5c6870d95a7dbb6719640c0485a15ccc6e
0a812d30ab76de97ea41ed2678ff57d9fde81585
0a812d30ab76de97ea41ed2678ff57d9fde81585
origin/main is an ancestor of HEAD
$ gh api graphql ... reviewThreads (isResolved, isOutdated, author, path, commit)
resolved=false outdated=true 560df81b home/dot_local/bin/common/executable_herdr-agents | Preserve customized copies of the retired hook**
resolved=false outdated=true 560df81b home/dot_local/bin/common/executable_herdr-agents | Resolve the configured hooks directory before cleanup**
resolved=false outdated=false 4445917b home/dot_local/bin/common/executable_herdr-agents | Preserve hooks outside Git's common directory**
resolved=false outdated=true 4445917b home/dot_agents/skills/agmsg-orchestration/SKILL.md | Use a fresh branch for every boundary**
resolved=false outdated=false 4445917b home/dot_local/bin/common/executable_herdr-agents | Scope guard retirement to repositories with the ruleset**
```

## Deployed stub recognition (this machine, read-only)

```
$ git hash-object <old installer body from origin/main~ (0a812d30)> ~/Workspace/dotfiles/.git/hooks/pre-push ~/.local/share/chezmoi/.git/hooks/pre-push
af94a0b55e08a02423f72f3d4f713a4a804d905e
af94a0b55e08a02423f72f3d4f713a4a804d905e
af94a0b55e08a02423f72f3d4f713a4a804d905e
$ grep -n stub_blob home/dot_local/bin/common/executable_herdr-agents | head -1
1571:    local stub_blob=af94a0b55e08a02423f72f3d4f713a4a804d905e
```

## Applied ruleset (read-only)

```
$ gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '{name,enforcement,rules:[.rules[].type]}'
unknown shorthand flag: 'c' in -c

Makes an authenticated HTTP request to the GitHub API and prints the response.

The endpoint argument should either be a path of a GitHub API v3 endpoint, or
`graphql` to access the GitHub API v4.

Placeholder values `{owner}`, `{repo}`, and `{branch}` in the endpoint
argument will get replaced with values from the repository of the current
directory or the repository specified in the `GH_REPO` environment variable.
Note that in some shells, for example PowerShell, you may need to enclose
any value that contains `{...}` in quotes to prevent the shell from
applying special meaning to curly braces.

The `-p/--preview` flag enables opting into previews, which are feature-flagged,
experimental API endpoints or behaviors. The API expects opt-in via the `Accept`
header with format `application/vnd.github.<preview-name>-preview+json` and this
command facilitates that via `--preview <preview-name>`. To send a request for
the corsair and scarlet witch previews, you could use `-p corsair,scarlet-witch`
or `--preview corsair --preview scarlet-witch`.

The default HTTP request method is `GET` normally and `POST` if any parameters
were added. Override the method with `--method`.

Pass one or more `-f/--raw-field` values in `key=value` format to add static string
parameters to the request payload. To add non-string or placeholder-determined values, see
`-F/--field` below. Note that adding request parameters will automatically switch the
request method to `POST`. To send the parameters as a `GET` query string instead, use
`--method GET`.

The `-F/--field` flag has magic type conversion based on the format of the value:

- literal values `true`, `false`, `null`, and integer numbers get converted to
  appropriate JSON types;
- placeholder values `{owner}`, `{repo}`, and `{branch}` get populated with values
  from the repository of the current directory;
- if the value starts with `@`, the rest of the value is interpreted as a
  filename to read the value from. Pass `-` to read from standard input.

For GraphQL requests, all fields other than `query` and `operationName` are
interpreted as GraphQL variables.

To pass nested parameters in the request payload, use `key[subkey]=value` syntax when
declaring fields. To pass nested values as arrays, declare multiple fields with the
syntax `key[]=value1`, `key[]=value2`. To pass an empty array, use `key[]` without a
value.

To pass pre-constructed JSON or payloads in other formats, a request body may be read
from file specified by `--input`. Use `-` to read from standard input. When passing the
request body this way, any parameters specified via field flags are added to the query
string of the endpoint URL.

In `--paginate` mode, all pages of results will sequentially be requested until
there are no more pages of results. For GraphQL requests, this requires that the
original query accepts an `$endCursor: String` variable and that it fetches the
`pageInfo{ hasNextPage, endCursor }` set of fields from a collection. Each page is a separate
JSON array or object. Pass `--slurp` to wrap all pages of JSON arrays or objects
into an outer JSON array.

For more information about output formatting flags, see `gh help formatting`.

[0;1;39mUSAGE[0m
  gh api <endpoint> [flags]

[0;1;39mFLAGS[0m
      --allow-escape-sequences   Allow printing terminal escape sequences
      --cache duration           Cache the response, e.g. "3600s", "60m", "1h"
  -F, --field key=value          Add a typed parameter in key=value format (use "@<path>" or "@-" to read value from file or stdin)
  -H, --header key:value         Add a HTTP request header in key:value format
      --hostname string          The GitHub hostname for the request (default "github.com")
  -i, --include                  Include HTTP response status line and headers in the output
      --input file               The file to use as body for the HTTP request (use "-" to read from standard input)
  -q, --jq string                Query to select values from the response using jq syntax
  -X, --method string            The HTTP method for the request (default "GET")
      --paginate                 Make additional HTTP requests to fetch all pages of results
  -p, --preview strings          Opt into GitHub API previews (names should omit '-preview')
  -f, --raw-field key=value      Add a string parameter in key=value format
      --silent                   Do not print the response body
      --slurp                    Use with "--paginate" to return an array of all pages of either JSON arrays or objects
  -t, --template string          Format JSON output using a Go template; see "gh help formatting"
      --verbose                  Include full HTTP request and response in the output

[0;1;39mINHERITED FLAGS[0m
  --help   Show help for command

[0;1;39mEXAMPLES[0m
  # List releases in the current repository
  $ gh api repos/{owner}/{repo}/releases
  
  # Post an issue comment
  $ gh api repos/{owner}/{repo}/issues/123/comments -f body='Hi from CLI'
  
  # Post nested parameter read from a file
  $ gh api gists -F 'files[myfile.txt][content]=@myfile.txt'
  
  # Add parameters to a GET request
  $ gh api -X GET search/issues -f q='repo:cli/cli is:open remote'
  
  # Use a JSON file as request body
  $ gh api repos/{owner}/{repo}/rulesets --input file.json
  
  # Set a custom HTTP header
  $ gh api -H 'Accept: application/vnd.github.v3.raw+json' ...
  
  # Opt into GitHub API previews
  $ gh api --preview baptiste,nebula ...
  
  # Print only specific fields from the response
  $ gh api repos/{owner}/{repo}/issues --jq '.[].title'
  
  # Use a template for the output
  $ gh api repos/{owner}/{repo}/issues --template \
    '{{range .}}{{.title}} ({{.labels | pluck "name" | join ", " | color "yellow"}}){{"\n"}}{{end}}'
  
  # Update allowed values of the "environment" custom property in a deeply nested array
  $ gh api -X PATCH /orgs/{org}/properties/schema \
     -F 'properties[][property_name]=environment' \
     -F 'properties[][default_value]=production' \
     -F 'properties[][allowed_values][]=staging' \
     -F 'properties[][allowed_values][]=production'
  
  # List releases with GraphQL
  $ gh api graphql -F owner='{owner}' -F name='{repo}' -f query='
    query($name: String!, $owner: String!) {
      repository(owner: $owner, name: $name) {
        releases(last: 3) {
          nodes { tagName }
        }
      }
    }
  '
  
  # List all repositories for a user
  $ gh api graphql --paginate -f query='
    query($endCursor: String) {
      viewer {
        repositories(first: 100, after: $endCursor) {
          nodes { nameWithOwner }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
  '
  
  # Get the percentage of forks for the current user
  $ gh api graphql --paginate --slurp -f query='
    query($endCursor: String) {
      viewer {
        repositories(first: 100, after: $endCursor) {
          nodes { isFork }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
  ' | jq 'def count(e): reduce e as $_ (0;.+1);
  [.[].data.viewer.repositories.nodes[]] as $r | count(select($r[].isFork))/count($r[])'

[0;1;39mENVIRONMENT VARIABLES[0m
  GH_TOKEN, GITHUB_TOKEN (in order of precedence): an authentication token for
  `github.com` API requests.
  
  GH_ENTERPRISE_TOKEN, GITHUB_ENTERPRISE_TOKEN (in order of precedence): an
  authentication token for API requests to GitHub Enterprise.
  
  GH_HOST: make the request to a GitHub host other than `github.com`.

[0;1;39mLEARN MORE[0m
  Use `gh <command> <subcommand> --help` for more information about a command.
  Read the manual at https://cli.github.com/manual
  Learn about exit codes using `gh help exit-codes`
  Learn about accessibility experiences using `gh help accessibility`

$ gh api repos/mryfmo/dotfiles --jq '{allow_squash_merge,allow_merge_commit,allow_rebase_merge,allow_auto_merge,delete_branch_on_merge}'
unknown shorthand flag: 'c' in -c

Makes an authenticated HTTP request to the GitHub API and prints the response.

The endpoint argument should either be a path of a GitHub API v3 endpoint, or
`graphql` to access the GitHub API v4.

Placeholder values `{owner}`, `{repo}`, and `{branch}` in the endpoint
argument will get replaced with values from the repository of the current
directory or the repository specified in the `GH_REPO` environment variable.
Note that in some shells, for example PowerShell, you may need to enclose
any value that contains `{...}` in quotes to prevent the shell from
applying special meaning to curly braces.

The `-p/--preview` flag enables opting into previews, which are feature-flagged,
experimental API endpoints or behaviors. The API expects opt-in via the `Accept`
header with format `application/vnd.github.<preview-name>-preview+json` and this
command facilitates that via `--preview <preview-name>`. To send a request for
the corsair and scarlet witch previews, you could use `-p corsair,scarlet-witch`
or `--preview corsair --preview scarlet-witch`.

The default HTTP request method is `GET` normally and `POST` if any parameters
were added. Override the method with `--method`.

Pass one or more `-f/--raw-field` values in `key=value` format to add static string
parameters to the request payload. To add non-string or placeholder-determined values, see
`-F/--field` below. Note that adding request parameters will automatically switch the
request method to `POST`. To send the parameters as a `GET` query string instead, use
`--method GET`.

The `-F/--field` flag has magic type conversion based on the format of the value:

- literal values `true`, `false`, `null`, and integer numbers get converted to
  appropriate JSON types;
- placeholder values `{owner}`, `{repo}`, and `{branch}` get populated with values
  from the repository of the current directory;
- if the value starts with `@`, the rest of the value is interpreted as a
  filename to read the value from. Pass `-` to read from standard input.

For GraphQL requests, all fields other than `query` and `operationName` are
interpreted as GraphQL variables.

To pass nested parameters in the request payload, use `key[subkey]=value` syntax when
declaring fields. To pass nested values as arrays, declare multiple fields with the
syntax `key[]=value1`, `key[]=value2`. To pass an empty array, use `key[]` without a
value.

To pass pre-constructed JSON or payloads in other formats, a request body may be read
from file specified by `--input`. Use `-` to read from standard input. When passing the
request body this way, any parameters specified via field flags are added to the query
string of the endpoint URL.

In `--paginate` mode, all pages of results will sequentially be requested until
there are no more pages of results. For GraphQL requests, this requires that the
original query accepts an `$endCursor: String` variable and that it fetches the
`pageInfo{ hasNextPage, endCursor }` set of fields from a collection. Each page is a separate
JSON array or object. Pass `--slurp` to wrap all pages of JSON arrays or objects
into an outer JSON array.

For more information about output formatting flags, see `gh help formatting`.

[0;1;39mUSAGE[0m
  gh api <endpoint> [flags]

[0;1;39mFLAGS[0m
      --allow-escape-sequences   Allow printing terminal escape sequences
      --cache duration           Cache the response, e.g. "3600s", "60m", "1h"
  -F, --field key=value          Add a typed parameter in key=value format (use "@<path>" or "@-" to read value from file or stdin)
  -H, --header key:value         Add a HTTP request header in key:value format
      --hostname string          The GitHub hostname for the request (default "github.com")
  -i, --include                  Include HTTP response status line and headers in the output
      --input file               The file to use as body for the HTTP request (use "-" to read from standard input)
  -q, --jq string                Query to select values from the response using jq syntax
  -X, --method string            The HTTP method for the request (default "GET")
      --paginate                 Make additional HTTP requests to fetch all pages of results
  -p, --preview strings          Opt into GitHub API previews (names should omit '-preview')
  -f, --raw-field key=value      Add a string parameter in key=value format
      --silent                   Do not print the response body
      --slurp                    Use with "--paginate" to return an array of all pages of either JSON arrays or objects
  -t, --template string          Format JSON output using a Go template; see "gh help formatting"
      --verbose                  Include full HTTP request and response in the output

[0;1;39mINHERITED FLAGS[0m
  --help   Show help for command

[0;1;39mEXAMPLES[0m
  # List releases in the current repository
  $ gh api repos/{owner}/{repo}/releases
  
  # Post an issue comment
  $ gh api repos/{owner}/{repo}/issues/123/comments -f body='Hi from CLI'
  
  # Post nested parameter read from a file
  $ gh api gists -F 'files[myfile.txt][content]=@myfile.txt'
  
  # Add parameters to a GET request
  $ gh api -X GET search/issues -f q='repo:cli/cli is:open remote'
  
  # Use a JSON file as request body
  $ gh api repos/{owner}/{repo}/rulesets --input file.json
  
  # Set a custom HTTP header
  $ gh api -H 'Accept: application/vnd.github.v3.raw+json' ...
  
  # Opt into GitHub API previews
  $ gh api --preview baptiste,nebula ...
  
  # Print only specific fields from the response
  $ gh api repos/{owner}/{repo}/issues --jq '.[].title'
  
  # Use a template for the output
  $ gh api repos/{owner}/{repo}/issues --template \
    '{{range .}}{{.title}} ({{.labels | pluck "name" | join ", " | color "yellow"}}){{"\n"}}{{end}}'
  
  # Update allowed values of the "environment" custom property in a deeply nested array
  $ gh api -X PATCH /orgs/{org}/properties/schema \
     -F 'properties[][property_name]=environment' \
     -F 'properties[][default_value]=production' \
     -F 'properties[][allowed_values][]=staging' \
     -F 'properties[][allowed_values][]=production'
  
  # List releases with GraphQL
  $ gh api graphql -F owner='{owner}' -F name='{repo}' -f query='
    query($name: String!, $owner: String!) {
      repository(owner: $owner, name: $name) {
        releases(last: 3) {
          nodes { tagName }
        }
      }
    }
  '
  
  # List all repositories for a user
  $ gh api graphql --paginate -f query='
    query($endCursor: String) {
      viewer {
        repositories(first: 100, after: $endCursor) {
          nodes { nameWithOwner }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
  '
  
  # Get the percentage of forks for the current user
  $ gh api graphql --paginate --slurp -f query='
    query($endCursor: String) {
      viewer {
        repositories(first: 100, after: $endCursor) {
          nodes { isFork }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
  ' | jq 'def count(e): reduce e as $_ (0;.+1);
  [.[].data.viewer.repositories.nodes[]] as $r | count(select($r[].isFork))/count($r[])'

[0;1;39mENVIRONMENT VARIABLES[0m
  GH_TOKEN, GITHUB_TOKEN (in order of precedence): an authentication token for
  `github.com` API requests.
  
  GH_ENTERPRISE_TOKEN, GITHUB_ENTERPRISE_TOKEN (in order of precedence): an
  authentication token for API requests to GitHub Enterprise.
  
  GH_HOST: make the request to a GitHub host other than `github.com`.

[0;1;39mLEARN MORE[0m
  Use `gh <command> <subcommand> --help` for more information about a command.
  Read the manual at https://cli.github.com/manual
  Learn about exit codes using `gh help exit-codes`
  Learn about accessibility experiences using `gh help accessibility`

```

## CompactionDB (main checkout, unsandboxed)

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T60 (operator 2026-10-03): the GitHub ruleset "main integration gate" is the sole boundary for `main`; the T54 client-side pre-push guard and the `ORCH_PUSH_MAIN` convention are removed, and the `.orchestration` boundary commit travels as a squash-merged PR like every other change.'
b81a4935-5ec0-4c23-9e86-bd202fd610fd
(exit 0)
```

# Revise round 1 (task_rev sha256:36500453…, audit finding on 4445917b live on 8259cf5c)

```
$ sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dot-main-push-guard-revert-T60-a01.md
365004531c5482a380aabfb8d3d15dce861e32e5ed5e3694e44c81602ee87278  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dot-main-push-guard-revert-T60-a01.md
$ git log --oneline origin/main..HEAD
65f54c46 fix(herdr-agents): compare the retired stub on raw bytes (hash-object --no-filters)
8259cf5c fix(herdr-agents): keep stub cleanup inside the common git dir; fresh boundary branches
4445917b fix(herdr-agents): remove only the exact retired stub, at the configured hooks path
560df81b chore(orchestration): retire the main-push guard; the GitHub ruleset is the boundary
$ git diff 8259cf5c HEAD --stat
 home/dot_local/bin/common/executable_herdr-agents | 2 +-
 tests/unit/test_herdr_agents.py                   | 9 +++++++--
 2 files changed, 8 insertions(+), 3 deletions(-)
$ git show HEAD -- home/dot_local/bin/common/executable_herdr-agents | grep "^[-+] "
-    if [[ "$(git -C "${workdir}" hash-object -- "${hook}")" == "${stub_blob}" ]]; then
+    if [[ "$(git -C "${workdir}" hash-object --no-filters -- "${hook}")" == "${stub_blob}" ]]; then
$ (subtest proof) python3 -m unittest <test_bootstrap_leaves_a_foreign_pre_push_hook_alone> with the hash-object line WITHOUT --no-filters
ERROR: test_bootstrap_leaves_a_foreign_pre_push_hook_alone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_leaves_a_foreign_pre_push_hook_alone) (hook='CRLF stub under a text .gitattributes')
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-1000/herdr-agents-test-h6c3bem2/project/.git/hooks/pre-push'
Ran 1 test in 0.138s
FAILED (errors=1)
$ (same) WITH --no-filters
Ran 1 test in 0.141s
OK
$ make unit-test
Ran 709 tests in 159.251s

OK (skipped=2)
(exit 0)
$ gh pr checks 231
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37087943521/job/111101993805	
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37087943519/job/111101993981	
private-bootstrap (ubuntu-24.04, client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37087943519/job/111101993942	
private-bootstrap (ubuntu-24.04, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37087943519/job/111101993776	
public-bootstrap (macos-14, client)	pass	7m0s	https://github.com/mryfmo/dotfiles/actions/runs/37087943519/job/111101993957	
public-bootstrap (ubuntu-24.04, client)	pass	8m58s	https://github.com/mryfmo/dotfiles/actions/runs/37087943519/job/111101993920	
public-bootstrap (ubuntu-24.04, server)	pass	7m38s	https://github.com/mryfmo/dotfiles/actions/runs/37087943519/job/111101993945	
test (macos-14, client)	pass	5m0s	https://github.com/mryfmo/dotfiles/actions/runs/37087943521/job/111102018680	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37087943521/job/111102019233	
test (ubuntu-24.04, client)	pass	7m5s	https://github.com/mryfmo/dotfiles/actions/runs/37087943521/job/111102018703	
test (ubuntu-24.04, server)	pass	3m46s	https://github.com/mryfmo/dotfiles/actions/runs/37087943521/job/111102018641	
test (ubuntu-26.04, client)	pass	7m10s	https://github.com/mryfmo/dotfiles/actions/runs/37087943521/job/111102018655	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37087943555/job/111101993781	
(exit 0)
$ gh api repos/mryfmo/dotfiles/pulls/231 --jq '.head.sha, .mergeable_state'
65f54c4629a500a6f1a8a0ba94d2992e3c055b1c
clean
$ git merge-base --is-ancestor origin/main HEAD && echo up-to-date; git rev-parse --short origin/main
up-to-date
0a812d30
$ gh api graphql ... reviewThreads
resolved=true outdated=true 560df81b home/dot_local/bin/common/executable_herdr-agents | Preserve customized copies of the retired hook**
resolved=true outdated=true 560df81b home/dot_local/bin/common/executable_herdr-agents | Resolve the configured hooks directory before cleanup**
resolved=true outdated=false 4445917b home/dot_local/bin/common/executable_herdr-agents | Preserve hooks outside Git's common directory**
resolved=true outdated=true 4445917b home/dot_agents/skills/agmsg-orchestration/SKILL.md | Use a fresh branch for every boundary**
resolved=true outdated=false 4445917b home/dot_local/bin/common/executable_herdr-agents | Scope guard retirement to repositories with the ruleset**
```

## Orchestrator verification at acceptance (2026-10-03, unsandboxed)

The two `gh api` lines in "Applied ruleset (read-only)" above failed with a gh usage error and prove nothing (Codex Bot P2 on boundary PR #232). The orchestrator ran the queries itself; verbatim successful output:

```
$ gh api repos/mryfmo/dotfiles/rulesets --jq '.[] | {id, name, enforcement}'
{"enforcement":"active","id":24397953,"name":"main integration gate"}
$ gh api repos/mryfmo/dotfiles/rules/branches/main --jq '.[] | .type'
deletion
non_fast_forward
pull_request
required_status_checks
$ gh api repos/mryfmo/dotfiles/rules/branches/main --jq '.[] | select(.type=="pull_request" or .type=="required_status_checks") | .parameters'
{"allowed_merge_methods":["merge","squash","rebase"],"dismiss_stale_reviews_on_push":true,"require_code_owner_review":false,"require_extra_approval_for_unattributed_changes":true,"require_last_push_approval":false,"required_approving_review_count":0,"required_review_thread_resolution":true,"required_reviewers":[]}
{"do_not_enforce_on_create":false,"required_status_checks":[{"context":"validate"},{"context":"test (ubuntu-24.04, server)"},{"context":"test (ubuntu-24.04, client)"},{"context":"test (macos-14, client)"},{"context":"public-bootstrap (ubuntu-24.04, server)"},{"context":"public-bootstrap (ubuntu-24.04, client)"},{"context":"public-bootstrap (macos-14, client)"}],"strict_required_status_checks_policy":true}
$ gh api repos/mryfmo/dotfiles --jq '{allow_squash_merge,allow_merge_commit,allow_rebase_merge,allow_auto_merge,delete_branch_on_merge}'
{"allow_auto_merge":true,"allow_merge_commit":false,"allow_rebase_merge":false,"allow_squash_merge":true,"delete_branch_on_merge":false}
```
