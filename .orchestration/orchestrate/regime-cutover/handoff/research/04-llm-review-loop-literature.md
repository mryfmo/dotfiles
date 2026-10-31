# Research 04. What the literature measures about LLM review loops (read 2026-10-30, JST)

This file answers one question for the loop in [02-audit-treadmill-analysis.md](../02-audit-treadmill-analysis.md): a worker builds a head, a fresh-context LLM auditor judges it against the PR's Contract, an `incorrect` verdict buys a fix round, and the treadmill rule changes the mechanism after three rounds of one class. The question is what peer-reviewed or arXiv work from 2024 to 2026 has measured about such loops, so that the two-strike rule (plan D-10, gate G-21), the brief-time closure check (U104) and the closed-acceptance-set rule (plan D1) rest on measured evidence and not only on the store's own 13 treadmill rows.

Every entry carries the title, venue, year, URL, one or two quoted findings with their numbers, and one line on what it implies for this loop. Quotes are from the abstract or the named section of the paper as read on 2026-10-30; a figure quoted from a table names the table. Venue "arXiv" means no peer-reviewed version was found on that date. Fifteen sources are entered; seven more that were read are listed at the end with one line each.

## Summary against the five questions

| Question                                                     | Entries                                               | One-line answer                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------ | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Judge inconsistency, false positives, panels, biases      | 1, 2, 3, 4                                            | One judge disagrees with itself across runs (alpha 0.27 to 0.56 on MT-Bench); open-ended "is this vulnerable" prompts flag patched code as vulnerable at rates above 88%; position and phrasing artifacts move verdicts; juries and majority votes help but do not remove the sensitivity.                                        |
| 2. Do iterative review or repair loops converge              | 5, 6, 7, 8                                            | Repair loops with an executable oracle plateau after three to four rounds; review loops without one get worse, since a second review of the same artifact adds 62% more false positives, and multi-round review F1 (Claude Haiku 4.5) falls from 0.65 at round 2 to 0.29 at round 10. Revising an already-correct state loses it. |
| 3. Agentic review with execution, precision versus recall    | 9, 10, 11                                             | Judges that execute and read the repository reach about 90% alignment with humans against 60 to 65% for a prompt-only judge; a critic that finds more real bugs also hallucinates more, and the trade-off is explicit; even three human validators per task left 59.4% of the hard tasks with flawed tests.                       |
| 4. Specification-bounded versus open-ended review            | 12, 13 (and 4, 9; the Tencent study in the last list) | A judge without a reference over-credits, and adding one flips up to 85% of verdicts; asked to check conformance to a spec, judges over-reject correct code, and more detailed prompts make it worse; a judge given one bounded question (is this specific alarm real) removes 94 to 98% of false alarms with high recall.        |
| 5. Denylists over shell and the undecidability of shell text | 14, 15                                                | 69.0 to 98.6% of 1,709 real command denylists are fragile, Claude Code's own built-in list included; completing one needs on average 217 more commands; the shell's runtime evaluation, expansion and subshells make ahead-of-time checking of the text intractable without a semantic analysis.                                  |

## 1. Judge inconsistency, false positives, panels, biases

### 1. Rating Roulette: Self-Inconsistency in LLM-As-A-Judge Frameworks

- Venue and year: Findings of EMNLP 2025 (arXiv 2510.27106, 2025). Haldar and Hockenmaier.
- URL: <https://aclanthology.org/2025.findings-emnlp.1361> and <https://arxiv.org/abs/2510.27106>
- Quoted findings:
  - "we show that LLM judges have low intra-rater reliability in their assigned scores across different runs. This variance makes their ratings inconsistent, almost arbitrary in the worst case" (abstract).
  - On MT-Bench, three runs of the same judge with the same prompt and settings: "Llama 3.1 had a Krippendorff's Alpha of 0.265 across its 3 runs, while for Deepseek-R1 it was 0.507. Qwen 3 was the most reliable with a Krippendorff's Alpha of 0.563. Even in the best case, these numbers are much lower than the desired threshold of 0.8" (section 4, MT-Bench).
  - "We see that accuracy is higher when computed via majority vote than the expected accuracy for a single run" (section 5.1).
- Implication for the loop: one fresh audit per head is one sample from a judge whose agreement with itself is well under the 0.8 reliability bar, so a finding that appears in one round and not the next is expected noise, not evidence that the fix round worked or failed. A verdict that gates a merge should be a majority of samples or should rest on a deterministic fact, which is what plan P1 ("one deterministic fact per round") already asks for.

