# 統合内部契約 IC01–IC18

版4.0.0。以下はregisters/integrated_contracts.jsonの生成表示。各契約は同じ開始・実行・変更・受け入れに適用する。DSH runtimeや新しい合否正本を追加しない。全契約はSPECIFIED_NOT_IMPLEMENTED。

<a id="ic01"></a>

## IC01：能力契約と操作開始判定

**責任者:** AdapterRegistry / QualificationService。**主担当:** WP04。**要求:** R13, R14, R15, R18, R20, R25, R35

**データ仕様:** OperationCapability: operation、requested、advertised、observed(passed/failed/unknown)、provider_id、binary_digest、composition_digest、environment_digest、probe_evidence_ref、qualified_at、expires_at、qualification_revision。resume/steer/structured_output/permission/cancel/skill/hook/sandbox/model/effortは独立した能力項目。

**正常経路:** Service Definitionが入力・出力・失敗・所有権を宣言し、Providerが実装、Consumerが必要能力を明示する。資格確認サービスは実probeの結果を保存し、操作受付側はその時点のbinary/構成/環境と一致するobserved能力を照合する。必要能力がすべてpassedの場合だけ処理を進める。

**失敗・拒否:** 未知能力、宣言のみの能力、期限切れ資格、必要能力不足は開始拒否。形式不正400、未対応422、旧資格またはhash相違409、認証/認可不足401/403。modelとeffortを黙って置換しない。内部計算量の非公開と公式runtimeでの有効設定未確認を区別する。

**適用境界:** 起動時検査だけに頼らず、start/resume/steer/cancel等の実操作入口で再照合する。公式CLIが提供しない観測を推測しない。Cordis ctxやDSH providerを本製品の実装済能力として扱わない。

### 操作契約（後続実装）

- `qualify(runtime, required_capabilities) -> qualification_ref`
- `admit(operation, run_binding, qualification_ref) -> permit_or_error`

**実装対象:** `src/adh/domain/capabilities.py`, `src/adh/adapters/contracts.py`, `src/adh/qualification/`, `contracts/capabilities/`

**分担WP:** WP00, WP01, WP02, WP04, WP06, WP10, WP12, WP14, WP15, WP16, WP20, WP26, WP31

**必須検証:** V04-01-S01, V26-01-S01, V04-01-S02, V26-03-S01

**出典:** DSH-S01, DSH-S02, DSH-S07

**既存統合条件:** モデル/profileのrequested/observedとSkill/subagent overrideをMO09で確認する。

<a id="ic02"></a>

## IC02：実行領域・Worktree・検証snapshotの整合

**責任者:** RunnerService / SnapshotService。**主担当:** WP09。**要求:** R06, R16, R19, R20, R22, R30, R34

**データ仕様:** ExecutionBinding: project_id/task_id/run_id/attempt/fence、repository_id、worktree_id、workspace_ref、execution_scope_id、source_root、artifact_root、phase、snapshot_ref。BoundaryCapability: files/network/process/credentialsごとのrequiredとobserved(full/partial/unavailable)。

**正常経路:** 実装中のread/write/shell/任意のterminal・LSPは、同じtask/attemptのwriter ExecutionBindingを使う。正式検証はwriter停止後に凍結し、別のVerifier ExecutionBindingへ同一snapshotをmaterializeする。両領域の実行identityは別、検証対象source digestは一致させる。

**失敗・拒否:** host readとVM testの混在、mainへの暗黙redirect、別worktree参照、外部symlink、必要境界がpartialの過大表示は拒否する。freeze未完了ではcandidate公開不可。別taskへの越境は403、対象不一致409、未対応platform/boundaryは422。

**適用境界:** WorktreeはOS認可ではない。同一実行領域という条件はwriter内の操作整合であり、独立Verifierをwriterと同じ権限・VMへ統合する意味ではない。FS/通信/process/資格情報の保証は別々に検証する。

### 操作契約（後続実装）

- `bind_task(attempt, workspace, scope) -> execution_binding`
- `freeze(writer_binding) -> immutable_snapshot`
- `materialize(snapshot, verifier_scope) -> verifier_binding`

**実装対象:** `src/adh/domain/execution.py`, `src/adh/snapshots/`, `src/adh/runner/`, `deployment/`

**分担WP:** WP09, WP10, WP12, WP13, WP14, WP15, WP16, WP20, WP24, WP26, WP29

**必須検証:** V14-05-S01, V20-01-S01, V09-03-S01, V29-01-S01

**出典:** DSH-S01, DSH-S14

<a id="ic03"></a>

## IC03：実効構成・能力資格・更新の固定

**責任者:** CompositionResolver / QualificationService。**主担当:** WP06。**要求:** R13, R14, R15, R29, R30, R33

**データ仕様:** EffectiveComposition: requested_models、observed_configuration、native binary/version/digest、plugin payload commit/runtime closure、Skill name/path/hash、Hook enabled/trusted/probe、設定source・優先順位・selected/rejected理由、provider、permission、composition_digest。Auth bytesは含めない。

**正常経路:** 一つの管理manifestからrole profileを作り、公式runtimeが実際に解決した構成と照合する。nativeの設定優先順位を尊重し、どの定義が選ばれたかを証拠化する。実行中は参照payloadを不変とし、新版は資格済の新runから適用する。

