# Validation evidence (a05)

Status: local implementation checks recorded; final-base full validator, independent worker review, push, CI and automatic-review window pending. Commands use the temporary uv cache and existing PyYAML. Evidence belongs to this task in worker-g. Historical results are labelled separately; no baseline success is described as RED.

## Unchanged 325f520b corpus comparison

Inline Python harness using the new anthropic_a03_cases table and tracked-fixture check against the unchanged source. Source blob afbf5d445bf78e59dc1e35745bd24a2a8bc7032b was verified equal to 325f520b before implementation; git diff --exit-code -- scripts/validate-agent-assets.py exited 0. The harness classifies stderr as hard/note/none, compares expected status and payload redaction, prints each row without its payload, and exits 1 for any policy mismatch. Exit: 1 (expected policy RED).

~~~~text
baseline_head=325f520bfc8b4dbb25e0744d27878cdf7eab2fd2 rows=414
1 local:a64daf1:1 api expected=hard actual=hard payload_leak=False
2 local:a64daf1:1 oauth expected=hard actual=hard payload_leak=False
3 local:a64daf1:1 reference expected=hard actual=none payload_leak=False
4 local:a64daf1:4 json expected=hard actual=hard payload_leak=False
5 local:a64daf1:4 toml expected=hard actual=hard payload_leak=False
6 local:a64daf1:4 ancestor expected=hard actual=hard payload_leak=False
7 unsupported assembled expected=none actual=hard payload_leak=False
8 unsupported command expected=hard actual=hard payload_leak=False
9 unsupported indirect expected=none actual=hard payload_leak=False
10 unsupported variable expected=none actual=hard payload_leak=False
11 other single-quoted-backslash expected=hard actual=hard payload_leak=False
12 other following-command expected=none actual=none payload_leak=False
13 other following-operator expected=hard actual=none payload_leak=False
14 other single-name expected=hard actual=hard payload_leak=False
15 other double-name expected=hard actual=hard payload_leak=False
16 other escaped-name expected=hard actual=hard payload_leak=False
17 other locale-name expected=hard actual=hard payload_leak=False
18 other quoted-ordinary-literal expected=none actual=none payload_leak=False
19 other decoded-ordinary-name expected=none actual=none payload_leak=False
20 other ordinary-brace-name expected=none actual=none payload_leak=False
21 other auth-brace-name expected=hard actual=hard payload_leak=False
22 other conditional-substitution expected=none actual=none payload_leak=False
23 other env-command expected=none actual=none payload_leak=False
24 other function-subshell-case expected=none actual=none payload_leak=False
25 other continued-case expected=hard actual=hard payload_leak=False
26 unsupported env-variable expected=none actual=hard payload_leak=False
27 unsupported env-assembled expected=none actual=hard payload_leak=False
28 a03-worker-577ad0f3 env-vanishing-prefix expected=hard actual=hard payload_leak=False
29 a03-worker-577ad0f3 env-option-prefix expected=hard actual=hard payload_leak=False
30 other quoted-leading-blank expected=hard actual=hard payload_leak=False
31 other escaped-leading-blank expected=hard actual=hard payload_leak=False
32 other trailing-empty-quote expected=hard actual=hard payload_leak=False
33 other leading-empty-quote expected=hard actual=hard payload_leak=False
34 other leading-empty-double expected=hard actual=hard payload_leak=False
35 other unclosed-reference expected=hard actual=hard payload_leak=False
36 other continued-reference expected=hard actual=none payload_leak=False
37 local:a64daf1:4 encoded-equals expected=hard actual=hard payload_leak=False
38 local:a64daf1:4 encoded-colon expected=hard actual=hard payload_leak=False
39 local:a64daf1:4 encoded-ancestor expected=hard actual=hard payload_leak=False
40 other yaml-complex-oauth expected=hard actual=hard payload_leak=False
41 other yaml-complex-escaped expected=hard actual=hard payload_leak=False
42 other yaml-complex-assignment expected=hard actual=hard payload_leak=False
43 other oauth-fence-header expected=hard actual=hard payload_leak=False
44 local:a64daf1:2 Don't store credentials. expected=hard actual=hard payload_leak=False
45 local:a64daf1:2 Never store credentials. expected=hard actual=hard payload_leak=False
46 local:a64daf1:3 '\u2028' expected=hard actual=hard payload_leak=False
47 local:a64daf1:3 decoded-'\u2028' expected=hard actual=hard payload_leak=False
48 local:a64daf1:3 '\u2029' expected=hard actual=hard payload_leak=False
49 local:a64daf1:3 decoded-'\u2029' expected=hard actual=hard payload_leak=False
50 local:a64daf1:3 '\x0b' expected=hard actual=hard payload_leak=False
51 local:a64daf1:3 decoded-'\x0b' expected=hard actual=hard payload_leak=False
52 local:a64daf1:3 allowed-' ' expected=none actual=none payload_leak=False
53 local:a64daf1:3 allowed-'\t' expected=hard actual=none payload_leak=False
54 local:a64daf1:3 allowed-'\n' expected=none actual=none payload_leak=False
55 a04-worker-c15be6b9 env-unknown-expansion expected=none actual=hard payload_leak=False
56 a04-worker-c15be6b9 env-special-expansion expected=none actual=hard payload_leak=False
57 a04-worker-c15be6b9 env-dynamic-name expected=none actual=hard payload_leak=False
58 a04-worker-c15be6b9 env-dynamic-name-bound expected=hard actual=hard payload_leak=False
59 a04-worker-c15be6b9 env-unknown-option expected=none actual=hard payload_leak=False
60 a04-worker-c15be6b9 env-unknown-attached-option expected=none actual=hard payload_leak=False
61 a04-worker-c15be6b9 env-unknown-attached-option-bound expected=hard actual=hard payload_leak=False
62 a04-worker-c15be6b9 env-redirect-fd expected=none actual=hard payload_leak=False
63 a04-worker-c15be6b9 env-redirect-fd-bound expected=hard actual=hard payload_leak=False
64 a04-worker-c15be6b9 env-redirect-expansion expected=none actual=hard payload_leak=False
65 a04-worker-c15be6b9 env-redirect-expansion-bound expected=hard actual=hard payload_leak=False
66 a04-worker-c15be6b9 env-brace-fd expected=none actual=hard payload_leak=False
67 a04-worker-c15be6b9 env-brace-fd-bound expected=hard actual=hard payload_leak=False
68 a04-worker-c15be6b9 env-duplicate-fd expected=none actual=hard payload_leak=False
69 a04-worker-c15be6b9 env-duplicate-fd-bound expected=hard actual=hard payload_leak=False
70 a04-worker-c15be6b9 env-append-redirection expected=none actual=hard payload_leak=False
71 a04-worker-c15be6b9 env-append-redirection-bound expected=hard actual=hard payload_leak=False
72 a04-worker-c15be6b9 env-process-redirection expected=none actual=hard payload_leak=False
73 a04-worker-c15be6b9 env-process-redirection-bound expected=hard actual=hard payload_leak=False
74 a04-worker-c15be6b9 env-ordinary-client expected=none actual=none payload_leak=False
75 a04-worker-c15be6b9 env-ordinary-ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
76 a04-worker-c15be6b9 env-ordinary-$opts; NORMAL=$DEPLOYED_KEY expected=none actual=none payload_leak=False
77 a04-worker-c15be6b9 env-ordinary-'$opts' NORMAL=ordinary expected=none actual=none payload_leak=False
78 a04-worker-c15be6b9 exec-unknown-expansion expected=none actual=hard payload_leak=False
79 a04-worker-c15be6b9 exec-special-expansion expected=none actual=hard payload_leak=False
80 a04-worker-c15be6b9 exec-dynamic-name expected=none actual=hard payload_leak=False
81 a04-worker-c15be6b9 exec-dynamic-name-bound expected=hard actual=hard payload_leak=False
82 a04-worker-c15be6b9 exec-unknown-option expected=none actual=hard payload_leak=False
83 a04-worker-c15be6b9 exec-unknown-attached-option expected=none actual=hard payload_leak=False
84 a04-worker-c15be6b9 exec-unknown-attached-option-bound expected=hard actual=hard payload_leak=False
85 a04-worker-c15be6b9 exec-redirect-fd expected=none actual=hard payload_leak=False
86 a04-worker-c15be6b9 exec-redirect-fd-bound expected=hard actual=hard payload_leak=False
87 a04-worker-c15be6b9 exec-redirect-expansion expected=none actual=hard payload_leak=False
88 a04-worker-c15be6b9 exec-redirect-expansion-bound expected=hard actual=hard payload_leak=False
89 a04-worker-c15be6b9 exec-brace-fd expected=none actual=hard payload_leak=False
90 a04-worker-c15be6b9 exec-brace-fd-bound expected=hard actual=hard payload_leak=False
91 a04-worker-c15be6b9 exec-duplicate-fd expected=none actual=hard payload_leak=False
92 a04-worker-c15be6b9 exec-duplicate-fd-bound expected=hard actual=hard payload_leak=False
93 a04-worker-c15be6b9 exec-append-redirection expected=none actual=hard payload_leak=False
94 a04-worker-c15be6b9 exec-append-redirection-bound expected=hard actual=hard payload_leak=False
95 a04-worker-c15be6b9 exec-process-redirection expected=none actual=hard payload_leak=False
96 a04-worker-c15be6b9 exec-process-redirection-bound expected=hard actual=hard payload_leak=False
97 a04-worker-c15be6b9 exec-ordinary-client expected=none actual=none payload_leak=False
98 a04-worker-c15be6b9 exec-ordinary-ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
99 a04-worker-c15be6b9 exec-ordinary-$opts; NORMAL=$DEPLOYED_KEY expected=none actual=none payload_leak=False
100 a04-worker-c15be6b9 exec-ordinary-'$opts' NORMAL=ordinary expected=none actual=none payload_leak=False
101 a04-worker-c15be6b9 command-unknown-expansion expected=none actual=hard payload_leak=False
102 a04-worker-c15be6b9 command-special-expansion expected=none actual=hard payload_leak=False
103 a04-worker-c15be6b9 command-dynamic-name expected=none actual=hard payload_leak=False
104 a04-worker-c15be6b9 command-dynamic-name-bound expected=hard actual=hard payload_leak=False
105 a04-worker-c15be6b9 command-unknown-option expected=none actual=hard payload_leak=False
106 a04-worker-c15be6b9 command-unknown-attached-option expected=none actual=hard payload_leak=False
107 a04-worker-c15be6b9 command-unknown-attached-option-bound expected=hard actual=hard payload_leak=False
108 a04-worker-c15be6b9 command-redirect-fd expected=none actual=hard payload_leak=False
109 a04-worker-c15be6b9 command-redirect-fd-bound expected=hard actual=hard payload_leak=False
110 a04-worker-c15be6b9 command-redirect-expansion expected=none actual=hard payload_leak=False
111 a04-worker-c15be6b9 command-redirect-expansion-bound expected=hard actual=hard payload_leak=False
112 a04-worker-c15be6b9 command-brace-fd expected=none actual=hard payload_leak=False
113 a04-worker-c15be6b9 command-brace-fd-bound expected=hard actual=hard payload_leak=False
114 a04-worker-c15be6b9 command-duplicate-fd expected=none actual=hard payload_leak=False
115 a04-worker-c15be6b9 command-duplicate-fd-bound expected=hard actual=hard payload_leak=False
116 a04-worker-c15be6b9 command-append-redirection expected=none actual=hard payload_leak=False
117 a04-worker-c15be6b9 command-append-redirection-bound expected=hard actual=hard payload_leak=False
118 a04-worker-c15be6b9 command-process-redirection expected=none actual=hard payload_leak=False
119 a04-worker-c15be6b9 command-process-redirection-bound expected=hard actual=hard payload_leak=False
120 a04-worker-c15be6b9 command-ordinary-client expected=none actual=none payload_leak=False
121 a04-worker-c15be6b9 command-ordinary-ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
122 a04-worker-c15be6b9 command-ordinary-$opts; NORMAL=$DEPLOYED_KEY expected=none actual=none payload_leak=False
123 a04-worker-c15be6b9 command-ordinary-'$opts' NORMAL=ordinary expected=none actual=none payload_leak=False
124 a04-worker-c15be6b9 nohup-unknown-expansion expected=none actual=hard payload_leak=False
125 a04-worker-c15be6b9 nohup-special-expansion expected=none actual=hard payload_leak=False
126 a04-worker-c15be6b9 nohup-dynamic-name expected=none actual=hard payload_leak=False
127 a04-worker-c15be6b9 nohup-dynamic-name-bound expected=hard actual=hard payload_leak=False
128 a04-worker-c15be6b9 nohup-unknown-option expected=none actual=hard payload_leak=False
129 a04-worker-c15be6b9 nohup-unknown-attached-option expected=none actual=hard payload_leak=False
130 a04-worker-c15be6b9 nohup-unknown-attached-option-bound expected=hard actual=hard payload_leak=False
131 a04-worker-c15be6b9 nohup-redirect-fd expected=none actual=hard payload_leak=False
132 a04-worker-c15be6b9 nohup-redirect-fd-bound expected=hard actual=hard payload_leak=False
133 a04-worker-c15be6b9 nohup-redirect-expansion expected=none actual=hard payload_leak=False
134 a04-worker-c15be6b9 nohup-redirect-expansion-bound expected=hard actual=hard payload_leak=False
135 a04-worker-c15be6b9 nohup-brace-fd expected=none actual=hard payload_leak=False
136 a04-worker-c15be6b9 nohup-brace-fd-bound expected=hard actual=hard payload_leak=False
137 a04-worker-c15be6b9 nohup-duplicate-fd expected=none actual=hard payload_leak=False
138 a04-worker-c15be6b9 nohup-duplicate-fd-bound expected=hard actual=hard payload_leak=False
139 a04-worker-c15be6b9 nohup-append-redirection expected=none actual=hard payload_leak=False
140 a04-worker-c15be6b9 nohup-append-redirection-bound expected=hard actual=hard payload_leak=False
141 a04-worker-c15be6b9 nohup-process-redirection expected=none actual=hard payload_leak=False
142 a04-worker-c15be6b9 nohup-process-redirection-bound expected=hard actual=hard payload_leak=False
143 a04-worker-c15be6b9 nohup-ordinary-client expected=none actual=none payload_leak=False
144 a04-worker-c15be6b9 nohup-ordinary-ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
145 a04-worker-c15be6b9 nohup-ordinary-$opts; NORMAL=$DEPLOYED_KEY expected=none actual=none payload_leak=False
146 a04-worker-c15be6b9 nohup-ordinary-'$opts' NORMAL=ordinary expected=none actual=none payload_leak=False
147 a04-worker-c15be6b9 sudo-unknown-expansion expected=none actual=hard payload_leak=False
148 a04-worker-c15be6b9 sudo-special-expansion expected=none actual=hard payload_leak=False
149 a04-worker-c15be6b9 sudo-dynamic-name expected=none actual=hard payload_leak=False
150 a04-worker-c15be6b9 sudo-dynamic-name-bound expected=hard actual=hard payload_leak=False
151 a04-worker-c15be6b9 sudo-unknown-option expected=none actual=hard payload_leak=False
152 a04-worker-c15be6b9 sudo-unknown-attached-option expected=none actual=hard payload_leak=False
153 a04-worker-c15be6b9 sudo-unknown-attached-option-bound expected=hard actual=hard payload_leak=False
154 a04-worker-c15be6b9 sudo-redirect-fd expected=none actual=hard payload_leak=False
155 a04-worker-c15be6b9 sudo-redirect-fd-bound expected=hard actual=hard payload_leak=False
156 a04-worker-c15be6b9 sudo-redirect-expansion expected=none actual=hard payload_leak=False
157 a04-worker-c15be6b9 sudo-redirect-expansion-bound expected=hard actual=hard payload_leak=False
158 a04-worker-c15be6b9 sudo-brace-fd expected=none actual=hard payload_leak=False
159 a04-worker-c15be6b9 sudo-brace-fd-bound expected=hard actual=hard payload_leak=False
160 a04-worker-c15be6b9 sudo-duplicate-fd expected=none actual=hard payload_leak=False
161 a04-worker-c15be6b9 sudo-duplicate-fd-bound expected=hard actual=hard payload_leak=False
162 a04-worker-c15be6b9 sudo-append-redirection expected=none actual=hard payload_leak=False
163 a04-worker-c15be6b9 sudo-append-redirection-bound expected=hard actual=hard payload_leak=False
164 a04-worker-c15be6b9 sudo-process-redirection expected=none actual=hard payload_leak=False
165 a04-worker-c15be6b9 sudo-process-redirection-bound expected=hard actual=hard payload_leak=False
166 a04-worker-c15be6b9 sudo-ordinary-client expected=none actual=none payload_leak=False
167 a04-worker-c15be6b9 sudo-ordinary-ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
168 a04-worker-c15be6b9 sudo-ordinary-$opts; NORMAL=$DEPLOYED_KEY expected=none actual=none payload_leak=False
169 a04-worker-c15be6b9 sudo-ordinary-'$opts' NORMAL=ordinary expected=none actual=none payload_leak=False
170 a04-worker-c15be6b9 xargs-unknown-expansion expected=none actual=hard payload_leak=False
171 a04-worker-c15be6b9 xargs-special-expansion expected=none actual=hard payload_leak=False
172 a04-worker-c15be6b9 xargs-dynamic-name expected=none actual=hard payload_leak=False
173 a04-worker-c15be6b9 xargs-dynamic-name-bound expected=hard actual=hard payload_leak=False
174 a04-worker-c15be6b9 xargs-unknown-option expected=none actual=hard payload_leak=False
175 a04-worker-c15be6b9 xargs-unknown-attached-option expected=none actual=hard payload_leak=False
176 a04-worker-c15be6b9 xargs-unknown-attached-option-bound expected=hard actual=hard payload_leak=False
177 a04-worker-c15be6b9 xargs-redirect-fd expected=none actual=hard payload_leak=False
178 a04-worker-c15be6b9 xargs-redirect-fd-bound expected=hard actual=hard payload_leak=False
179 a04-worker-c15be6b9 xargs-redirect-expansion expected=none actual=hard payload_leak=False
180 a04-worker-c15be6b9 xargs-redirect-expansion-bound expected=hard actual=hard payload_leak=False
181 a04-worker-c15be6b9 xargs-brace-fd expected=none actual=hard payload_leak=False
182 a04-worker-c15be6b9 xargs-brace-fd-bound expected=hard actual=hard payload_leak=False
183 a04-worker-c15be6b9 xargs-duplicate-fd expected=none actual=hard payload_leak=False
184 a04-worker-c15be6b9 xargs-duplicate-fd-bound expected=hard actual=hard payload_leak=False
185 a04-worker-c15be6b9 xargs-append-redirection expected=none actual=hard payload_leak=False
186 a04-worker-c15be6b9 xargs-append-redirection-bound expected=hard actual=hard payload_leak=False
187 a04-worker-c15be6b9 xargs-process-redirection expected=none actual=hard payload_leak=False
188 a04-worker-c15be6b9 xargs-process-redirection-bound expected=hard actual=hard payload_leak=False
189 a04-worker-c15be6b9 xargs-ordinary-client expected=none actual=none payload_leak=False
190 a04-worker-c15be6b9 xargs-ordinary-ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
191 a04-worker-c15be6b9 xargs-ordinary-$opts; NORMAL=$DEPLOYED_KEY expected=none actual=none payload_leak=False
192 a04-worker-c15be6b9 xargs-ordinary-'$opts' NORMAL=ordinary expected=none actual=none payload_leak=False
193 a04-worker-c15be6b9 time-unknown-expansion expected=none actual=hard payload_leak=False
194 a04-worker-c15be6b9 time-special-expansion expected=none actual=hard payload_leak=False
195 a04-worker-c15be6b9 time-dynamic-name expected=none actual=hard payload_leak=False
196 a04-worker-c15be6b9 time-dynamic-name-bound expected=hard actual=hard payload_leak=False
197 a04-worker-c15be6b9 time-unknown-option expected=none actual=hard payload_leak=False
198 a04-worker-c15be6b9 time-unknown-attached-option expected=none actual=hard payload_leak=False
199 a04-worker-c15be6b9 time-unknown-attached-option-bound expected=hard actual=hard payload_leak=False
200 a04-worker-c15be6b9 time-redirect-fd expected=none actual=hard payload_leak=False
201 a04-worker-c15be6b9 time-redirect-fd-bound expected=hard actual=hard payload_leak=False
202 a04-worker-c15be6b9 time-redirect-expansion expected=none actual=hard payload_leak=False
203 a04-worker-c15be6b9 time-redirect-expansion-bound expected=hard actual=hard payload_leak=False
204 a04-worker-c15be6b9 time-brace-fd expected=none actual=hard payload_leak=False
205 a04-worker-c15be6b9 time-brace-fd-bound expected=hard actual=hard payload_leak=False
206 a04-worker-c15be6b9 time-duplicate-fd expected=none actual=hard payload_leak=False
207 a04-worker-c15be6b9 time-duplicate-fd-bound expected=hard actual=hard payload_leak=False
208 a04-worker-c15be6b9 time-append-redirection expected=none actual=hard payload_leak=False
209 a04-worker-c15be6b9 time-append-redirection-bound expected=hard actual=hard payload_leak=False
210 a04-worker-c15be6b9 time-process-redirection expected=none actual=hard payload_leak=False
211 a04-worker-c15be6b9 time-process-redirection-bound expected=hard actual=hard payload_leak=False
212 a04-worker-c15be6b9 time-ordinary-client expected=none actual=none payload_leak=False
213 a04-worker-c15be6b9 time-ordinary-ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
214 a04-worker-c15be6b9 time-ordinary-$opts; NORMAL=$DEPLOYED_KEY expected=none actual=none payload_leak=False
215 a04-worker-c15be6b9 time-ordinary-'$opts' NORMAL=ordinary expected=none actual=none payload_leak=False
216 a04-worker-c15be6b9 known-env -i ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
217 a04-worker-c15be6b9 known-env -- ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
218 a04-worker-c15be6b9 known-sudo -n env ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
219 a04-worker-c15be6b9 known-sudo --preserve-env=http_proxy,https_proxy env ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
220 a04-worker-c15be6b9 known-time -p env ANTHROPIC_API_KEY=$DEPLOYED_KEY client expected=hard actual=none payload_leak=False
221 a04-worker-c15be6b9 known-command -v "$NAME" expected=none actual=none payload_leak=False
222 a04-worker-c15be6b9 known-command_args=(exec -C "$repo") expected=none actual=none payload_leak=False
223 a04-worker-c15be6b9 known-exec 3>"$prefix-$run.md" expected=none actual=none payload_leak=False
224 a04-worker-c15be6b9 qualified-env expected=none actual=hard payload_leak=False
225 a04-worker-c15be6b9 unresolved-path expected=none actual=hard payload_leak=False
226 a04-worker-c15be6b9 assignment-env expected=hard actual=hard payload_leak=False
227 a04-worker-c15be6b9 assignment-exec expected=hard actual=hard payload_leak=False
228 a04-worker-c15be6b9 assignment-command expected=hard actual=hard payload_leak=False
229 a04-worker-c15be6b9 assignment-nohup expected=hard actual=hard payload_leak=False
230 a04-worker-c15be6b9 assignment-sudo expected=hard actual=hard payload_leak=False
231 a04-worker-c15be6b9 assignment-xargs expected=hard actual=hard payload_leak=False
232 a04-worker-c15be6b9 assignment-time expected=hard actual=hard payload_leak=False
233 a04-worker-c15be6b9 review-env "$NAME"=/usr/bin/env client expected=none actual=hard payload_leak=False
234 a04-worker-c15be6b9 review-env "$EMPTY" NORMAL=/usr/bin/env client expected=none actual=hard payload_leak=False
235 a04-worker-c15be6b9 review-NAME=ANTHROPIC_API_KEY; TOOL=env; "$TOOL" "$NAME"=literal-value client expected=hard actual=hard payload_leak=False
236 a04-worker-c15be6b9 review-"$TOOL" NORMAL=literal-value client expected=none actual=hard payload_leak=False
237 a04-worker-c15be6b9 review-"$1" "$NAME"=literal-value client expected=none actual=hard payload_leak=False
238 a04-worker-c15be6b9 review-"$(printf env)" "$NAME"=literal-value client expected=none actual=hard payload_leak=False
239 a04-worker-c15be6b9 operand-env expected=hard actual=hard payload_leak=False
240 a04-worker-c15be6b9 ordinary-operand-env expected=none actual=none payload_leak=False
241 a04-worker-c15be6b9 operand-export expected=hard actual=hard payload_leak=False
242 a04-worker-c15be6b9 ordinary-operand-export expected=none actual=none payload_leak=False
243 a04-worker-c15be6b9 review-ordinary-NORMAL=$((1<(case + 1))) expected=none actual=none payload_leak=False
244 a04-worker-c15be6b9 review-ordinary-"$TOOL" client expected=none actual=none payload_leak=False
245 spelling retained-001 expected=hard actual=hard payload_leak=False
246 spelling retained-002 expected=hard actual=hard payload_leak=False
247 spelling retained-003 expected=hard actual=hard payload_leak=False
248 spelling retained-004 expected=hard actual=hard payload_leak=False
249 spelling retained-005 expected=hard actual=hard payload_leak=False
250 spelling retained-006 expected=none actual=hard payload_leak=False
251 spelling retained-007 expected=none actual=hard payload_leak=False
252 spelling retained-008 expected=none actual=hard payload_leak=False
253 spelling retained-009 expected=none actual=hard payload_leak=False
254 spelling retained-010 expected=none actual=hard payload_leak=False
255 spelling retained-011 expected=none actual=hard payload_leak=False
256 spelling retained-012 expected=none actual=hard payload_leak=False
257 spelling retained-013 expected=none actual=hard payload_leak=False
258 spelling retained-014 expected=hard actual=none payload_leak=False
259 spelling retained-015 expected=hard actual=none payload_leak=False
260 spelling retained-016 expected=hard actual=hard payload_leak=False
261 spelling retained-017 expected=hard actual=hard payload_leak=False
262 spelling retained-018 expected=none actual=hard payload_leak=False
263 spelling retained-019 expected=hard actual=hard payload_leak=False
264 spelling retained-020 expected=hard actual=hard payload_leak=False
265 spelling retained-021 expected=hard actual=hard payload_leak=False
266 spelling retained-022 expected=hard actual=hard payload_leak=False
267 spelling retained-023 expected=none actual=hard payload_leak=False
268 spelling retained-024 expected=none actual=hard payload_leak=False
269 spelling retained-025 expected=none actual=hard payload_leak=False
270 spelling retained-026 expected=none actual=hard payload_leak=False
271 spelling retained-027 expected=none actual=hard payload_leak=False
272 spelling retained-028 expected=none actual=hard payload_leak=False
273 spelling retained-029 expected=none actual=hard payload_leak=False
274 spelling retained-030 expected=none actual=hard payload_leak=False
275 spelling retained-031 expected=none actual=hard payload_leak=False
276 spelling retained-032 expected=none actual=hard payload_leak=False
277 spelling retained-033 expected=none actual=hard payload_leak=False
278 spelling retained-034 expected=none actual=hard payload_leak=False
279 spelling retained-035 expected=none actual=hard payload_leak=False
280 spelling retained-036 expected=none actual=hard payload_leak=False
281 spelling retained-037 expected=none actual=hard payload_leak=False
282 spelling retained-038 expected=none actual=hard payload_leak=False
283 spelling retained-039 expected=none actual=hard payload_leak=False
284 spelling retained-040 expected=none actual=hard payload_leak=False
285 spelling retained-041 expected=none actual=hard payload_leak=False
286 spelling retained-042 expected=none actual=hard payload_leak=False
287 spelling retained-043 expected=none actual=hard payload_leak=False
288 spelling retained-044 expected=none actual=hard payload_leak=False
289 spelling retained-045 expected=none actual=hard payload_leak=False
290 spelling retained-046 expected=none actual=hard payload_leak=False
291 spelling retained-047 expected=none actual=hard payload_leak=False
292 spelling retained-048 expected=none actual=hard payload_leak=False
293 spelling retained-049 expected=none actual=hard payload_leak=False
294 spelling retained-050 expected=none actual=hard payload_leak=False
295 spelling retained-051 expected=none actual=hard payload_leak=False
296 spelling retained-052 expected=none actual=hard payload_leak=False
297 spelling retained-053 expected=hard actual=none payload_leak=False
298 spelling retained-054 expected=none actual=none payload_leak=False
299 spelling retained-055 expected=none actual=none payload_leak=False
300 spelling retained-056 expected=none actual=none payload_leak=False
301 spelling retained-057 expected=none actual=none payload_leak=False
302 spelling retained-058 expected=none actual=none payload_leak=False
303 spelling retained-059 expected=none actual=none payload_leak=False
304 spelling retained-060 expected=none actual=none payload_leak=False
305 spelling retained-061 expected=none actual=none payload_leak=False
306 spelling retained-062 expected=none actual=none payload_leak=False
307 spelling retained-063 expected=none actual=none payload_leak=False
308 spelling retained-064 expected=none actual=none payload_leak=False
309 spelling retained-065 expected=none actual=none payload_leak=False
310 spelling retained-066 expected=none actual=none payload_leak=False
311 spelling retained-067 expected=none actual=none payload_leak=False
312 spelling retained-068 expected=none actual=none payload_leak=False
313 spelling retained-069 expected=none actual=none payload_leak=False
314 spelling retained-070 expected=none actual=none payload_leak=False
315 spelling retained-071 expected=none actual=none payload_leak=False
316 spelling retained-072 expected=none actual=none payload_leak=False
317 spelling retained-073 expected=none actual=none payload_leak=False
318 spelling retained-074 expected=none actual=none payload_leak=False
319 spelling retained-075 expected=none actual=none payload_leak=False
320 spelling retained-076 expected=none actual=none payload_leak=False
321 spelling retained-077 expected=none actual=none payload_leak=False
322 spelling retained-078 expected=none actual=none payload_leak=False
323 spelling retained-079 expected=none actual=none payload_leak=False
324 spelling retained-080 expected=none actual=none payload_leak=False
325 spelling retained-081 expected=none actual=none payload_leak=False
326 spelling retained-082 expected=none actual=none payload_leak=False
327 spelling retained-083 expected=none actual=none payload_leak=False
328 spelling retained-084 expected=hard actual=hard payload_leak=False
329 spelling retained-085 expected=hard actual=hard payload_leak=False
330 spelling retained-086 expected=none actual=hard payload_leak=False
331 local:b139995:1 retained-087 expected=hard actual=hard payload_leak=False
332 local:b139995:1 retained-088 expected=hard actual=hard payload_leak=False
333 local:b139995:1 retained-089 expected=hard actual=hard payload_leak=False
334 local:b139995:1 retained-090 expected=none actual=none payload_leak=False
335 local:b139995:1 retained-091 expected=none actual=none payload_leak=False
336 local:b139995:1 retained-092 expected=none actual=none payload_leak=False
337 honest ANTHROPIC_API_KEY$DEPLOYED_KEY expected=none actual=none payload_leak=False
338 honest ANTHROPIC_API_KEY$DEPLOYED_KEY client expected=none actual=none payload_leak=False
339 honest ANTHROPIC_API_KEY$DEPLOYED_KEY client --flag expected=none actual=none payload_leak=False
340 honest ANTHROPIC_API_KEY$DEPLOYED_KEYexport  expected=none actual=none payload_leak=False
341 honest ANTHROPIC_API_KEY$DEPLOYED_KEYexport  client expected=none actual=none payload_leak=False
342 honest ANTHROPIC_API_KEY$DEPLOYED_KEYexport  client --flag expected=none actual=none payload_leak=False
343 honest ANTHROPIC_API_KEY"$DEPLOYED_KEY" expected=none actual=none payload_leak=False
344 honest ANTHROPIC_API_KEY"$DEPLOYED_KEY" client expected=none actual=none payload_leak=False
345 honest ANTHROPIC_API_KEY"$DEPLOYED_KEY" client --flag expected=none actual=none payload_leak=False
346 honest ANTHROPIC_API_KEY"$DEPLOYED_KEY"export  expected=none actual=none payload_leak=False
347 honest ANTHROPIC_API_KEY"$DEPLOYED_KEY"export  client expected=none actual=none payload_leak=False
348 honest ANTHROPIC_API_KEY"$DEPLOYED_KEY"export  client --flag expected=none actual=none payload_leak=False
349 honest ANTHROPIC_API_KEY${DEPLOYED_KEY} expected=none actual=none payload_leak=False
350 honest ANTHROPIC_API_KEY${DEPLOYED_KEY} client expected=none actual=none payload_leak=False
351 honest ANTHROPIC_API_KEY${DEPLOYED_KEY} client --flag expected=none actual=none payload_leak=False
352 honest ANTHROPIC_API_KEY${DEPLOYED_KEY}export  expected=none actual=none payload_leak=False
353 honest ANTHROPIC_API_KEY${DEPLOYED_KEY}export  client expected=none actual=none payload_leak=False
354 honest ANTHROPIC_API_KEY${DEPLOYED_KEY}export  client --flag expected=none actual=none payload_leak=False
355 honest ANTHROPIC_API_KEY"${DEPLOYED_KEY}" expected=none actual=none payload_leak=False
356 honest ANTHROPIC_API_KEY"${DEPLOYED_KEY}" client expected=none actual=none payload_leak=False
357 honest ANTHROPIC_API_KEY"${DEPLOYED_KEY}" client --flag expected=none actual=none payload_leak=False
358 honest ANTHROPIC_API_KEY"${DEPLOYED_KEY}"export  expected=none actual=none payload_leak=False
359 honest ANTHROPIC_API_KEY"${DEPLOYED_KEY}"export  client expected=none actual=none payload_leak=False
360 honest ANTHROPIC_API_KEY"${DEPLOYED_KEY}"export  client --flag expected=none actual=none payload_leak=False
361 self-reference ANTHROPIC_API_KEY$ANTHROPIC_API_KEY expected=hard actual=none payload_leak=False
362 self-reference ANTHROPIC_API_KEY$ANTHROPIC_OAUTH_TOKEN expected=hard actual=hard payload_leak=False
363 self-reference ANTHROPIC_API_KEY${ANTHROPIC_API_KEY} expected=hard actual=none payload_leak=False
364 self-reference ANTHROPIC_API_KEY${ANTHROPIC_OAUTH_TOKEN} expected=hard actual=hard payload_leak=False
365 honest ANTHROPIC_OAUTH_TOKEN$DEPLOYED_KEY expected=none actual=hard payload_leak=False
366 honest ANTHROPIC_OAUTH_TOKEN$DEPLOYED_KEY client expected=none actual=hard payload_leak=False
367 honest ANTHROPIC_OAUTH_TOKEN$DEPLOYED_KEY client --flag expected=none actual=hard payload_leak=False
368 honest ANTHROPIC_OAUTH_TOKEN$DEPLOYED_KEYexport  expected=none actual=hard payload_leak=False
369 honest ANTHROPIC_OAUTH_TOKEN$DEPLOYED_KEYexport  client expected=none actual=hard payload_leak=False
370 honest ANTHROPIC_OAUTH_TOKEN$DEPLOYED_KEYexport  client --flag expected=none actual=hard payload_leak=False
371 honest ANTHROPIC_OAUTH_TOKEN"$DEPLOYED_KEY" expected=none actual=hard payload_leak=False
372 honest ANTHROPIC_OAUTH_TOKEN"$DEPLOYED_KEY" client expected=none actual=hard payload_leak=False
373 honest ANTHROPIC_OAUTH_TOKEN"$DEPLOYED_KEY" client --flag expected=none actual=hard payload_leak=False
374 honest ANTHROPIC_OAUTH_TOKEN"$DEPLOYED_KEY"export  expected=none actual=hard payload_leak=False
375 honest ANTHROPIC_OAUTH_TOKEN"$DEPLOYED_KEY"export  client expected=none actual=hard payload_leak=False
376 honest ANTHROPIC_OAUTH_TOKEN"$DEPLOYED_KEY"export  client --flag expected=none actual=hard payload_leak=False
377 honest ANTHROPIC_OAUTH_TOKEN${DEPLOYED_KEY} expected=none actual=hard payload_leak=False
378 honest ANTHROPIC_OAUTH_TOKEN${DEPLOYED_KEY} client expected=none actual=hard payload_leak=False
379 honest ANTHROPIC_OAUTH_TOKEN${DEPLOYED_KEY} client --flag expected=none actual=hard payload_leak=False
380 honest ANTHROPIC_OAUTH_TOKEN${DEPLOYED_KEY}export  expected=none actual=hard payload_leak=False
381 honest ANTHROPIC_OAUTH_TOKEN${DEPLOYED_KEY}export  client expected=none actual=hard payload_leak=False
382 honest ANTHROPIC_OAUTH_TOKEN${DEPLOYED_KEY}export  client --flag expected=none actual=hard payload_leak=False
383 honest ANTHROPIC_OAUTH_TOKEN"${DEPLOYED_KEY}" expected=none actual=hard payload_leak=False
384 honest ANTHROPIC_OAUTH_TOKEN"${DEPLOYED_KEY}" client expected=none actual=hard payload_leak=False
385 honest ANTHROPIC_OAUTH_TOKEN"${DEPLOYED_KEY}" client --flag expected=none actual=hard payload_leak=False
386 honest ANTHROPIC_OAUTH_TOKEN"${DEPLOYED_KEY}"export  expected=none actual=hard payload_leak=False
387 honest ANTHROPIC_OAUTH_TOKEN"${DEPLOYED_KEY}"export  client expected=none actual=hard payload_leak=False
388 honest ANTHROPIC_OAUTH_TOKEN"${DEPLOYED_KEY}"export  client --flag expected=none actual=hard payload_leak=False
389 self-reference ANTHROPIC_OAUTH_TOKEN$ANTHROPIC_API_KEY expected=hard actual=hard payload_leak=False
390 self-reference ANTHROPIC_OAUTH_TOKEN$ANTHROPIC_OAUTH_TOKEN expected=hard actual=hard payload_leak=False
391 self-reference ANTHROPIC_OAUTH_TOKEN${ANTHROPIC_API_KEY} expected=hard actual=hard payload_leak=False
392 self-reference ANTHROPIC_OAUTH_TOKEN${ANTHROPIC_OAUTH_TOKEN} expected=hard actual=hard payload_leak=False
393 local:325f520:1 empty-subscript expected=hard actual=none payload_leak=False
394 local:325f520:1 subscript-zero expected=hard actual=none payload_leak=False
395 local:325f520:2 builtin-dash-dash expected=hard actual=none payload_leak=False
396 security:325f520:1 nullglob expected=hard actual=none payload_leak=False
397 security:325f520:2 builtin-newline expected=hard actual=none payload_leak=False
398 a03-prefix recorded-unresolved-prefix expected=hard actual=hard payload_leak=False
399 local:325f520:3 toml-comment expected=note actual=none payload_leak=False
400 local:325f520:3 yaml-comment expected=note actual=none payload_leak=False
401 local:325f520:4 honest-heredoc expected=none actual=hard payload_leak=False
402 local:325f520:5 markdown-line-four expected=hard actual=hard payload_leak=False
403 spelling percent expected=hard actual=none payload_leak=False
404 spelling unicode expected=hard actual=none payload_leak=False
405 spelling pieces expected=hard actual=hard payload_leak=False
406 spelling braced-name expected=hard actual=hard payload_leak=False
407 spelling layered expected=hard actual=none payload_leak=False
408 whole-line second-assignment expected=hard actual=hard payload_leak=False
409 whole-line cr expected=hard actual=hard payload_leak=False
410 note comment expected=note actual=none payload_leak=False
411 note prose expected=note actual=none payload_leak=False
412 code bare expected=hard actual=none payload_leak=False
413 code fence expected=hard actual=none payload_leak=False
414 code indented expected=hard actual=none payload_leak=False
verdict_counts={('hard', 'hard'): 130, ('hard', 'none'): 32, ('none', 'hard'): 154, ('none', 'none'): 94, ('note', 'none'): 4}
policy_or_redaction_mismatches=190