### 2. Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge

- Venue and year: arXiv 2406.07791 (2024, v9 revised November 2025). Shi, Ma, Liang, Diao, Ma, Vosoughi.
- URL: <https://arxiv.org/abs/2406.07791>
- Quoted findings:
  - "Our experiments, involving 15 LLM judges across MTBench and DevBench with 22 tasks and approximately 40 solution-generating models, result in over 150,000 evaluation instances" and "position bias is not due to random chance and varies significantly across judges and tasks" (abstract).
  - "While position bias is weakly influenced by the length of prompt components, it is strongly affected by the quality gap between solutions" (abstract).
- Implication for the loop: the audit prompt's ordering of material (the Contract, the diff, the earlier verdict) is itself a variable the verdict responds to, most strongly when the two things compared are close in quality, which is exactly the state of a head after a fix round. Fixing the prompt order per lever and never pasting the previous verdict into the next audit removes one source of round-to-round drift.

### 3. Safer or Luckier? LLMs as Safety Evaluators Are Not Robust to Artifacts

- Venue and year: ACL 2025, long papers (pages 19750 to 19766). Chen and Goldfarb-Tarrant.
- URL: <https://aclanthology.org/2025.acl-long.970/>
- Quoted findings:
  - "This study evaluates a diverse set of 11 LLM judge models across critical safety domains, examining three key aspects: self-consistency in repeated judging tasks, alignment with human judgments, and susceptibility to input artifacts such as apologetic or verbose phrasing" and "apologetic language artifacts alone can skew evaluator preferences by up to 98%" (abstract).
  - "we investigate jury-based evaluations aggregating decisions from multiple models. Although this approach both improves robustness and enhances alignment to human judgements, artifact sensitivity persists even with the best jury configurations" (abstract).
- Implication for the loop: the wording of a PR body or a worker's reply (hedging, apology, verbosity) moves an LLM verdict; a jury of models reduces but does not remove this. The loop's defence is structural: the audit reads the head as data and the rules from `origin/main` (standing order 20), and replies to findings are machine-checked lines (`fixed:`, `refuted:`, `residual:`), not prose the judge weighs.

### 4. When AI Agrees Too Much: Manipulating Automated Code Review via Bias Injection

- Venue and year: arXiv 2603.18740 (2026, v2). Alexopoulos, Alexopoulos, Spinellis, Mitropoulos. Earlier title "Measuring and Exploiting Contextual Bias in LLM-Assisted Security Code Review".
- URL: <https://arxiv.org/abs/2603.18740>
- Quoted findings:
  - On patched (non-vulnerable) code under a neutral "is this vulnerable" prompt: "All models exhibit very high false positive rates (>88%) even under neutral conditions, with the sole exception of Claude 3.5 Haiku (68.4%)" (section 3.2.2). On vulnerable code: "Incorrect justifications range from 71.0% (Claude 3.5 Haiku) to 57.6% (Gemini 2.0 Flash), meaning the majority of detections on vulnerable files flag issues unrelated to the actual vulnerabilities" (section 3.2.1).
  - Against two real review pipelines (Claude Code and CodeRabbit) over 33 CVEs in 20 projects, "Our refinement attack ... is successful in 32/33 (97%) cases, exploiting a fundamental asymmetry: attackers can iteratively refine attacks against a local clone of the review pipeline, while defenders have only one chance to detect them" (abstract).
- Implication for the loop: an open-ended "find any security defect" audit of a change that is in fact safe will say "vulnerable" most of the time, and when it says so on a real defect it usually points at the wrong line. The loop's auditor must be asked a bounded question against the Contract, and the measured 88%+ false positive rate on safe code is the quantitative reason an `incorrect` verdict alone cannot be the stopping signal.

## 2. Do iterative review or repair loops converge

### 5. More Rounds, More Noise: Why Multi-Turn Review Fails to Improve Cross-Context Verification

- Venue and year: arXiv 2603.16244 (2026). Song Tae-Eun.
- URL: <https://arxiv.org/abs/2603.16244>
- Quoted findings:
  - "In a controlled experiment with 30 artifacts and 150 injected errors ... Single-pass CCR (F1 = 0.376) significantly outperformed all multi-turn variants ... Multi-turn review increased recall (+0.08) but generated 62% more false positives (8.5 vs. 5.2), collapsing precision from 0.30 to 0.20" (abstract).
  - "reviewers in later rounds fabricate findings when the artifact's real errors have been exhausted" and "Independent re-review without prior context (D-CCR-2c) performed worst (F1 = 0.263), confirming that mere repetition degrades rather than helps" (abstract).