**失敗・拒否:** 必須Skill欠落・不正frontmatter・同名shadow・Hook未信頼・payload driftを検出し、資格を無効化して新admissionを止める。意図しないlive差替えは安全停止・照合へ。承認された旧runの不変payloadを、新版が出たという理由だけで書き換えない。

**適用境界:** 本製品のdumpは実効構成の観測結果でありDSH dump-configを公式CLIへ付加するものではない。未知状態をenabled扱いにしない。初期本人認証・Hook信頼をハーネスが偽装しない。

### 操作契約（後続実装）

- `resolve(role, declared_manifest) -> resolution_trace`
- `verify_effective(runtime, trace) -> composition_digest`
- `activate(qualified_revision, new_run_only) -> activation_record`

**実装対象:** `src/adh/assets/`, `skill-pack/`, `policies/`, `contracts/composition/`

**分担WP:** WP01, WP06, WP10, WP12, WP15, WP16, WP24, WP26, WP30

**必須検証:** V06-02-S01, V26-02-S01, V06-05-S01, V30-04-S01

**出典:** DSH-S01, DSH-S19, DSH-S20

**既存統合条件:** prompt/role/renderer/Skill routeの版をpackとして固定し、MO02/MO10/MO12で重複・更新を管理する。

<a id="ic04"></a>

## IC04：確定状態・永続イベント・再生成可能な投影

**責任者:** SupervisorStore / ProjectionService。**主担当:** WP07。**要求:** R17, R24, R29, R31, R34, R35

**データ仕様:** EventEnvelope: event_id/project_id/task_id/run_id/attempt、event_class(domain/native_observation/ephemeral)、schema_version、committed_seq、recorded_at、source_event_ref、payload。Projection: state_version、baseline_revision、as_of_seq、scope、values。

**正常経路:** Supervisor管理DBだけが工程正本。domain更新とevent/outboxを同transactionでcommitする。UI/status/記憶投影は一つの整合read cutから作り、反映済sequenceを返す。cache消失・版違いは正本DBと確定eventから再構成する。

**失敗・拒否:** 未commit通知、未来cursor、旧stateVersion、他project eventを状態確定に使わない。過去の成功事実を削除せず、訂正/失効eventを追記する。native時刻・native statusをdomain確定と同一視しない。

**適用境界:** 全面event-sourcingへの置換ではない。監査再生はread-onlyで外部dispatchを起こさない。公式CLI内部の非公開contextや未記録状態まで完全再生したとは表示しない。

### 操作契約（後続実装）

- `commit_domain_change(change, event, outbox) -> committed_seq`
- `project(scope, state_version) -> consistent_snapshot`
- `rebuild_projection(scope) -> as_of_seq`

**実装対象:** `src/adh/storage/`, `src/adh/projections/`, `src/adh/observability/`, `migrations/`

**分担WP:** WP07, WP08, WP12, WP15, WP16, WP23, WP24, WP25, WP27, WP29, WP30

**必須検証:** V07-03-S01, V25-06-S01, V12-05-S01, V25-06-S02

**出典:** DSH-S01, DSH-S08

<a id="ic05"></a>

## IC05：永続化後のdispatchと不明結果の照合

**責任者:** DispatchService / SupervisorStore / Runner receipt ledger。**主担当:** WP07。**要求:** R17, R22, R24, R25, R28, R31, R34

**データ仕様:** DispatchIntent: dispatch_id、idempotency_key、task/run/attempt/fence、contract_hash、grant_ref、qualification_ref、composition_digest、execution_binding_ref、operation、payload_hash、committed_seq、delivery_state。RunnerReceipt: dispatch_id、observed_run_identity、receipt_state、durable_at。

**正常経路:** 権限・予算・資格・領域・契約を照合し、intentとoutboxをcommitしてから送信する。Runnerは認証済dispatch_idを重複排除し、その受領と実run identityを耐久記録する。native開始/再開の応答が得られて初めて対応IDを確定する。

**失敗・拒否:** commit前のdisk-full/異常終了では外部呼出0。commit後・応答前に切れた場合はDISPATCH_UNKNOWNとして停止し、Runner/native/session/effectを照合する。未実行の証拠があるか、受信側冪等性が確認できる場合だけ安全再送する。

**適用境界:** 外部から制御可能なtask開始/再開/Runner/effect境界に適用する。公式CLI内部の全model requestや全toolの永続化を外側から保証しない。Runnerの受領台帳は資源/配送の記録で、第二のproject state authorityではない。

### 操作契約（後続実装）

- `prepare_dispatch(contract, grant, binding) -> durable_intent`
- `deliver(intent) -> receipt_or_unknown`
- `reconcile_dispatch(intent) -> not_started|running|finished|unknown`

**実装対象:** `src/adh/dispatch/`, `src/adh/storage/`, `src/adh/runner/`, `src/adh/effects/`

**分担WP:** WP07, WP14, WP15, WP16, WP17, WP23, WP26, WP27, WP29

**必須検証:** V07-03-S02, V26-01-S02, V07-02-S01, V23-02-S01

**出典:** DSH-S06

**既存統合条件:** dispatch intentにはTaskPacket・PromptPlan・model packのdigestを含める。

<a id="ic06"></a>

## IC06：目標・許可・常駐worker・継続文脈の分離