~~~~

## Unseen-shape unchanged baseline

Command: UV_CACHE_DIR=/private/tmp/uv-cache-a012 GIT_CONFIG_GLOBAL=/dev/null uv run --no-project --with pyyaml python -m unittest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule -v. Source: unchanged 325f520b. Exit: 0; baseline already rejects this shape.

~~~~text
test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.082s

OK

~~~~

## Local implementation module suite before independent review

Command: UV_CACHE_DIR=/private/tmp/uv-cache-a012 GIT_CONFIG_GLOBAL=/dev/null uv run --no-project --with pyyaml python -m unittest tests/unit/test_validate_agent_assets.py -v. Exit: 0. PyYAML available; no skipped cases. This is a pre-rebase worktree result; final-base output will follow.

~~~~text
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) ... ok
test_anthropic_auth_route_normalizes_shell_names_and_refuses_unreadable_names (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_normalizes_shell_names_and_refuses_unreadable_names) ... ok
test_anthropic_auth_route_parses_both_platform_renderings_of_chezmoi_templates (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_parses_both_platform_renderings_of_chezmoi_templates) ... ok
test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty) ... ok
test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment) ... ok
test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty) ... ok
test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter) ... ok
test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_json_and_toml_through_their_parsers) ... ok
test_anthropic_auth_route_reads_yaml_through_its_parser (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_yaml_through_its_parser) ... ok
test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text) ... ok
test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) ... ok
test_anthropic_check_accepts_an_environment_reference_followed_by_a_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_accepts_an_environment_reference_followed_by_a_command) ... ok
test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) ... ok
test_anthropic_check_decodes_ansi_c_escaped_names (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_decodes_ansi_c_escaped_names) ... ok
test_anthropic_check_keeps_single_quote_semantics_for_backslashes (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_keeps_single_quote_semantics_for_backslashes) ... ok
test_anthropic_check_parses_each_fenced_example_with_a_fresh_quote_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_parses_each_fenced_example_with_a_fresh_quote_state) ... ok
test_anthropic_check_redacts_assignment_payloads_in_diagnostics (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_redacts_assignment_payloads_in_diagnostics) ... ok
test_anthropic_check_refuses_an_env_option_it_cannot_classify_before_an_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_env_option_it_cannot_classify_before_an_assignment) ... ok
test_anthropic_check_refuses_an_unresolved_env_prefix_before_a_dynamic_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_unresolved_env_prefix_before_a_dynamic_assignment) ... ok
test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule) ... ok
test_anthropic_check_refuses_parse_failures_and_missing_yaml_without_disclosing_payloads (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_parse_failures_and_missing_yaml_without_disclosing_payloads) ... ok
test_anthropic_check_rejects_undecodable_name_forms (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_rejects_undecodable_name_forms) ... ok
test_anthropic_check_splits_shell_text_on_lf_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_splits_shell_text_on_lf_only) ... ok
test_anthropic_check_uses_the_unchanged_whole_line_for_allowance (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_uses_the_unchanged_whole_line_for_allowance) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/validate-agent-assets-test-7mn3hpnj/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok

----------------------------------------------------------------------
Ran 122 tests in 18.350s

OK

~~~~

## Real applied-tree auth and fixed regex before independent review

Inline Python loads scripts/validate-agent-assets.py with importlib, extracts the fixed regex from task.md and asserts equality with AUTH_ALLOWED.pattern, then calls validate_anthropic_auth_route() on the repository's own tracked home/install tree. UV_CACHE_DIR=/private/tmp/uv-cache-a012 uv run --no-project --with pyyaml python. Exit: 0. No applied-file edits or waivers.

~~~~text
fixed_allowlist_regex_byte_identical=True
real_applied_tree_auth_check=pass

~~~~

## Ruff unchanged baseline at original filenames

Command: UV_CACHE_DIR=/private/tmp/uv-cache-a012 uv run ruff check --config <worker-g>/ruff.toml scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py. Cwd: /private/tmp/a012-ruff-baseline, holding pristine 325f520b contents at those exact relative filenames with original 100644 modes. Exit: 1 (eight inherited findings).

~~~~text
EXE001 Shebang is present but file is not executable
 --> scripts/validate-agent-assets.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Validate Codex, Claude Code, MCP, plugin, and skill assets."""
  |

I001 [*] Import block is un-sorted or un-formatted
  --> scripts/validate-agent-assets.py:4:1
   |
 2 |   """Validate Codex, Claude Code, MCP, plugin, and skill assets."""
 3 |
 4 | / from __future__ import annotations
 5 | |
 6 | | import configparser
 7 | | import fnmatch
 8 | | import json
 9 | | import os
10 | | import posixpath
11 | | import re
12 | | import subprocess
13 | | import sys
14 | | from collections.abc import Iterable
15 | | from functools import cache
16 | | from pathlib import Path
17 | | from typing import Any
18 | |
19 | | import tomllib
   | |______________^
20 |
21 |   try:
   |
help: Organize imports
   |
13 | import sys
14 + import tomllib
15 | from collections.abc import Iterable
16 | from functools import cache
17 | from pathlib import Path
18 | from typing import Any
   -
   - import tomllib
19 |
   |

SIM102 Use a single `if` statement instead of nested `if` statements
   --> scripts/validate-agent-assets.py:139:9
    |
138 |           commands = [hook_command_string(hook) for hook in hooks]
139 | /         if event == "PermissionRequest" and any("permgate" in command for command in commands):
140 | |             if not commands or "permgate" not in commands[0]:
    | |_____________________________________________________________^
141 |                   findings.append(f"permgate-first source={source} event={event} first={commands[0]!r}")
    |
help: Combine `if` statements using `and`

C401 Unnecessary generator (rewrite as a set comprehension)
   --> scripts/validate-agent-assets.py:901:12
    |
899 |             fail(f"MCP server {name} must be disabled by default in the shared manifest")
900 |         agents = server.get("agents", {})
901 |         if set(agent for agent, enabled in agents.items() if enabled) != targets:
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
902 |             fail(f"MCP server {name} must be exposed to every target agent")
903 |         transport = server.get("transport")
    |
help: Rewrite as a set comprehension
    |
900 |         agents = server.get("agents", {})
    -         if set(agent for agent, enabled in agents.items() if enabled) != targets:
901 +         if {agent for agent, enabled in agents.items() if enabled} != targets:
902 |             fail(f"MCP server {name} must be exposed to every target agent")
    |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> scripts/validate-agent-assets.py:958:18
    |
956 |           if path.stat().st_mode & 0o111 == 0:
957 |               fail(f"{path} must be executable")
958 |           result = subprocess.run(
    |  __________________^
959 | |             [str(path)],
960 | |             input="",
961 | |             text=True,
962 | |             stdout=subprocess.PIPE,
963 | |             stderr=subprocess.PIPE,
964 | |             check=False,
965 | |         )
    | |_________^
966 |           if result.returncode != 0:
967 |               fail(f"{path} must run successfully: {result.stderr.strip()}")
    |
help: Replace with `capture_output` keyword argument
    |
961 |             text=True,
    -             stdout=subprocess.PIPE,
    -             stderr=subprocess.PIPE,
962 +             capture_output=True,
963 |             check=False,
    |
note: This is an unsafe fix and may change runtime behavior

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_validate_agent_assets.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Exercise focused checks in validate-agent-assets.py."""
  |