- Implication for the loop: this is the "infinite nitpick" measured. A second fresh reviewer of the same artifact finds few new real errors and many fabricated ones, and the fresh-context variant is the worst of all. The store's per-head fresh audit is exactly D-CCR-2c when the head has not materially changed (a merge of main, a formatting commit), which is what the "per-head verdict rule" rows in the treadmill analysis already recorded as rounds that bought no finding.

### 6. From Static to Dynamic: Benchmarking Real-World Code Review with MCR-Bench

- Venue and year: Proceedings of the ACM on Software Engineering, ISSTA 2026 issue (arXiv 2608.27442, 2026). Zheng, Wang, Wang, Duan, Zhang, Liu, Ma, Zheng.
- URL: <https://dl.acm.org/doi/10.1145/3832219> and <https://arxiv.org/abs/2608.27442>
- Quoted findings:
  - "2,269 real-world multi-round code review tasks ... mainstream LLMs exhibit limited overall performance in defect detection and defect lifecycle state tracking, with performance degrading significantly as the number of interaction rounds increases" (abstract).
  - Table 10, average F1 by review round: Claude Haiku 4.5 goes 0.6495 at round 2, 0.5359 at round 4, 0.4768 at round 7, 0.2857 at round 10; GPT-5.2 goes 0.5995, 0.5659, 0.6238, 0.5000 at the same rounds; the paper names "cross-round temporal misalignment and inadequate long-range memory" as the drivers (abstract and section 6.2).
- Implication for the loop: a reviewer that carries the history of earlier rounds loses track of which defects are open, fixed or regressed, and its F1 roughly halves by round 10. The loop should not ask one context to hold the round history; the ledger holds it, each audit sees one head and one Contract, and the treadmill count is kept by the coordinator, not by the judge.

### 7. Is Three the Magic Number? An Empirical Evaluation of LLM-Based Repair Loops

- Venue and year: arXiv 2607.05197 (2026). Kiecker, Reichmann, Kang, An, Grunske.
- URL: <https://arxiv.org/abs/2607.05197>
- Quoted findings:
  - "we observe a consistent pattern of diminishing returns: the first three to four repair iterations account for most achievable gains, while later iterations contribute only marginal improvements" (abstract).
  - "repair behavior is influenced more strongly by workflow orchestration and feedback design than by the underlying model itself. These results suggest that repair budgets should be treated as an explicit experimental variable" (abstract).
- Implication for the loop: when the feedback is an executable oracle (compiler, tests), the budget that captures most of the gain is three to four rounds, and the orchestration matters more than the model. This is the measured basis for a fixed round cap written into the brief, and it agrees with the two-strike proposal: the third round should change the mechanism or the feedback, not repeat it.

### 8. Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair

- Venue and year: arXiv 2607.24604 (2026). Gao, Yang, Yang.
- URL: <https://arxiv.org/abs/2607.24604>
- Quoted findings:
  - "Under forced revision, current correctness with current traces falls from 0.820 after one revision to 0.673 after two, although ever-correct rises to 0.847" (abstract; 900 three-revision trajectories over 30 HumanEval repairs).
  - "stale traces harm 34/135 correct starts versus 4/135 with current traces, a 22.2-point increase (task-cluster 95% CI [8.9, 37.0], exact Holm p=0.0337)" and the authors "derive an evidence-bound typed loop contract ... that binds verifier evidence to exact code states, preserves verified checkpoints, and emits auditable admission receipts" (abstract).
- Implication for the loop: forcing another revision on a state that is already correct destroys correct work, and feeding the reviser evidence from an earlier state makes it worse by 22 points. The ledger's rule that a verdict is bound to the full 40-hex head and never carries over (standing order 18) is this paper's "state-bound evidence"; the missing half is "preserve verified checkpoints", meaning a `correct` head should not be re-opened by a later round's new finding without a new row that names why.

## 3. Agentic review with execution, precision versus recall

### 9. LLM Critics Help Catch LLM Bugs (CriticGPT)

- Venue and year: arXiv 2407.00215 (2024). McAleese, Pokorny, Ceron Uribe, Nitishinskaya, Trebacz, Leike (OpenAI).
- URL: <https://arxiv.org/abs/2407.00215>
- Quoted findings:
  - "On code containing naturally occurring LLM errors model-written critiques are preferred over human critiques in 63% of cases, and human evaluation finds that models catch more bugs than human contractors paid for code review" (abstract).
  - "the rate of nitpicks and hallucinated bugs is much higher for models than for humans ... models which hallucinate bugs more often are also more likely to catch human inserted and previously detected bugs. We see this as analogous to precision and recall" (section 3.4); "human-machine teams of critics and contractors catch similar numbers of bugs to LLM critics while hallucinating less than LLMs alone" (abstract).