**責任者:** SupervisorScheduler / MandateAuthority / Native adapters。**主担当:** WP11。**要求:** R02, R11, R18, R21, R23, R24, R25, R32

**データ仕様:** GoalRef: objective/requirement_ids/baseline_revision。ExecutionAuthorization: grant/stop_reason/budget/epoch/qualification/expiry。Continuation: task/attempt/exact_session_or_thread_id/continuation_mode/session_compatibility/handoff_ref。

**正常経路:** 目標がactiveでも、状態・権限・予算・照合の許可が揃わなければ進めない。常駐Codex workerはworktreeに結び付け順次割当。同じtaskの修正は原則exact sessionで継続し、独立reviewは作者履歴を引き継がない新sessionとする。

**失敗・拒否:** USER_STOP/BUDGET/AUTH/RECONCILINGをgoal activeで解除しない。旧handoffやround上限を達成と認定しない。attemptでworkspaceが変わる場合はnativeの安全な再束縛能力を確認し、未対応なら認可された新sessionへ引継ぐ。旧cwdへ黙って再開しない。

**適用境界:** Ralphを第二のproject loopとして追加しない。freshは独立reviewと認可された再構成に用い、各taskでCodexを無条件spawnする方式へ変更しない。native Goal/Workflowは資格済の場合のtask内部手段で、合否や外部予算の上書き権限を持たない。

### 操作契約（後続実装）

- `evaluate_next_action(goal, state, grant, budget) -> allowed_action|pause`
- `resume_exact(binding, compatibility) -> session_or_error`
- `build_handoff(current_state, evidence) -> bounded_handoff`

**実装対象:** `src/adh/budgets/`, `src/adh/scheduler/`, `src/adh/recovery/`, `workflows/`

**分担WP:** WP08, WP10, WP11, WP15, WP16, WP19, WP22, WP24, WP25, WP28

**必須検証:** V22-01-S01, V28-06-S01, V11-06-S01, V22-05-S01

**出典:** DSH-S09, DSH-S10, DSH-S11, DSH-S17, DSH-S18, DSH-S21

**既存統合条件:** MO04/MO07により明示委任の範囲で完遂し、履歴所有と正確なID再開を保持する。

<a id="ic07"></a>

## IC07：上流から統合までの型付きDAGと耐久配送

**責任者:** WorkflowPlanner / Scheduler / AgmsgBridge。**主担当:** WP10。**要求:** R03, R04, R07, R08, R10, R12, R16, R17, R18, R24, R26

**データ仕様:** WorkflowNode: node_id、kind(research/analysis/experiment/decision/specification/plan/implementation/verification/review/integration/release)、input_refs、output_contract、dependencies、scope、acceptance_rule、budget_ref。MessageReceipt: message_id/task/run/attempt/fence、payload_hash、received_durable_seq、ack_state。

**正常経路:** 同じDAG契約で、並列調査→候補別実験→結果照合→ADR/仕様→実装→独立検証→直列統合を扱う。未確定設計の調査nodeはInputBaseline/Mandateに束ね、設計凍結を循環前提にしない。下流joinは必要な実結果と受入を照合する。配送は受領耐久化後にackし、重複通知でもclaimは一つ。

**失敗・拒否:** 循環/不存在依存、古いfence、別project sender、ack前crash、scope重複を拒否/照合する。agmsg read_atは輸送上の観測であり業務受領や完了とは同一視しない。actor認可は管理API/mTLSで行う。

**適用境界:** agmsgを別busへ置換しない。Supervisor管理DBに業務inbox/outboxを置き、複数VMへSQLiteをmountしない。自由生成JSを管理processへ渡さず、許可されたnode種と契約を実行する。exactly-once外部作用は保証しない。

### 操作契約（後続実装）

- `validate_workflow(nodes, baseline, mandate) -> executable_dag`
- `receive_message(envelope, authenticated_actor) -> durable_receipt`
- `schedule_ready(dag, resources, grants) -> bounded_assignments`

**実装対象:** `src/adh/workflows/`, `src/adh/scheduler/`, `src/adh/messaging/`, `workflows/`

**分担WP:** WP05, WP07, WP10, WP17, WP18, WP19, WP22, WP24, WP27, WP28

**必須検証:** V19-01-S01, V17-02-S01, V17-05-S01, V10-01-S01

**出典:** DSH-S12, DSH-S13

**既存統合条件:** MO05の独立取得と委任待ち中の統括作業を、同じDAG/資源・予算条件で実行する。

<a id="ic08"></a>

## IC08：run所有権・停止完了・直交する終了情報

**責任者:** Runner lifecycle controller / Native adapter。**主担当:** WP14。**要求:** R16, R17, R24, R25, R31, R34

**データ仕様:** RunOutcome: run_id/attempt/fence、owner_identity、process_group_identity、published、timed_out、cancelled、signal、exit_code、stop_reason、quiescence_ref、partial_artifacts。

**正常経路:** 一つのrunに一つのlifecycle ownerを置く。外部公開前は起動側が資源を所有して失敗時に回収し、公開後はRunnerのrun ownerが終了まで所有する。停止はadmission閉鎖→取消→grace→強制停止→子孫静止確認の順とする。