FLY002 Consider f-string instead of string join
   --> tests/unit/test_validate_agent_assets.py:255:13
    |
253 |       def write_codex_config(self, sandbox_workspace_write: str, projects_toml: str = "") -> None:
254 |           (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
255 | /             "\n".join(
256 | |                 [
257 | |                     "#:schema https://developers.openai.com/codex/config-schema.json",
258 | |                     'model = "gpt-5.5"',
259 | |                     'model_reasoning_effort = "high"',
260 | |                     'sandbox_mode = "workspace-write"',
261 | |                     "",
262 | |                     "[sandbox_workspace_write]",
263 | |                     sandbox_workspace_write,
264 | |                     "",
265 | |                     "[features]",
266 | |                     "plugins = true",
267 | |                     "hooks = true",
268 | |                     "plugin_hooks = true",
269 | |                     "",
270 | |                     "[shell_environment_policy]",
271 | |                     'inherit = "core"',
272 | |                     'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
273 | |                     "",
274 | |                     projects_toml,
275 | |                 ]
276 | |             )
    | |_____________^
277 |           )
    |
help: Replace with f-string
    |
254 |         (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
    -             "\n".join(
    -                 [
    -                     "#:schema https://developers.openai.com/codex/config-schema.json",
    -                     'model = "gpt-5.5"',
    -                     'model_reasoning_effort = "high"',
    -                     'sandbox_mode = "workspace-write"',
    -                     "",
    -                     "[sandbox_workspace_write]",
    -                     sandbox_workspace_write,
    -                     "",
    -                     "[features]",
    -                     "plugins = true",
    -                     "hooks = true",
    -                     "plugin_hooks = true",
    -                     "",
    -                     "[shell_environment_policy]",
    -                     'inherit = "core"',
    -                     'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
    -                     "",
    -                     projects_toml,
    -                 ]
    -             )
255 +             f'#:schema https://developers.openai.com/codex/config-schema.json\nmodel = "gpt-5.5"\nmodel_reasoning_effort = "high"\nsandbox_mode = "workspace-write"\n\n[sandbox_workspace_write]\n{sandbox_workspace_write}\n\n[features]\nplugins = true\nhooks = true\nplugin_hooks = true\n\n[shell_environment_policy]\ninherit = "core"\nset = {{ PATH = "{{{{ .chezmoi.homeDir }}}}/.local/bin:/usr/bin:/bin" }}\n\n{projects_toml}'
256 |         )
    |