- Implication for the loop: recall and nitpick rate rise together in an LLM critic; a critic tuned to miss nothing will also raise findings that are not defects, and only a human in the team brought the hallucination rate down without losing recall. The loop should therefore read a P2 or P3 from a fresh auditor as a recall-biased signal and route it to the residual mechanism (standing order 22) rather than to another fix round.

### 10. Agent-as-a-Judge: Evaluate Agents with Agents

- Venue and year: ICML 2025, PMLR volume 267 (arXiv 2410.10934, 2024). Zhuge, Zhao, Ashley, Wang, Khizbullin, Xiong, Liu, Chang, Krishnamoorthi, Tian, Shi, Chandra, Schmidhuber.
- URL: <https://proceedings.mlr.press/v267/zhuge25a.html> and <https://arxiv.org/abs/2410.10934>
- Quoted findings:
  - On DevAI, "55 realistic automated AI development tasks" with "365 hierarchical user requirements", Table 3 (columns MetaGPT, GPT-Pilot, OpenHands) gives the agent judge an alignment rate with the human majority of 88.52%, 83.88% and 90.44% in the black-box setting and 92.07%, 86.61% and 90.16% in the gray-box setting, against 84.15%, 65.30% and 60.38% (black-box) for LLM-as-a-Judge and 89.34%, 84.88% and 85.70% for the average individual human evaluator.
  - Component ablation on OpenHands: alignment 65.03% with only the `ask` component, 75.95% with the code graph, 82.24% with `read`, 90.44% with `locate`, 90.16% with `retrieve` (Table 4); "Agent-as-a-Judge saves 97.72% of the time and 97.64% of the cost compared to involving three human experts" (section 1).
- Implication for the loop: a judge that can read the repository, locate files and run things is as aligned with humans as a single human evaluator; a judge that only reads the prompt is 25 points worse. The judge is handed the requirements as an explicit list and grades each one, which is the Contract-section design the `pr-audit.sh` lever already requires. The same paper notes the task is class-imbalanced (most requirements fail), so alignment rate flatters a judge that says "fail" by default; precision-recall curves are the honest measure.

### 11. Introducing SWE-bench Verified, with the 2026 follow-up

- Venue and year: OpenAI research publication, August 2024 (updated February 2025); follow-up "Why SWE-bench Verified no longer measures frontier coding capabilities", February 2026. Chowdhury, Aung, Shern, Jaffe, Sherburn, Starace and others. Not a peer-reviewed paper; entered because it is the human-validation protocol the assignment names.
- URL: <https://openai.com/index/introducing-swe-bench-verified/> and <https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/>
- Quoted findings:
  - 2024: "We worked with 93 software developers experienced in Python ... each sample is labeled 3 times by separate annotators ... we conservatively ensemble annotations by taking the highest-severity label amongst the 3 annotators"; "38.3% of samples were flagged for underspecified problem statements, and 61.1% were flagged for unit tests that may unfairly mark valid solutions as incorrect. Overall, our annotation process resulted in 68.3% of SWE-bench samples being filtered out."
  - 2026: "We conducted an audit of 138 SWE-bench Verified problems that OpenAI o3 did not consistently solve over 64 independent runs. Each case was independently reviewed by at least six experienced software engineers ... 59.4% of the 138 problems contained material issues in test design and/or problem description"; of these "35.5% ... narrow test cases" and "18.8% ... wide test cases" that "check for additional functionality that wasn't specified in the problem description".
- Implication for the loop: even three human validators per task, taking the worst label, left more than half of the hard residue with a specification that did not match its oracle; the two named failure shapes, an oracle narrower than the spec and an oracle wider than the spec, are the two ways a Contract and a verdict can disagree. A unit whose audit keeps failing should be checked for a spec-oracle mismatch before another fix round, which is the brief-time closure check in a different vocabulary.

## 4. Specification-bounded versus open-ended review

### 12. LLM Judges Can Be Too Generous When There Is No Reference Answer

