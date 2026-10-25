// The installed omp's own bash.patterns matcher, run on a policy file and a list of commands (regime-cutover U76).
//
// omp 18.12.6 (as 18.11.3) keeps the matcher private in src/tools/bash.ts, so this script copies its declarations out of the
// installed source at run time (from `const BASH_APPROVAL_SHELL_CONTROL_CHARS` through `hasBashApprovalShellControl`,
// and from `type BashPatternApproval` through `findBashApprovalPatternRule`), imports the installed
// `tokenizeShellSegments`, and asks `findBashApprovalPatternRule` for each command's first matching rule. A missing
// block is an error, never a fallback.
// Usage: bun installed-matcher.ts <pi-coding-agent package dir> <policy.yml> <commands.json>
// Prints one JSON array: the matching rule's approval per command, or null when no rule matches.
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

const [pkg, policyPath, commandsPath] = process.argv.slice(2);
const source = fs.readFileSync(path.join(pkg, "src/tools/bash.ts"), "utf8");

function block(start: string, endFunction: string): string {
	const from = source.indexOf(start);
	const to = source.indexOf(`function ${endFunction}(`, from);
	if (from < 0 || to < 0) throw new Error(`installed bash.ts lacks ${start} .. ${endFunction}`);
	const close = source.indexOf("\n}\n", to);
	if (close < 0) throw new Error(`installed bash.ts: ${endFunction} has no closing brace`);
	return source.slice(from, close + 3);
}

const values = source.match(/const BASH_PATTERN_APPROVAL_VALUES = [^\n]*\n/);
if (!values) throw new Error("installed bash.ts lacks BASH_PATTERN_APPROVAL_VALUES");
const module = [
	`import { tokenizeShellSegments } from ${JSON.stringify(path.join(pkg, "src/tools/shell-tokenize.ts"))};`,
	block("const BASH_APPROVAL_SHELL_CONTROL_CHARS", "hasBashApprovalShellControl"),
	values[0],
	block("type BashPatternApproval", "findBashApprovalPatternRule"),
	"export { getBashApprovalPatternRules, findBashApprovalPatternRule };",
].join("\n");
const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "omp-matcher-")), "matcher.ts");
fs.writeFileSync(file, module);
// A runtime import: the module is the matcher source copied out of the installed package above, written per run.
const { getBashApprovalPatternRules, findBashApprovalPatternRule } = await import(file);

const policy = Bun.YAML.parse(fs.readFileSync(policyPath, "utf8")) as { bash?: { patterns?: unknown } };
const rules = getBashApprovalPatternRules(policy.bash?.patterns);
const commands = JSON.parse(fs.readFileSync(commandsPath, "utf8")) as string[];
console.log(JSON.stringify(commands.map(command => findBashApprovalPatternRule(command, rules)?.approval ?? null)));