**失敗・拒否:** SIGTERM後exit0でもtimeout/cancelledを消さない。observer例外は隔離して記録するが、認可/永続化の失敗は処理継続しない。停止確定が受入commitに先行した場合はlate successで再開/acceptedにせず候補証拠として保持する。

**適用境界:** fenceは古い結果の受理を防ぐが既存processを停止させない。ACK/exit0/PIDだけで安全な再割当としない。PID再利用、孫process、起動失敗、遅延callbackを対象にする。

### 操作契約（後続実装）

- `publish_run(started_resources) -> owned_run`
- `stop_run(run, reason) -> quiescence_or_reconciling`
- `observe_outcome(raw_outcomes) -> orthogonal_outcome`

**実装対象:** `src/adh/runner/`, `src/adh/adapters/claude/`, `src/adh/adapters/codex/`, `src/adh/recovery/`

**分担WP:** WP03, WP11, WP14, WP15, WP16, WP20, WP22, WP26, WP27, WP29

**必須検証:** V14-01-S01, V26-01-S03, V14-01-S02, V14-06-S01

**出典:** DSH-S02, DSH-S03, DSH-S07

<a id="ic09"></a>

## IC09：原本参照付き文脈投影と判定情報の保持

**責任者:** EvidenceStore / ContextProjectionService。**主担当:** WP18。**要求:** R03, R05, R06, R20, R27, R29, R30, R31, R32, R34

**データ仕様:** ContextEnvelope: source_digest、redacted_digest、baseline_revision、source_locator、ranges、omitted、retrieval_ref、projection_version、measured_bytes、token_estimate_method、structured_findings。structured_findingsはexit/failed/skipped/unresolved_requirementsを保持する。

**正常経路:** 資料とログの許可された原本をACL付きEvidence Storeに保存し、モデルには範囲・省略・取得手段を持つ上限付き表現を送る。hashと実内容を再確認して取得できる。要件、例外条件、失敗件数、未解決指摘を単なるhead/tail要約だけに任せない。

**失敗・拒否:** 中央のFAIL/skip/例外条項、古いsummary、欠けたsource参照、秘密入り出力を検出し、必要範囲の再取得または不合格へ。秘密除去後に元hashと同じと装わず変換を記録する。Auth bytesは保存・配布しない。

**適用境界:** 公式CLI内部のcompaction/KV cacheを制御したとは主張しない。短縮対象は本製品が外部から渡すcontextのみ。文字数とtoken数を区別し、未知usageを0計上しない。

### 操作契約（後続実装）

- `store_source(bytes, acl, redaction_policy) -> source_ref`
- `project_context(source_refs, budget) -> context_envelope`
- `retrieve_range(ref, actor, range) -> verified_content`

**実装対象:** `src/adh/evidence/`, `src/adh/context/`, `src/adh/memory/`, `workflows/research/`

**分担WP:** WP03, WP09, WP12, WP16, WP17, WP18, WP20, WP21, WP24, WP25, WP28, WP30

**必須検証:** V25-01-S01, V28-06-S02, V20-05-S01, V25-04-S01

**出典:** DSH-S05, DSH-S01

**既存統合条件:** MO03のReadLedgerとcontext epochを使い、必要文脈を失わず重複供給を減らす。

<a id="ic10"></a>

## IC10：上流設計・producer/consumer・外向き契約のレビュー

**責任者:** DesignWorkflow / Independent Reviewer / Contract tooling。**主担当:** WP02。**要求:** R03, R04, R05, R07, R08, R09, R10, R11, R12, R21, R35

**データ仕様:** DecisionDossier: requirements、sources/claims、alternatives、experiments、ADR、producer/consumer表、normal/error/cancel/disposal/limits、default_rationale、model_visible_contract、review_findings。

**正常経路:** 実consumerと所有者を持つ契約を先に定義し、呼出側・実装側・モデルに渡すschema/result・利用者向け診断を同時レビューする。生成可能なAPI一覧は契約から生成し、意味的妥当性は別sessionのA3が一次資料と実験に戻って判断する。

**失敗・拒否:** 未使用抽象、無根拠default、片側だけの契約、NFR省略、エラーcodeと手引の不一致、未実行実験を拒否する。仕様に関わる指摘は実装都合でwaiveせず変更手続を通す。

**適用境界:** Superpowersを置換せず同じ上流工程の品質条件に統合する。DSH固有のnamed export/Cordis injectをPythonへ強制しない。私的推論全文は証拠として要求しない。

### 操作契約（後続実装）

- `review_contract(producer, consumers, baseline, evidence) -> findings`
- `validate_dossier(dossier) -> structural_result`
- `independent_semantic_review(dossier) -> review_receipt`

**実装対象:** `contracts/`, `docs/architecture/`, `src/adh/design/`, `workflows/design/`

**分担WP:** WP02, WP03, WP04, WP18, WP19, WP21, WP28, WP30

**必須検証:** V02-02-S01, V04-06-S01, V02-02-S02, V04-06-S02

**出典:** DSH-S07, DSH-S15, DSH-S16

**既存統合条件:** MO08で上流根拠・範囲・引用と要約を確認し、model-facing契約の意味を独立reviewする。

<a id="ic11"></a>

## IC11：実配布entry・実世界の変化・退行検出の検証

**責任者:** Quality tooling / Independent Verifier / Release authority。**主担当:** WP03。**要求:** R20, R21, R22, R26, R27, R30, R33, R34, R35