note: This is an unsafe fix and may change runtime behavior

UP037 [*] Remove quotes from type annotation
    --> tests/unit/test_validate_agent_assets.py:2276:41
     |
2274 |         shutil.rmtree(self.temp_dir)
2275 |
2276 |     def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
     |                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2277 |         return subprocess.run(
2278 |             [sys.executable, str(VALIDATOR), "--mask-secrets", *map(str, paths)],
     |
help: Remove quotes
     |
2275 |
     -     def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
2276 +     def run_mask(self, *paths: Path) -> subprocess.CompletedProcess[str]:
2277 |         return subprocess.run(
     |

Found 8 errors.
[*] 2 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).


~~~~

## Ruff current implementation before independent review

Command: UV_CACHE_DIR=/private/tmp/uv-cache-a012 uv run ruff check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py. Exit: 1 (same eight inherited findings). JSON comparison by relative filename/code/message, ignoring shifted line numbers, reports baseline exit=1 findings=8; current exit=1 findings=8; new_findings=[]; removed_findings=[]; same_finding_set=True. No suppression or unrelated repair.

~~~~text
EXE001 Shebang is present but file is not executable
 --> scripts/validate-agent-assets.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Validate Codex, Claude Code, MCP, plugin, and skill assets."""
  |

I001 [*] Import block is un-sorted or un-formatted
  --> scripts/validate-agent-assets.py:4:1
   |
 2 |   """Validate Codex, Claude Code, MCP, plugin, and skill assets."""
 3 |
 4 | / from __future__ import annotations
 5 | |
 6 | | import configparser
 7 | | import fnmatch
 8 | | import json
 9 | | import os
10 | | import posixpath
11 | | import re
12 | | import subprocess
13 | | import sys
14 | | from collections.abc import Iterable
15 | | from functools import cache
16 | | from pathlib import Path
17 | | from typing import Any
18 | | from urllib.parse import unquote
19 | |
20 | | import tomllib
   | |______________^
21 |
22 |   try:
   |
help: Organize imports
   |
13 | import sys
14 + import tomllib
15 | from collections.abc import Iterable
--------------------------------------------------------------------------------
19 | from urllib.parse import unquote
   -
   - import tomllib
20 |
   |

SIM102 Use a single `if` statement instead of nested `if` statements
   --> scripts/validate-agent-assets.py:140:9
    |
139 |           commands = [hook_command_string(hook) for hook in hooks]
140 | /         if event == "PermissionRequest" and any("permgate" in command for command in commands):
141 | |             if not commands or "permgate" not in commands[0]:
    | |_____________________________________________________________^
142 |                   findings.append(f"permgate-first source={source} event={event} first={commands[0]!r}")
    |
help: Combine `if` statements using `and`

C401 Unnecessary generator (rewrite as a set comprehension)
   --> scripts/validate-agent-assets.py:902:12
    |
900 |             fail(f"MCP server {name} must be disabled by default in the shared manifest")
901 |         agents = server.get("agents", {})
902 |         if set(agent for agent, enabled in agents.items() if enabled) != targets:
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
903 |             fail(f"MCP server {name} must be exposed to every target agent")
904 |         transport = server.get("transport")
    |
help: Rewrite as a set comprehension
    |
901 |         agents = server.get("agents", {})
    -         if set(agent for agent, enabled in agents.items() if enabled) != targets:
902 +         if {agent for agent, enabled in agents.items() if enabled} != targets:
903 |             fail(f"MCP server {name} must be exposed to every target agent")
    |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> scripts/validate-agent-assets.py:959:18
    |
957 |           if path.stat().st_mode & 0o111 == 0:
958 |               fail(f"{path} must be executable")
959 |           result = subprocess.run(
    |  __________________^
960 | |             [str(path)],
961 | |             input="",
962 | |             text=True,
963 | |             stdout=subprocess.PIPE,
964 | |             stderr=subprocess.PIPE,
965 | |             check=False,
966 | |         )
    | |_________^
967 |           if result.returncode != 0:
968 |               fail(f"{path} must run successfully: {result.stderr.strip()}")
    |
help: Replace with `capture_output` keyword argument
    |
962 |             text=True,
    -             stdout=subprocess.PIPE,
    -             stderr=subprocess.PIPE,
963 +             capture_output=True,
964 |             check=False,
    |
note: This is an unsafe fix and may change runtime behavior

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_validate_agent_assets.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Exercise focused checks in validate-agent-assets.py."""
  |

FLY002 Consider f-string instead of string join
   --> tests/unit/test_validate_agent_assets.py:255:13
    |
253 |       def write_codex_config(self, sandbox_workspace_write: str, projects_toml: str = "") -> None:
254 |           (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
255 | /             "\n".join(
256 | |                 [
257 | |                     "#:schema https://developers.openai.com/codex/config-schema.json",
258 | |                     'model = "gpt-5.5"',
259 | |                     'model_reasoning_effort = "high"',
260 | |                     'sandbox_mode = "workspace-write"',
261 | |                     "",
262 | |                     "[sandbox_workspace_write]",
263 | |                     sandbox_workspace_write,
264 | |                     "",
265 | |                     "[features]",
266 | |                     "plugins = true",
267 | |                     "hooks = true",
268 | |                     "plugin_hooks = true",
269 | |                     "",
270 | |                     "[shell_environment_policy]",
271 | |                     'inherit = "core"',
272 | |                     'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
273 | |                     "",
274 | |                     projects_toml,
275 | |                 ]
276 | |             )
    | |_____________^
277 |           )
    |
help: Replace with f-string
    |
254 |         (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
    -             "\n".join(
    -                 [
    -                     "#:schema https://developers.openai.com/codex/config-schema.json",
    -                     'model = "gpt-5.5"',
    -                     'model_reasoning_effort = "high"',
    -                     'sandbox_mode = "workspace-write"',
    -                     "",
    -                     "[sandbox_workspace_write]",
    -                     sandbox_workspace_write,
    -                     "",
    -                     "[features]",
    -                     "plugins = true",
    -                     "hooks = true",
    -                     "plugin_hooks = true",
    -                     "",
    -                     "[shell_environment_policy]",
    -                     'inherit = "core"',
    -                     'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
    -                     "",
    -                     projects_toml,
    -                 ]
    -             )
255 +             f'#:schema https://developers.openai.com/codex/config-schema.json\nmodel = "gpt-5.5"\nmodel_reasoning_effort = "high"\nsandbox_mode = "workspace-write"\n\n[sandbox_workspace_write]\n{sandbox_workspace_write}\n\n[features]\nplugins = true\nhooks = true\nplugin_hooks = true\n\n[shell_environment_policy]\ninherit = "core"\nset = {{ PATH = "{{{{ .chezmoi.homeDir }}}}/.local/bin:/usr/bin:/bin" }}\n\n{projects_toml}'
256 |         )
    |
note: This is an unsafe fix and may change runtime behavior

UP037 [*] Remove quotes from type annotation
    --> tests/unit/test_validate_agent_assets.py:2497:41
     |
2495 |         shutil.rmtree(self.temp_dir)
2496 |
2497 |     def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
     |                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2498 |         return subprocess.run(
2499 |             [sys.executable, str(VALIDATOR), "--mask-secrets", *map(str, paths)],
     |
help: Remove quotes
     |
2496 |
     -     def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
2497 +     def run_mask(self, *paths: Path) -> subprocess.CompletedProcess[str]:
2498 |         return subprocess.run(
     |

Found 8 errors.
[*] 2 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).

~~~~

## Other pre-review checks

Command: UV_CACHE_DIR=/private/tmp/uv-cache-a012 uv run ruff format --config ruff.toml --check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py

Exit: 0.

~~~~text
2 files already formatted
~~~~

Command: git diff --check

Exit: 0; no output.

Crit status --json reports review_file_exists=false, daemon.running=false and sessions=[]; no Crit data is available. An independent read-only worker review and saved JSON/receipt will replace it as AGENTS requires. No browser or human review is requested.

Full make validate-agent-assets, final-base source hashes, exact committed-range inventory, review gate, CI and the bounded automatic-review observation will be appended after their actual execution. No final-head claim is made by this draft.

## Single independent worker review and consolidated correction

Review: clean a99521b446de5796393ce4f9654136fda4f6e95d, merge base 3e41e36abc949acd7e6b4859c1a22df9e665c8d4. One native read-only independent agent, not a task-level audit/security-profile review. Two findings: a05-worker-review-1 P1 (raw/intermediate stripped spelling lost by ANSI-C escape decoding); a05-worker-review-2 P2 (fake fence closer and quoted fence code classification). No second independent review. The single fix round is e37be90d9aef1c2371529cf02b7266e1645f597e.

RED command: UV_CACHE_DIR=/private/tmp/uv-cache-a012 GIT_CONFIG_GLOBAL=/dev/null uv run --no-project --with pyyaml python -m unittest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus -v. Source unchanged from a99521b4; only the reproductions added to tests. Exit 1, four reproduction failures. The fifth note-only control passed.

### Exact pre-correction RED output

~~~~text
test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) ... 
  test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) (provenance='a05-worker-review-1', case='bare-escape-api') ... FAIL
  test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) (provenance='a05-worker-review-1', case='bare-escape-oauth') ... FAIL
  test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) (provenance='a05-worker-review-2', case='fence-prefix') ... FAIL
  test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) (provenance='a05-worker-review-2', case='quoted-fence') ... FAIL

