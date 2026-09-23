<!-- 自動生成：python tools/kit_lint.py trace。手で編集しない（check が差分を不合格にする）。 -->
# 追跡表：要件→ルール→シナリオ→設計判断→専用検証

ルール・シナリオ・テスト条件は要件を**具体化**（specifies）するだけで、合格を意味しない。「合格した実行」の列だけが実行証跡に基づく。ただし、その要件を確かめるテストが1件以上合格したことを示すだけで、要件の全体が検証済みであることは意味しない。

## 機能要件

| 要件 | 優先度 | ルール | シナリオ | 設計判断 | 専用検証 | テスト条件 | 合格した実行 |
|---|---|---|---|---|---|---|---|
| [FR-001](prd/PRD_SAMPLE.md#FR-001) | Must | RULE-003, RULE-012 | SCN-008, SCN-010, SCN-024 | — | NVT-002 | CT-003, CT-006 | CT |
| [FR-002](prd/PRD_SAMPLE.md#FR-002) | Must | RULE-003 | SCN-007, SCN-009 | — | — | CT-003, E2E-004, UT-013 | CT, UT |
| [FR-003](prd/PRD_SAMPLE.md#FR-003) | Must | RULE-001 | SCN-001, SCN-003, SCN-004 | — | — | E2E-001, PT-003, UAT-001, UT-001, UT-002, UT-003, UT-004, UT-005, UT-006 | UT |
| [FR-004](prd/PRD_SAMPLE.md#FR-004) | Must | RULE-001 | SCN-002, SCN-003, SCN-005 | — | — | PT-003, UAT-001, UAT-005, UT-002, UT-003, UT-007, UT-008, UT-009, UT-010 | UT |
| [FR-005](prd/PRD_SAMPLE.md#FR-005) | Must | RULE-002 | SCN-006 | — | — | — | — |
| [FR-006](prd/PRD_SAMPLE.md#FR-006) | Must | RULE-004 | SCN-011 | — | — | E2E-001, UAT-003 | — |
| [FR-007](prd/PRD_SAMPLE.md#FR-007) | Must | RULE-005 | SCN-012 | — | — | PT-001, UAT-003 | — |
| [FR-008](prd/PRD_SAMPLE.md#FR-008) | Must | RULE-006 | SCN-013, SCN-014 | ADR-0001 | — | CT-004 | CT |
| [FR-009](prd/PRD_SAMPLE.md#FR-009) | Must | RULE-007 | SCN-015 | — | — | — | — |
| [FR-010](prd/PRD_SAMPLE.md#FR-010) | Must | RULE-007 | SCN-016 | ADR-0001 | — | E2E-003, UAT-006 | — |
| [FR-011](prd/PRD_SAMPLE.md#FR-011) | Must | RULE-008 | SCN-017, SCN-018 | — | — | E2E-001, UT-011, UT-015 | CT, UT |
| [FR-012](prd/PRD_SAMPLE.md#FR-012) | Must | RULE-009 | SCN-019 | — | — | UAT-002, UT-013 | CT, UT |
| [FR-013](prd/PRD_SAMPLE.md#FR-013) | Must | RULE-010 | SCN-020, SCN-021 | — | — | PT-002, UAT-002, UT-013 | CT, UT |
| [FR-014](prd/PRD_SAMPLE.md#FR-014) | Must | RULE-011 | SCN-022 | ADR-0002 | NVT-010 | CT-001, CT-005, PT-004, UAT-004 | CT |
| [FR-015](prd/PRD_SAMPLE.md#FR-015) | Must | RULE-012 | SCN-023, SCN-024, SCN-025 | ADR-0002 | — | CT-002, PT-002 | CT |
| [FR-016](prd/PRD_SAMPLE.md#FR-016) | Must | RULE-013 | SCN-026, SCN-027 | ADR-0002 | — | CT-002, E2E-001 | CT |
| [FR-017](prd/PRD_SAMPLE.md#FR-017) | Should | RULE-014 | SCN-028 | ADR-0002 | — | — | — |
| [FR-018](prd/PRD_SAMPLE.md#FR-018) | Must | RULE-015 | SCN-029 | — | — | UT-011 | UT |
| [FR-019](prd/PRD_SAMPLE.md#FR-019) | Must | RULE-016 | SCN-030 | — | — | E2E-002, UAT-007, UT-011 | UT |
| [FR-020](prd/PRD_SAMPLE.md#FR-020) | Must | RULE-017 | SCN-031 | — | — | UT-011, UT-012, UT-014 | UT |
| [FR-021](prd/PRD_SAMPLE.md#FR-021) | Must | RULE-018 | SCN-032, SCN-033 | — | NVT-009 | PT-004, UT-016 | UT |
| [FR-022](prd/PRD_SAMPLE.md#FR-022) | Must | RULE-019 | SCN-034, SCN-035 | — | — | UT-017, UT-018 | UT |
| [FR-023](prd/PRD_SAMPLE.md#FR-023) | Could | RULE-019 | SCN-036 | — | — | UT-017 | UT |
| [FR-024](prd/PRD_SAMPLE.md#FR-024) | Must | RULE-020 | SCN-037 | ADR-0001 | — | E2E-003, UAT-006 | — |
| [FR-025](prd/PRD_SAMPLE.md#FR-025) | Should | RULE-021 | SCN-038 | — | — | — | — |
| [FR-026](prd/PRD_SAMPLE.md#FR-026) | Must | — | — | — | NVT-011 | — | — |
| [FR-027](prd/PRD_SAMPLE.md#FR-027) | Must | RULE-022 | SCN-040 | — | — | E2E-002, PT-001 | — |
| [FR-028](prd/PRD_SAMPLE.md#FR-028) | Must | RULE-023 | SCN-041, SCN-042 | — | — | UT-013 | CT, UT |

## 非機能要件

| 要件 | 品質特性 | 専用検証 | 割当先の文書 | テスト条件 | 設計判断 |
|---|---|---|---|---|---|
| [NFR-001](prd/PRD_SAMPLE.md#NFR-001) | 性能効率性 | NVT-001 | st/ST_SAMPLE.md | — | — |
| [NFR-002](prd/PRD_SAMPLE.md#NFR-002) | セキュリティ（機密性・完全性） | NVT-002 | ct/CT_SAMPLE.md | CT-003, CT-006, E2E-004 | — |
| [NFR-003](prd/PRD_SAMPLE.md#NFR-003) | 信頼性（可用性） | NVT-003 | st/ST_SAMPLE.md | — | — |
| [NFR-004](prd/PRD_SAMPLE.md#NFR-004) | 信頼性（回復性） | NVT-004 | st/ST_SAMPLE.md | — | — |
| [NFR-005](prd/PRD_SAMPLE.md#NFR-005) | 性能効率性（時間効率性） | NVT-005 | st/ST_SAMPLE.md | — | ADR-0002 |
| [NFR-006](prd/PRD_SAMPLE.md#NFR-006) | インタラクション能力 | NVT-006 | st/ST_SAMPLE.md | E2E-005, UAT-005 | — |
| [NFR-007](prd/PRD_SAMPLE.md#NFR-007) | 機能適合性（AIの正確性） | NVT-007 | st/ST_SAMPLE.md | — | — |
| [NFR-008](prd/PRD_SAMPLE.md#NFR-008) | セキュリティ（責任追跡性） | NVT-008 | st/ST_SAMPLE.md | — | — |
| [NFR-009](prd/PRD_SAMPLE.md#NFR-009) | セキュリティ（機密性） | NVT-009 | st/ST_SAMPLE.md | — | — |

## ルール

| ルール | 業務ルール | シナリオ | 要件 |
|---|---|---|---|
| RULE-001 | 入力規則を満たす下書きだけが提出できる | SCN-001, SCN-002, SCN-003, SCN-004, SCN-005 | FR-003, FR-004 |
| RULE-002 | 提出済みの内容は直接編集できない | SCN-006 | FR-005 |
| RULE-003 | 権限のない相手には申請の内容も存在も明かさない | SCN-007, SCN-008, SCN-009, SCN-010 | FR-001, FR-002 |
| RULE-004 | 参考意見は出典付きの参考情報として示す | SCN-011 | FR-006 |
| RULE-005 | 出典で裏付けられない主張は未確認と示す | SCN-012 | FR-007 |
| RULE-006 | AIは申請の状態を変えられない | SCN-013, SCN-014 | FR-008 |
| RULE-007 | AIが使えなくても人の審査は続けられる | SCN-015, SCN-016 | FR-009, FR-010 |
| RULE-008 | 有効な審査者は他人の提出済み申請を理由付きで決裁できる | SCN-017, SCN-018 | FR-011 |
| RULE-009 | 審査者は自分が提出した申請を決裁できない | SCN-019 | FR-012 |
| RULE-010 | 古い版に対する決裁は成立しない | SCN-020, SCN-021 | FR-013 |
| RULE-011 | 決裁と監査記録は必ず対で成立する | SCN-022 | FR-014 |
| RULE-012 | 同じ決裁要求の再送で決裁は重複しない | SCN-023, SCN-024, SCN-025 | FR-001, FR-015 |
| RULE-013 | 確定した決裁は申請者に1件だけ通知される | SCN-026, SCN-027 | FR-016 |
| RULE-014 | 届けられない通知は運用者が把握できる | SCN-028 | FR-017 |
| RULE-015 | 申請者は終端前の自分の申請を取り消せる | SCN-029 | FR-018 |
| RULE-016 | 差戻された申請の修正は新しい内容版になる | SCN-030 | FR-019 |
| RULE-017 | 提出済みでない申請は決裁できない | SCN-031 | FR-020 |
| RULE-018 | 終端から90日で本文は削除対象になる | SCN-032, SCN-033 | FR-021 |
| RULE-019 | 放置された申請は自動で取り消される | SCN-034, SCN-035, SCN-036 | FR-022, FR-023 |
| RULE-020 | 停止中は新しい参考意見を受け付けない | SCN-037 | FR-024 |
| RULE-021 | 停止前に始まった結果は停止後に採用しない | SCN-038 | FR-025 |
| RULE-022 | 参考意見は作成時の内容版にだけ結び付く | SCN-040 | FR-027 |
| RULE-023 | 複数の拒否条件に当たる要求には決まった優先順位の理由だけを返す | SCN-041, SCN-042 | FR-028 |

## テスト項目

| ID | 水準 | 由来 |
|---|---|---|
| UT-001 | UT | FR-003 |
| UT-002 | UT | FR-004, RULE-001 |
| UT-003 | UT | FR-003, FR-004 |
| UT-004 | UT | FR-003, SCN-004 |
| UT-005 | UT | FR-003 |
| UT-006 | UT | FR-003 |
| UT-007 | UT | FR-004, SCN-005 |
| UT-008 | UT | FR-004 |
| UT-009 | UT | FR-004 |
| UT-010 | UT | FR-004 |
| UT-011 | UT | FR-011, FR-018, FR-019, FR-020 |
| UT-012 | UT | FR-020, RULE-017 |
| UT-013 | UT | FR-002, FR-012, FR-013, FR-028, RULE-023 |
| UT-014 | UT | FR-020, RULE-017 |
| UT-015 | UT | FR-011, SCN-018 |
| UT-016 | UT | FR-021, RULE-018 |
| UT-017 | UT | FR-022, FR-023, RULE-019 |
| UT-018 | UT | FR-022 |
| CT-001 | CT | ADR-0002, FR-014, NVT-010 |
| CT-002 | CT | ADR-0002, FR-015, FR-016 |
| CT-003 | CT | FR-001, FR-002, NVT-002 |
| CT-004 | CT | ADR-0001, FR-008 |
| CT-005 | CT | ADR-0002, FR-014 |
| CT-006 | CT | FR-001, NVT-002 |
| E2E-001 | ST | FR-003, FR-006, FR-011, FR-016 |
| E2E-002 | ST | FR-019, FR-027 |
| E2E-003 | ST | ADR-0001, FR-010, FR-024 |
| E2E-004 | ST | FR-002, NFR-002 |
| E2E-005 | ST | NFR-006 |
| UAT-001 | UAT | FR-003, FR-004, GOAL-001 |
| UAT-002 | UAT | FR-012, FR-013, GOAL-001, GOAL-002, KPI-001 |
| UAT-003 | UAT | FR-006, FR-007, GOAL-002, GRD-002 |
| UAT-004 | UAT | FR-014, GOAL-002, GRD-001 |
| UAT-005 | UAT | FR-004, NFR-006 |
| UAT-006 | UAT | FR-010, FR-024, GRD-002 |
| UAT-007 | UAT | FR-019, GOAL-002 |
| PT-001 | UAT | FR-007, FR-027, GRD-002 |
| PT-002 | UAT | FR-013, FR-015 |
| PT-003 | UAT | FR-003, FR-004 |
| PT-004 | UAT | FR-014, FR-021, GRD-001 |