**データ仕様:** TestExecution: entry_kind(source/built_installed/recorded_boundary/live_native)、candidate_digest、test_definition_digest、execution_binding、observed_file_manifest、untouched_manifest、exit/counts/artifact_refs、mutation_id、expected_detection。

**正常経路:** mockは不確定/高コスト境界だけに限定し、下流の本物のstore/adapter/判定を通す。releaseはclean installした実entryから始め、出力treeと変更禁止領域を外部から比較する。native公開frameの記録再生は契約回帰、実Auth/E2Eは別試験として実施する。

**失敗・拒否:** AgentのPASS文だけ、built artifactだけの破損、ゼロ件/全skip、ログ中央失敗、重要比較を外したmutation、並列port共有を検出し必ず失敗することを確認する。基準を下げず修正後新RCで再試験。

**適用境界:** 192論理項目・統合subcase・実収集test件数・18 AI runを混同しない。keyless/replayを実AI結果へ昇格しない。有限試験で未知欠陥ゼロを主張しない。

### 操作契約（後続実装）

- `run_inventory(frozen_candidate, qualified_environment) -> check_receipt`
- `verify_world(candidate, expected, untouched) -> external_diff`
- `test_mutation(control_mutation) -> detected_failure`

**実装対象:** `tests/`, `quality/`, `src/adh/verifier/`, `docs/runbooks/`

**分担WP:** WP00, WP02, WP03, WP04, WP20, WP21, WP24, WP26, WP28, WP29, WP30, WP31

**必須検証:** V30-01-S01, V28-01-S01, V03-04-S01, V29-05-S01

**出典:** DSH-S04, DSH-S07, DSH-S16

**既存統合条件:** MO11/MO12の行動・効率・更新試験を固定oracleへ結び、文書QAを製品合格へ加算しない。

<a id="ic12"></a>

## IC12：モデル別の指示・Skills・文脈・評価を一体化する契約

**責任者:** 既存Assets/Qualification/Context services + IndependentEvaluator。**主担当:** WP04。**要求:** R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R27, R29, R30, R31, R32, R33, R34, R35

**データ仕様:** ModelExecutionProfile、PromptPlan、TaskPacket、ReadLedgerEntry、SkillRoute、OptimizationRun、OptimizationQualification。prompt/profile/renderer/catalog digestは既存policy/assets hashへ束ねる。

**正常経路:** MO01–MO12の規範により共通制約・役割・task情報を一つの版付き入力に構成する。資格済nativeへ新規入力として渡し、履歴を改変せず、同じ安全/品質条件で比較し認定する。

**失敗・拒否:** 必須文脈欠落、権限/モデル上書き、未知のnative設定、誤発火、旧読了、未実測の効果認定、比較条件差を拒否する。予算待ちやprovider拒否はモデル変更で回避しない。

**適用境界:** 完全な仕様は正本、短いpromptはそのタスク投影。API専用機能はnative CLIへ転用しない。内部思考/キャッシュ制御を保証しない。新規LLM/daemon/状態正本は増やさない。

### 操作契約（後続実装）

- `plan_prompt(profile, task, baseline, ledger, catalog) -> PromptPlan`
- `render_task_context(plan, verified_sources) -> TaskPacket`
- `qualify_model_pack(pack, native_observations, evaluation) -> qualification`

**実装対象:** `src/adh/assets/`, `src/adh/context/`, `src/adh/qualification/`, `contracts/model-execution.schema.json`, `profiles/`, `prompts/`, `skill-pack/`, `evaluation/`

**分担WP:** WP00, WP01, WP02, WP03, WP04, WP05, WP06, WP09, WP10, WP14, WP15, WP16, WP17, WP18, WP19, WP20, WP21, WP22, WP24, WP25, WP26, WP28, WP29, WP30, WP31

**必須検証:** V04-06-M01, V17-04-M01, V31-03-M01, V06-05-M01, V06-06-M01, V26-02-M01, V18-06-M01, V25-01-M01, V28-02-M01, V16-02-M01, V22-01-M01, V28-04-M01, V05-01-M01, V15-01-M01, V28-01-M01, V15-03-M01, V25-06-M01, V26-01-M01, V15-02-M01, V15-06-M01, V28-06-M01, V19-01-M01, V21-02-M01, V28-02-M02, V01-01-M01, V06-03-M01, V26-03-M01, V06-03-M02, V21-06-M01, V24-01-M01, V03-06-M01, V28-06-M02, V31-02-M01, V30-04-M01, V30-05-M01, V31-05-M01

**出典:** OPT-S01, OPT-S02, OPT-S03, OPT-S04, OPT-S05, OPT-S06, OPT-S07, OPT-S08

<a id="ic13"></a>

## IC13：型付き文書graph・要求から検査までの正本

**責任者:** DocumentRegistry / Context / Change authority。**主担当:** WP04。**要求:** R01, R02, R03, R04, R05, R07, R08, R09, R10, R11, R12, R14, R15, R17, R18, R20, R22, R24, R27, R29, R30, R31, R33, R34, R35

**データ仕様:** ArtifactNode/Relation、original R、EARS refinement、AC、Oracle/TEST参照、normative closure、CHG impact-set。TaskPacketは適用する必須条件と参照を保持する。