======================================================================
FAIL: test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) (provenance='a05-worker-review-1', case='bare-escape-api')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-g/tests/unit/test_validate_agent_assets.py", line 2048, in assert_anthropic_a03_cases
    self.assertEqual(row["exit_status"], int(refused), stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : 

======================================================================
FAIL: test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) (provenance='a05-worker-review-1', case='bare-escape-oauth')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-g/tests/unit/test_validate_agent_assets.py", line 2048, in assert_anthropic_a03_cases
    self.assertEqual(row["exit_status"], int(refused), stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : 

======================================================================
FAIL: test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) (provenance='a05-worker-review-2', case='fence-prefix')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-g/tests/unit/test_validate_agent_assets.py", line 2048, in assert_anthropic_a03_cases
    self.assertEqual(row["exit_status"], int(refused), stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : NOTE: home/example.md:3: note: credential name in a comment or Markdown prose


======================================================================
FAIL: test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) (provenance='a05-worker-review-2', case='quoted-fence')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-g/tests/unit/test_validate_agent_assets.py", line 2048, in assert_anthropic_a03_cases
    self.assertEqual(row["exit_status"], int(refused), stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : NOTE: home/example.md:2: note: credential name in a comment or Markdown prose


----------------------------------------------------------------------
Ran 1 test in 11.805s

FAILED (failures=4)

~~~~

### Command: same environment and unittest runner, test_anthropic_check_bypass_corpus and test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule. Exit 0 after the one source correction. Includes all 425 corpus rows and controls.

~~~~text
test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) ... ok
test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule) ... ok