- Venue and year: arXiv 2607.12885 (2026). Kranti and Vajjala.
- URL: <https://arxiv.org/abs/2607.12885>
- Quoted findings:
  - "the judge models we evaluated tend to over-credit incorrect answers in the absence of a reference answer, and adding reference answer information to the prompt flips the judge model's correct/incorrect decisions by as much as 85% in some experimental settings" (abstract).
  - "Comparison with a subset of human annotations shows that these reference-driven changes generally align with human judgments" and the authors ask for "calibrating the LLM judges with a sample with reference-aware evaluation before using them in reference-free setups" (abstract).
- Implication for the loop: without a reference the judge is lenient, and the reference moves the verdict toward the human one. In this loop the reference is the Contract section plus the deterministic checks on the head; an audit of a PR without a Contract is the reference-free condition and `pr-audit.sh` is right to refuse it.

### 13. Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement

- Venue and year: arXiv 2603.00539 (2026). Jin and Chen.
- URL: <https://arxiv.org/abs/2603.00539>
- Quoted findings:
  - "we demonstrate that LLMs frequently misclassify correct code implementation as non-compliant or defective. Surprisingly, we find that more detailed prompt design, particularly with those requiring explanations and proposed corrections, leads to higher misjudgment rates" (abstract). Measured as the false-negative rate on correct code: "Under Direct, GPT-4o achieves a relatively low FNR in HumanEval (26.2%) and MBPP (35.9%), but once explanations and repairs are required, the FNR increases sharply to 73.2% in HumanEval and 87.9% in MBPP. Meanwhile, its FPR drops to nearly zero in several settings" (section on closed-source models).
  - The proposed remedy "treats the model proposed fix as executable counterfactual evidence, and validates the original and revised implementations using benchmark tests and spec-constrained augmented tests" (abstract).
- Implication for the loop: the opposite failure to entry 12. Given a specification to check against, the judge over-rejects correct code, and asking it to explain and propose a fix makes the over-rejection worse. A spec bounds the question but does not make the verdict reliable by itself; the paper's answer is to execute the judge's proposed fix as a test, which is the loop's "one deterministic fact per round" applied to the auditor's own claim: a P1 that cannot be turned into a failing test or a reproduced command is a candidate for `refuted:`.

## 5. Denylists over shell and the undecidability of shell text

### 14. One Goal, Many Commands: Characterizing Denylist Fragility in AI Agents

- Venue and year: arXiv 2606.15549 (2026, v2). Chen and Lin. v1 title "CmdNeedle: Measuring the Incompleteness of Command Denylists for AI Agents".
- URL: <https://arxiv.org/abs/2606.15549>
- Quoted findings:
  - "even a built-in denylist of Claude Code, well-maintained by its developers, can overlook bypass commands that invalidate its effectiveness" (abstract); the overlooked command is AWK: "the domain-specific language (DSL) used by AWK is Turing-complete, and more importantly, AWK can invoke Bash and pass arbitrary Bash scripts in the invocation. The fact that AWK is not in the denylist essentially bypasses the rule that covers Bash" (section 3.1).
  - "we applied ShellSieve to 1,709 real-world command denylists (containing 13,332 denylist rules) collected from GitHub ... 69.0-98.6% of the denylists are fragile" (abstract); "fixing fragile denylists will require adding numerous commands (averaging 217 if they aim to block specific operations)" (section 1); the two confirmed root causes are "authors of denylists ignore less-known commands" and "multi-purpose commands are deliberately unlisted from the denylists for their benign use" (section 1).
- Implication for the loop: this is the measured form of "a denylist over Bash never closes". The pipeline that found the bypasses is itself an LLM proposing commands and a sandbox validating them, which is the same shape as a fresh auditor finding one more channel per round (U109 rounds 21 to 23). Every treadmill row that ended by replacing a verb list with an exact-shape allowlist or an AST walk (U103 round 3, U109 round 10) is the paper's conclusion applied; the decision-tree in plan D1 (parser if one exists, else an enumerable allowlist, else remove the feature) is the only ordering the numbers support.

### 15. From Ahead-of- to Just-in-Time and Back Again: Static Analysis for Unix Shell Programs