**正常経路:** 10分類を別の直列工程にせず、唯一の原本へtyped edgeを結び、担当taskへ必要な要求/契約/guardだけ投影する。CHG/EVALは開始時から作用する。

**失敗・拒否:** 参照/型/版/要求の欠落、原本と要約の逆転、未実行証拠の捏造、無承認変更は拒否。無関係な編集で全taskを無効化しない。

**適用境界:** 文書graphはsourceとplanの対応であり実装完了の証明でない。Task DAGとは別。graph hashは監査、受入失効は適用closureとpolicyで決める。

### 操作契約（後続実装）

- `validate_document_graph(graph) -> structural_findings`
- `resolve_normative_closure(task, baseline) -> refs_and_digest`
- `assess_change(before, after, scope) -> impact_set_and_regates`

**実装対象:** `src/adh/documents/`, `src/adh/context/`, `src/adh/change/`, `contracts/document-graph.schema.json`

**分担WP:** WP00, WP01, WP02, WP03, WP04, WP05, WP06, WP07, WP08, WP09, WP10, WP11, WP12, WP13, WP14, WP15, WP16, WP17, WP18, WP19, WP20, WP21, WP22, WP23, WP24, WP25, WP26, WP27, WP28, WP29, WP30, WP31

**必須検証:** V02-01-DG01-P, V02-04-DG01-N, V00-02-DG02-P, V19-05-DG02-N, V04-04-DG03-P, V20-05-DG03-N, V04-01-DG04-P, V18-02-DG04-N, V10-01-DG05-P, V10-06-DG05-N, V17-04-DG06-P, V18-06-DG06-N, V08-05-DG07-P, V24-05-DG07-N, V19-01-DG08-P, V19-02-DG08-N, V28-01-DG09-P, V28-06-DG09-N, V31-01-DG10-P, V31-03-DG10-N

**出典:** DG-S01, DG-S02, DG-S03, DG-S04, DG-S05, DG-S06

<a id="ic14"></a>

## IC14：全工程の操作別ガードレール・強制・復旧

**責任者:** Supervisor Policy + API/Runner/OS/Verifier enforcement。**主担当:** WP04。**要求:** R01, R02, R03, R05, R06, R09, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35

**データ仕様:** OperationIntent、GuardDecision、GuardQualification、actor/task/target/attempt/fence、policy/closure/qualification digest、reason、expiry、recovery、実作用証拠。

**正常経路:** 有効な委任/安全policy/要求/task scope/環境能力の共通部分で操作を許可。事前判定と耐久intent後にdispatchし受信側とOSで強制。候補は独立検証を経て受理する。

**失敗・拒否:** 既知違反DENY、必須能力/guard故障HOLD、侵害疑義QUARANTINE。無関係なtaskは進める。判断の欠損をALLOWへ変換しない。

**適用境界:** promptやHook存在を強制防御にしない。既存サービス内モジュールとして実装し別daemonを24個作らない。未知攻撃の完全防御を主張しない。

### 操作契約（後続実装）

- `evaluate_guard(intent, current_policy, qualification) -> decision`
- `enforce_operation(decision, current_binding) -> execute_or_refuse`
- `recover_guarded_task(record, authorized_change) -> requalified_state`

**実装対象:** `src/adh/policy/`, `src/adh/api/`, `src/adh/runner/`, `src/adh/verifier/`, `contracts/guardrails.schema.json`

**分担WP:** WP00, WP01, WP02, WP03, WP04, WP05, WP06, WP07, WP08, WP09, WP10, WP11, WP12, WP13, WP14, WP15, WP16, WP17, WP18, WP19, WP20, WP21, WP22, WP23, WP24, WP25, WP26, WP27, WP28, WP29, WP30, WP31

**必須検証:** V18-05-GR01-P, V29-01-GR01-N, V29-01-GR01-F, V22-06-GR01-R, V08-01-GR02-P, V08-04-GR02-N, V08-02-GR02-F, V08-05-GR02-R, V12-01-GR03-P, V17-03-GR03-N, V12-03-GR03-F, V08-03-GR03-R, V26-01-GR04-P, V26-03-GR04-N, V01-02-GR04-F, V15-06-GR04-R, V06-02-GR05-P, V06-05-GR05-N, V26-03-GR05-F, V30-04-GR05-R, V09-01-GR06-P, V09-03-GR06-N, V14-03-GR06-F, V24-06-GR06-R, V13-03-GR07-P, V13-02-GR07-N, V20-02-GR07-F, V26-04-GR07-R, V13-04-GR08-P, V13-04-GR08-N, V26-04-GR08-F, V14-04-GR08-R, V14-04-GR09-P, V29-01-GR09-N, V26-03-GR09-F, V14-06-GR09-R, V24-01-GR10-P, V10-02-GR10-N, V10-04-GR10-F, V10-06-GR10-R, V17-02-GR11-P, V23-03-GR11-N, V07-02-GR11-F, V17-05-GR11-R, V14-01-GR12-P, V29-04-GR12-N, V11-04-GR12-F, V22-04-GR12-R, V22-01-GR13-P, V22-03-GR13-N, V11-02-GR13-F, V22-06-GR13-R, V20-04-GR14-P, V20-03-GR14-N, V20-06-GR14-F, V20-01-GR14-R, V21-01-GR15-P, V21-05-GR15-N, V21-06-GR15-F, V21-02-GR15-R, V03-06-GR16-P, V20-05-GR16-N, V03-03-GR16-F, V08-04-GR16-R, V16-01-GR17-P, V16-04-GR17-N, V15-03-GR17-F, V16-05-GR17-R, V24-01-GR18-P, V24-02-GR18-N, V24-03-GR18-F, V24-06-GR18-R, V08-05-GR19-P, V08-03-GR19-N, V24-05-GR19-F, V30-04-GR19-R, V25-01-GR20-P, V25-02-GR20-N, V25-04-GR20-F, V28-06-GR20-R, V23-01-GR21-P, V23-05-GR21-N, V23-02-GR21-F, V23-04-GR21-R, V30-05-GR22-P, V09-06-GR22-N, V25-04-GR22-F, V31-05-GR22-R, V14-05-GR23-P, V29-05-GR23-N, V14-06-GR23-F, V13-05-GR23-R, V28-04-GR24-P, V26-03-GR24-N, V29-03-GR24-F, V22-06-GR24-R