----------------------------------------------------------------------
Ran 2 tests in 12.704s

OK

~~~~

### Command: UV_CACHE_DIR=/private/tmp/uv-cache-a012 GIT_CONFIG_GLOBAL=/dev/null uv run --no-project --with pyyaml python -m unittest tests/unit/test_validate_agent_assets.py -v. Exit 0; 122 tests, no skips; source/test contents committed in e37be90d.

~~~~text
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) ... ok
test_anthropic_auth_route_normalizes_shell_names_and_refuses_unreadable_names (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_normalizes_shell_names_and_refuses_unreadable_names) ... ok
test_anthropic_auth_route_parses_both_platform_renderings_of_chezmoi_templates (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_parses_both_platform_renderings_of_chezmoi_templates) ... ok
test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty) ... ok
test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment) ... ok
test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty) ... ok
test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter) ... ok
test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_json_and_toml_through_their_parsers) ... ok
test_anthropic_auth_route_reads_yaml_through_its_parser (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_yaml_through_its_parser) ... ok
test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text) ... ok
test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) ... ok
test_anthropic_check_accepts_an_environment_reference_followed_by_a_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_accepts_an_environment_reference_followed_by_a_command) ... ok
test_anthropic_check_bypass_corpus (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_bypass_corpus) ... ok
test_anthropic_check_decodes_ansi_c_escaped_names (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_decodes_ansi_c_escaped_names) ... ok
test_anthropic_check_keeps_single_quote_semantics_for_backslashes (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_keeps_single_quote_semantics_for_backslashes) ... ok
test_anthropic_check_parses_each_fenced_example_with_a_fresh_quote_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_parses_each_fenced_example_with_a_fresh_quote_state) ... ok
test_anthropic_check_redacts_assignment_payloads_in_diagnostics (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_redacts_assignment_payloads_in_diagnostics) ... ok
test_anthropic_check_refuses_an_env_option_it_cannot_classify_before_an_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_env_option_it_cannot_classify_before_an_assignment) ... ok
test_anthropic_check_refuses_an_unresolved_env_prefix_before_a_dynamic_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_unresolved_env_prefix_before_a_dynamic_assignment) ... ok
test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule) ... ok
test_anthropic_check_refuses_parse_failures_and_missing_yaml_without_disclosing_payloads (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_refuses_parse_failures_and_missing_yaml_without_disclosing_payloads) ... ok
test_anthropic_check_rejects_undecodable_name_forms (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_rejects_undecodable_name_forms) ... ok
test_anthropic_check_splits_shell_text_on_lf_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_splits_shell_text_on_lf_only) ... ok
test_anthropic_check_uses_the_unchanged_whole_line_for_allowance (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_check_uses_the_unchanged_whole_line_for_allowance) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/validate-agent-assets-test-y7kdbiwl/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok

----------------------------------------------------------------------
Ran 122 tests in 22.313s

OK

~~~~

### Command: UV_CACHE_DIR=/private/tmp/uv-cache-a012 uv run ruff check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py. Exit 1. JSON comparison with pristine 325f520b at original filenames again gives baseline exit=1 findings=8, fixed exit=1 findings=8, new_findings=[], same_finding_set=True.

~~~~text
EXE001 Shebang is present but file is not executable
 --> scripts/validate-agent-assets.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Validate Codex, Claude Code, MCP, plugin, and skill assets."""
  |

I001 [*] Import block is un-sorted or un-formatted
  --> scripts/validate-agent-assets.py:4:1
   |
 2 |   """Validate Codex, Claude Code, MCP, plugin, and skill assets."""
 3 |
 4 | / from __future__ import annotations
 5 | |
 6 | | import configparser
 7 | | import fnmatch
 8 | | import json
 9 | | import os
10 | | import posixpath
11 | | import re
12 | | import subprocess
13 | | import sys
14 | | from collections.abc import Iterable
15 | | from functools import cache
16 | | from pathlib import Path
17 | | from typing import Any
18 | | from urllib.parse import unquote
19 | |
20 | | import tomllib
   | |______________^
21 |
22 |   try:
   |
help: Organize imports
   |
13 | import sys
14 + import tomllib
15 | from collections.abc import Iterable
--------------------------------------------------------------------------------
19 | from urllib.parse import unquote
   -
   - import tomllib
20 |
   |

SIM102 Use a single `if` statement instead of nested `if` statements
   --> scripts/validate-agent-assets.py:140:9
    |
139 |           commands = [hook_command_string(hook) for hook in hooks]
140 | /         if event == "PermissionRequest" and any("permgate" in command for command in commands):
141 | |             if not commands or "permgate" not in commands[0]:
    | |_____________________________________________________________^
142 |                   findings.append(f"permgate-first source={source} event={event} first={commands[0]!r}")
    |
help: Combine `if` statements using `and`

C401 Unnecessary generator (rewrite as a set comprehension)
   --> scripts/validate-agent-assets.py:902:12
    |
900 |             fail(f"MCP server {name} must be disabled by default in the shared manifest")
901 |         agents = server.get("agents", {})
902 |         if set(agent for agent, enabled in agents.items() if enabled) != targets:
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
903 |             fail(f"MCP server {name} must be exposed to every target agent")
904 |         transport = server.get("transport")
    |
help: Rewrite as a set comprehension
    |
901 |         agents = server.get("agents", {})
    -         if set(agent for agent, enabled in agents.items() if enabled) != targets:
902 +         if {agent for agent, enabled in agents.items() if enabled} != targets:
903 |             fail(f"MCP server {name} must be exposed to every target agent")
    |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> scripts/validate-agent-assets.py:959:18
    |
957 |           if path.stat().st_mode & 0o111 == 0:
958 |               fail(f"{path} must be executable")
959 |           result = subprocess.run(
    |  __________________^
960 | |             [str(path)],
961 | |             input="",
962 | |             text=True,
963 | |             stdout=subprocess.PIPE,
964 | |             stderr=subprocess.PIPE,
965 | |             check=False,
966 | |         )
    | |_________^
967 |           if result.returncode != 0:
968 |               fail(f"{path} must run successfully: {result.stderr.strip()}")
    |
help: Replace with `capture_output` keyword argument
    |
962 |             text=True,
    -             stdout=subprocess.PIPE,
    -             stderr=subprocess.PIPE,
963 +             capture_output=True,
964 |             check=False,
    |
note: This is an unsafe fix and may change runtime behavior

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_validate_agent_assets.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Exercise focused checks in validate-agent-assets.py."""
  |

FLY002 Consider f-string instead of string join
   --> tests/unit/test_validate_agent_assets.py:255:13
    |
253 |       def write_codex_config(self, sandbox_workspace_write: str, projects_toml: str = "") -> None:
254 |           (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
255 | /             "\n".join(
256 | |                 [
257 | |                     "#:schema https://developers.openai.com/codex/config-schema.json",
258 | |                     'model = "gpt-5.5"',
259 | |                     'model_reasoning_effort = "high"',
260 | |                     'sandbox_mode = "workspace-write"',
261 | |                     "",
262 | |                     "[sandbox_workspace_write]",
263 | |                     sandbox_workspace_write,
264 | |                     "",
265 | |                     "[features]",
266 | |                     "plugins = true",
267 | |                     "hooks = true",
268 | |                     "plugin_hooks = true",
269 | |                     "",
270 | |                     "[shell_environment_policy]",
271 | |                     'inherit = "core"',
272 | |                     'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
273 | |                     "",
274 | |                     projects_toml,
275 | |                 ]
276 | |             )
    | |_____________^
277 |           )
    |
help: Replace with f-string
    |
254 |         (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
    -             "\n".join(
    -                 [
    -                     "#:schema https://developers.openai.com/codex/config-schema.json",
    -                     'model = "gpt-5.5"',
    -                     'model_reasoning_effort = "high"',
    -                     'sandbox_mode = "workspace-write"',
    -                     "",
    -                     "[sandbox_workspace_write]",
    -                     sandbox_workspace_write,
    -                     "",
    -                     "[features]",
    -                     "plugins = true",
    -                     "hooks = true",
    -                     "plugin_hooks = true",
    -                     "",
    -                     "[shell_environment_policy]",
    -                     'inherit = "core"',
    -                     'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
    -                     "",
    -                     projects_toml,
    -                 ]
    -             )
255 +             f'#:schema https://developers.openai.com/codex/config-schema.json\nmodel = "gpt-5.5"\nmodel_reasoning_effort = "high"\nsandbox_mode = "workspace-write"\n\n[sandbox_workspace_write]\n{sandbox_workspace_write}\n\n[features]\nplugins = true\nhooks = true\nplugin_hooks = true\n\n[shell_environment_policy]\ninherit = "core"\nset = {{ PATH = "{{{{ .chezmoi.homeDir }}}}/.local/bin:/usr/bin:/bin" }}\n\n{projects_toml}'
256 |         )
    |
note: This is an unsafe fix and may change runtime behavior

UP037 [*] Remove quotes from type annotation
    --> tests/unit/test_validate_agent_assets.py:2572:41
     |
2570 |         shutil.rmtree(self.temp_dir)
2571 |
2572 |     def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
     |                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2573 |         return subprocess.run(
2574 |             [sys.executable, str(VALIDATOR), "--mask-secrets", *map(str, paths)],
     |
help: Remove quotes
     |
2571 |
     -     def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
2572 +     def run_mask(self, *paths: Path) -> subprocess.CompletedProcess[str]:
2573 |         return subprocess.run(
     |

Found 8 errors.
[*] 2 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).

~~~~

Other fixed-source checks:

~~~~text
fixed_allowlist_regex_byte_identical=True
real_applied_tree_auth_check=pass
~~~~

The importlib/task-regex/applied-tree command described above was rerun after the sole correction and exited 0. The format check again exited 0 (2 files already formatted); git diff --check exited 0 with no output. Crit comments --all --json <status-selected review file> exited 1 (file absent), consistent with review_file_exists=false. No browser review was opened.

Root read a05-worker-review.json, whose two resolved line records document both fixes, then ran:

AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/a05-worker-receipt.md make require-crit-review

Exit 0.

~~~~text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
~~~~

The first unevidenced gate exited 2: it required native review and included unrelated untracked prior-task worklogs in its broad-diff measurement. Those artifacts were not modified or committed in a05. This is worker process evidence, not final-head acceptance or an audit.

## Post-round bounded verification: OPEN P2

A direct call to anthropic_text_findings(text, '', markdown=True) on e37be90d confirms a05-worker-verification-1: a list-contained fence with a bare credential name emits note at line 2, where code requires a hard finding. Exact fixture and output: post-round-open.json. No payload is involved; assignment-bearing text still gets hard refusal. This P2 remains open and was reported to the orchestrator; no second correction or owner disposition is claimed. The two independent-review findings passed their fresh regressions; no surviving P0/P1 was observed. The full module's green result is bounded by this explicitly failing policy check.