- Venue and year: HotOS 2025 (Workshop on Hot Topics in Operating Systems), ACM. Lazarek, Jung, Lamprou, Li, Narsipur, Zhao, Greenberg, Kallas, Mamouras, Vasilakis.
- URL: <https://doi.org/10.1145/3713082.3730395> (open PDF: <https://sigops.org/s/conferences/hotos/2025/papers/hotos25-364.pdf>)
- Quoted findings:
  - "the shell is uniquely challenging when it comes to anything static. Its pervasive dynamicity—e.g., runtime evaluation, expansion, subshells—seems to make ahead-of-time checking intractable. Its tight integration with, and arbitrary effects on, the broader environment complicates reasoning about possible states and effects prior to program execution. And its opaque, polyglot commands—communicating with each other and the shell through raw bytes—occlude deep reasoning" (section 1).
  - On the state of practice: "The most widely used tool is ShellCheck, a syntactic linter based on a collection of hard-coded patterns ... this kind of syntax-matching approach is limited: it fails to recognize an obviously safe fix (Fig. 2) and it fails to identify the unambiguous incorrectness of an obviously unsafe fix (Fig. 3). (The two attempted fixes, placed next to each other, differ by only one character.) Surface-level syntactic linting, while useful, is inherently noisy and context-insensitive" (section 2). The authors' own proposal needs symbolic execution over the shell semantics, command specifications mined by probing, and "If ahead-of-time checking is insufficient to conclude safety, specification-aware runtime monitoring" (section 1).
- Implication for the loop: the systems community's own statement is that pattern matching over shell text cannot decide safety, that two scripts one character apart can be safe and catastrophic, and that even a semantics-driven analysis falls back to a runtime monitor when it cannot conclude. For this repository that means a text-level rule over a `run:` body or a Bash command is a lint, never a gate; the gates that held were the ones that moved to the parser's tree (shfmt JSON under the U105 contract) with an exact table, or to the sandbox.

## Read but not entered (one line each)

- Replacing Judges with Juries (Verga et al., arXiv 2404.18796, 2024): a panel of three smaller judges from different families "outperforms a single large judge, exhibits less intra-model bias ... while being over seven times less expensive"; the panel result for entry 3 in a non-safety setting. <https://arxiv.org/abs/2404.18796>
- Don't Judge Code by Its Cover (Moon et al., Findings of EACL 2026): six superficial variations of functionally equivalent code (names, comments, formatting) change the judge's score in all tested models, "even when prompted to generate test cases before scoring". <https://aclanthology.org/2026.findings-eacl.70/>
- LLM-based Vulnerability Detection at Project Scale (Li et al., arXiv 2601.19239, 2026): 6,442 sampled warnings, 5,896 false positives; "the lowest overall SFDR being 9.09% for C/C++ and 31.82% for Java" with "prompt-compliance failures" as an LLM-only false-positive cause. <https://arxiv.org/abs/2601.19239>
- Reducing False Positives in Static Bug Detection with LLMs: An Empirical Study in Industry (Du et al., arXiv 2601.18844, 2026): 433 Tencent alarms (328 false); an LLM asked the bounded question "is this specific alarm real" in a hybrid with static analysis "eliminate[s] 94-98% of false positives with high recall", the counterpart to entry 4's open-ended prompt. <https://arxiv.org/abs/2601.18844>
- No Free Labels (Krumdick et al., arXiv 2503.05061, 2025): 1,200 expert-graded responses; without a reference, judges agree with experts "only on questions the judges were able to correctly answer themselves", and expert references "largely mitigate" it. <https://arxiv.org/abs/2503.05061>
- How Many Tries Does It Take? (Arimbur, arXiv 2604.10508, 2026): seven models, five self-repair attempts, "Most gains concentrate in the first two rounds"; assertion (logic) errors repair at about 45% against much higher rates for syntax and name errors. <https://arxiv.org/abs/2604.10508>
- Large Language Models Cannot Self-Correct Reasoning Yet (Huang et al., ICLR 2024, arXiv 2310.01798): without external feedback GPT-3.5 on GSM8K goes 75.9 to 75.1 to 74.7 over two self-correction rounds (Table 3); the pre-2024 origin of plan R1. <https://arxiv.org/abs/2310.01798>

## How this was gathered

Searches on 2026-10-30 over arXiv, the ACL Anthology, PMLR, the ACM Digital Library abstracts and the two OpenAI publications, with the five questions as queries; every abstract was read from its arXiv or publisher page, and the numbered sections and tables quoted above were read from the arXiv HTML or the open PDF. The ACM DL page of entry 15 returned HTTP 403 on this host, so the SIGOPS open copy was read instead. Four sources the store already cites (entries 5, 6 and 8, and the Huang paper in the last list) were re-read and their figures checked against the text; the store's earlier paraphrase of entry 5 ("a second review round on the same artifact raised recall slightly and false positives by 62%") is confirmed. Left out by design: vendor blog posts on denylist bypasses that carry no measurement, and surveys that only restate the primary papers above.