**出典:** GR-S01, GR-S02, GR-S03, GR-S04, GR-S05, GR-S06, GR-S07, GR-S08, GR-S09, GR-S10

<a id="ic15"></a>

## IC15：配布・設定生成・全資産・ReleaseSetの一体管理

**責任者:** Assets/Qualification + dotfiles release owner。**主担当:** WP06。**要求:** R13, R14, R15, R27, R33, R34, R35

**データ仕様:** CompositionIntent, AssetBinding, ReleaseSet, RoleBinding, native effective-config証拠。dotfiles commit・ADH commit・選択payload・profile/policy/quality/knowledge lockを同じrelease_set_idへ固定。

**正常経路:** モデルの編集正本はdotfiles home/dot_agents/agent-config.yamlのadh profile。V4要求は一致を検査する制約であり別のruntime設定源ではない。隔離profileへ生成→実値照合→資格確認→段階公開。任意UIと必須機能を区別し利用者の既存用途を保持する。

**失敗・拒否:** 片側設定drift、古いE2E express、未管理selected plugin、payload不足、二repo不一致は新admission停止。既存runを無断更新せず旧lockを保全。未完了配布を成功manifestへ記録しない。

**適用境界:** one logical releaseはone code repoを意味しない。dotfilesは配布と薄いwrapper、ADHは一つの実装。二repoを原子的Git transactionと偽らず段階配置/互換表/戻しで管理。

### 操作契約（後続実装）

- `resolve_composition(project_policy, source_manifest) -> CompositionIntent`
- `qualify_release(release_set, observed_evidence) -> qualification`
- `activate_release(qualified_ref, expected_version) -> activation_record`

**実装対象:** `dotfiles:home/dot_agents/agent-config.yaml`, `dotfiles:scripts/generate-agent-configs.py`, `adh:src/adh/assets/`, `adh:src/adh/qualification/`

**分担WP:** WP00, WP01, WP02, WP04, WP05, WP06, WP15, WP16, WP17, WP26, WP27, WP30, WP31

**必須検証:** V06-02-U4-01, V26-01-U4-02, V15-04-U4-03, V06-01-U4-04, V26-02-U4-05, V17-05-U4-06, V30-04-U4-07, V06-05-U4-08, V17-01-U4-38, V24-05-U4-40, V26-04-U4-42, V30-06-U4-45, V31-02-U4-46

**出典:** V4-S01, V4-S02, V4-S03

<a id="ic16"></a>

## IC16：正本・コード構造・記憶・Semantica参照の統合

**責任者:** DocumentRegistry / Context / isolated KnowledgeAdapter。**主担当:** WP18。**要求:** R01, R03, R04, R05, R06, R12, R18, R20, R24, R29, R30, R31, R34, R35

**データ仕様:** KnowledgeSnapshot/Query/Response: project, trust_domain, baseline, source snapshot, ACL digest, schema/adapter/upstream revision, source refs, relation_kind/status, bounded result。

**正常経路:** 明示ID/edgeは決定的に取込。UAはコード構造、CompactionDBは記録、Semanticaは再構成可能な参照graph。権限・有効版で先にsubgraphを絞り、原本locator/hash/range付きで必要文脈を返す。規範closureは正本から別に必ず取得。

**失敗・拒否:** 偽source/不正日付/越境/任意保存先は拒否。候補/古い索引は区別。破損時は原本に戻り不足taskのみHOLD。confidenceやPolicyEngine出力をgrant/acceptanceにしない。

**適用境界:** 専用uv workerに本人Auth/管理DBを与えない。MCP/外部LLM/embedding/外部graph DBを必須追加しない。graphはキャッシュであって第二の業務正本ではない。推定因果を証明としない。

### 操作契約（後続実装）

- `ingest(manifest, grant_ref) -> snapshot_ref`
- `query(binding, intent, bounds) -> provenance_results`
- `context(binding, required_closure, bounds) -> context_envelope`
- `impact(binding, changed_ids) -> explicit_and_inferred_candidates`
- `verify(snapshot_ref) -> integrity_result`
- `rebuild(approved_manifest) -> new_snapshot_ref`

**実装対象:** `adh:integrations/semantica/`, `adh:src/adh/knowledge/contracts/`, `adh:src/adh/context/`, `dotfiles:home/dot_local/bin/common/executable_agent-context`

**分担WP:** WP01, WP02, WP04, WP06, WP09, WP12, WP13, WP17, WP18, WP19, WP22, WP25, WP26, WP28, WP29, WP30, WP31

**必須検証:** V18-01-U4-09, V26-04-U4-10, V18-04-U4-11, V09-05-U4-12, V22-06-U4-13, V25-01-U4-14, V18-03-U4-15, V13-03-U4-16, V25-02-U4-17, V18-06-U4-18, V24-05-U4-19, V18-02-U4-20, V26-02-U4-21, V26-02-U4-35, V28-01-U4-39, V22-04-U4-41

**出典:** V4-S04, V4-S05, V4-S06

<a id="ic17"></a>

## IC17：prek・Oxc・既存検査の単一品質契約

**責任者:** QualityPlanRegistry / Runner / Verifier。**主担当:** WP14。**要求:** R06, R11, R14, R15, R16, R17, R19, R20, R22, R24, R26, R27, R30, R32, R33, R34, R35

**データ仕様:** QualityPlan/Invocation/Result: project, rule_inventory_digest, fixed toolchain, explicit config, mode, stage, source_basis, targets, input tree digest, expected checks, expected mutation=false for check, raw result refs。

**正常経路:** 同じinventoryからedit差分/commit index snapshot/独立candidate/統合/最終RC用計画を選択。prekは信頼済み非破壊checkの入口、OxcはJS/対応形式担当、Ruff/Pyright/Shellと既存回帰を保持。fixは所有writerの明示操作として分離。

**失敗・拒否:** 空対象の全体整形、未信頼config/未固定自動取得、必須checker欠損、skip/zeroを拒否。formatter変更後はcandidate/graph/receiptを失効。元indexを触らずprivate snapshotを検査。

**適用境界:** prekはsandboxでも最終認可でもない。重いgraph/LLMをcommitに入れない。CIはcandidateの自己緩和した設定でなく保護oracleを使用。TS型検査を互換未検証で削除しない。

### 操作契約（後続実装）

- `plan_quality(stage, binding, trusted_profile) -> QualityPlan`
- `check(plan, read_only_snapshot) -> QualityResult`
- `fix(explicit_grant, owned_paths, profile) -> ChangeProposal`

**実装対象:** `adh:src/adh/quality/`, `adh:quality/`, `dotfiles:home/dot_agents/quality/`, `dotfiles:home/dot_claude/hooks/executable_format-edited-files.py`

**分担WP:** WP03, WP04, WP06, WP09, WP12, WP14, WP20, WP21, WP24, WP26, WP28, WP29, WP30, WP31

**必須検証:** V03-01-U4-22, V06-04-U4-23, V14-04-U4-24, V06-03-U4-25, V14-06-U4-26, V14-06-U4-27, V14-05-U4-28, V03-02-U4-29, V20-05-U4-30, V30-02-U4-31, V24-03-U4-32, V26-03-U4-33, V22-02-U4-34, V29-05-U4-43

**出典:** V4-S07, V4-S08, V4-S09, V4-S10, V4-S17, V4-S18

<a id="ic18"></a>

## IC18：学習・変更・合否・統合復旧の共通ライフサイクル

**責任者:** Supervisor / ChangeAuthority / Evidence / learning owner。**主担当:** WP25。**要求:** R01, R02, R11, R12, R18, R21, R22, R24, R25, R26, R27, R28, R29, R30, R31, R33, R34, R35

**データ仕様:** LearningCandidate/PromotionRecord, ChangeImpact, ReleaseAcceptance: original evidence, applicability, proposal, independent checks, approval, changed digests, affected tasks, supersedes。

**正常経路:** RESULT/worklog done/pane idleは観測。A3/A4の同一candidate証拠で唯一のauthorityが合否確定。学習は候補から独立評価・承認後に次releaseへ反映。変更ごとに意味/対象closureへ絞って失効し、安全な局所復旧を許す。

**失敗・拒否:** 未承認昇格、自己受入、古いreceipt、効果不明の再送、policy TOCTOUを拒否。禁止作用のあるtaskだけを止め独立taskを進める。旧writer静止前は再割当不可。

**適用境界:** モデル自体の安全拒否を回避する設計ではない。システム誤検知は透明なレビュー・権限内再資格で修正。開発bootstrapと完成製品の二重authorityを作らない。

### 操作契約（後続実装）

- `propose_learning(evidence, scope) -> candidate`
- `evaluate_candidate(candidate, fixed_eval) -> evaluation`
- `promote_candidate(candidate, approval, expected_baseline) -> new_release_requirement`
- `accept_release(release_set, evidence_inventory) -> decision`

**実装対象:** `adh:src/adh/learning/`, `adh:src/adh/recovery/`, `adh:src/adh/integration/`, `adh:src/adh/domain/acceptance/`

**分担WP:** WP00, WP04, WP05, WP08, WP10, WP11, WP17, WP21, WP22, WP23, WP24, WP25, WP26, WP27, WP28, WP29, WP30, WP31

**必須検証:** V25-02-U4-36, V30-04-U4-37, V29-01-U4-44, V23-03-U4-47, V31-05-U4-48

**出典:** V4-S02, V4-S03, V4-S15
