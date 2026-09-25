# 5. 検証条件・検証内容・証拠基準

## 検証階層

| 種別 | 判定すること | 代用できないもの |
|---|---|---|
| DOCUMENT | 要求/仕様/設計/手順の整合、意味レビュー | 実動作 |
| STATIC | format/lint/type/schema/lock/scan | 実通信・実OS |
| CONTRACT | 入出力/状態/role/署名の正負ケース | 実adapterと製品の接続 |
| LOCAL | 実Git/SQLite/別process/私設serverでの動作 | Auth付きLLMとVM境界 |
| NATIVE_KEYLESS | 公式binary起動、help/schema、非課金handshake | 本人アカウントのmodel利用・生成 |
| NATIVE_AUTH | 本人Authの実model/effort、session、Hook、Skills | OS権限隔離の証明 |
| VM | 実VM・OSユーザー・process・net・key境界 | 全工程の推論品質 |
| AI_E2E | 指定modelが実際に調査/実装/修正/レビューして工程を遂行 | 決定的なfixture書換えscript |
| RELIABILITY/PERFORMANCE/OPS | 障害・負荷・導入・更新・復旧 | 机上試算 |
| RELEASE | 同一RCの全必須検査・成果物一致 | 部分suiteの寄せ集め |

本計画は32WP×6項目=192の**論理的な検証項目**を定める。各項目にfixture、手順、oracle、証拠、階層がある。実装時はrole×API、状態遷移、platformなどをsubcaseへ展開し実収集件数をinventoryに固定する。192という数をpytestの実行件数と同一視しない。

## Statusを固定する

PLANNEDは作業、NOT_RUNは検証の初期値。RUNNING、PASS、FAIL、BLOCKED_ENV、BLOCKED_AUTH、BLOCKED_DECISION、UNKNOWN、SKIP、XFAIL、N/Aを区別する。必須対象でPASS以外は全体受入を止める。N/Aは試験前に適用範囲から承認済みで除外された非必須platformなどに限る。失敗した後にN/Aへ変更しない。

期待した拒否が起きるnegative testはPASS。その対象製品が安全上無欠陥という意味ではない。攻撃例が実操作を壊さないよう偽secret・隔離target・private endpointを使う。

## 実行ごとの証拠

command IDと版、argv（shell文字列のみで代用しない）、cwd、開始/終了、exit/signal/timeout、収集/実行/失敗/skip/xfail件数、targetの6hash、native model/effort/session、environment、actor/role、stdout/stderr/resultのartifact digest、前提qualification、再試行番号を残す。

モデルが書いた『実行済み』をcollector出力に変換しない。artifactを実際に読みhashを再計算する。秘密を含むrawログは制限領域へ隔離し、ユーザー向けbundleはredacted版と変換記録を保存する。秘密除去を理由に失敗の種類や終了codeを隠さない。

## 独立性

実装A2、機械検証A4、意味レビューA3を分ける。A3が元candidateを編集したら独立review失格。A4のtest execution processはAuthも署名鍵も保持しない。signerは観測結果と固定inventoryから署名する。別鍵で署名していても同じ無制限processであれば権限分離の合格にはしない。

## 品質閾値（本計画の受入基準）

- R01–R35の実装/実検証へのtraceability 100%。
- 必須case PASS100%、SKIP/NOT_RUN/BLOCKED/UNKNOWN/XFAIL=0。
- Ruff format差分0、Ruff未解決違反0、Pyright strict error0。既存由来の警告も適用範囲と理由を明記する。
- authored production Python全体でline coverage≥95%、branch coverage≥90%。authority/scheduler/lease/acceptance/canonicalization/effect状態遷移はbranch100%。実行不能行の除外は事前定義のgenerated codeに限り、後から分母を減らさない。
- すべての許可/非許可状態edge、認可role/operation組合せ、偽署名/replay/旧fenceをnegative controlにする。安全重要invariantの手動mutation（比較除去等）は全て失敗を検出する。
- 未解決の受入阻害finding=0。Critical/Highだけでなく、MUST違反はseverityが低くても阻害。低severityの助言は承認済み残余リスクとして記録可。
- secrets検出0。dependency vulnerabilityはCritical/High0を原則とし、実行影響のないfalse positiveも理由・根拠・承認記録が必要。scan tool/DB日時を記録し未知脆弱性ゼロとは言わない。
- AI E2Eは6scenarioを各3回、計18run。全runを保存。成功だけ選別しない。失敗後の修正版RCで再試験する。

この閾値は達成済実績ではない。計画で事前固定する基準であり、下げるには利用者承認を含むbaseline改訂が必要。

## NFRの条件

lease=120秒、heartbeat=30秒、termination grace=10秒は旧設計を継承。管理VMの性能試験は4vCPU/8GiB以上・local diskを記録し、32concurrent client/1000task/10分を初期負荷条件とする。Supervisor latencyはLLM response時間を除外して記録する。初期目標はwarm crash復旧処理の開始120秒以内、process crash後のcommitted event RPO=0。VM起動待ちや外部サービス待ち、電断耐久は別測定であり、この数値へ混ぜない。

writer停止が確認できなければdeadline超過時も新writerを開始しない。予算と資源の絶対値は操作者が委任するRunContextに記録し、未設定・不明を0や無制限へ変換しない。

## 再試験範囲

局所修正は該当case→関連interface/依存→WP suite→統合回帰の順。schema/policy/asset/CLI/environment/suite/署名/認可の変更はqualification失効として影響native/VM/E2Eを再試験。最終WP31では必ず同一RCで全必須suiteを実行する。最終実行後のコード・契約・設定変更は新RCを発行して再検証する。

## 論理caseと統合subcaseの数え方

192の論理case IDを保存し、その内側に196の必須subcaseを記入済みである。旧追補の22グループはprovenanceの別名に退役させ、別のPASS件数として数えない。80件は追加80論理caseではない。親caseは元の合格条件AND全必須subcaseの指定階層PASSで成立する。

一つの親caseに複数tierのsubcaseがある場合、tierごとに証拠を分ける。DOCUMENT/CONTRACTの成功からNATIVE_AUTH/VM/AI_E2E成功へ昇格しない。実装時の細分化は許すが、記載済みsubcaseの削除・合格基準緩和・skipは不可。

IC01の能力虚偽、IC02のhost/VM混在、IC04の未来投影、IC05のcommit前dispatch、IC06の停止解除、IC07のack前crash、IC08のtimeout+exit0、IC09の中央FAIL省略、IC10の両端drift、IC11のbuilt破損/mutationは必須反例とする。


## モデル別検証の内包

192親caseには従来44とモデル最適化36の計196subcaseを内包する。全必須subcaseを所定tierで満たして親を合格にする。48のrouting事例、封印する未見群、4armの72runは各subcaseの内部fixture/反復であり親case数へ加算しない。詳細は[evaluation規約](../evaluation/EXPERIMENT_PROTOCOL.md)。

stage別の開発検査は影響範囲で選ぶが、WP候補・独立・統合・最終RCの固定inventoryを減らさない。効率改善の比較でも、失敗・SKIP・未実行・scope違反を成功として扱わない。

## DG/GRの追加サブケース
192親の基本条件と既存80子を保持し、文書20子・guard96子を内包する。全244子はNOT_RUNから開始。GRごとに正常許可・禁止・故障/迂回・復旧の4観点、DGごとに正負2観点を個別に指定tierで実行する。DOCUMENTは文書の意味的独立レビューを含み、Schema/リンク機械検査だけでは満たさない。SECURITYは危険な本番資産でなく合成secret/制御宛先を用いる。

各GR結果は実actor/版/モード/強制点/decisionとworld effectを残す。Hook故障を検出できたというだけでなく、故障中にも禁止作用が実行されていないことを試す。正当なケースの不必要な拒否も不合格。


## V4検証集合の数え方

親192件の各pass_condition、既存内包196件のpass_conditionを保持する。V4の48件を同じ親へ内包し、内包は計244件。親と子、移管元のSI36/DI24、72runの反復は異なる粒度であり、加算して実証件数を増やさない。旧追加計画の全検査は[移管表](../registers/legacy_addon_mapping.json)で対応する。required componentやcaseをoptionalに変更して通さない。

親PASSには基本条件と全内包子の所定tier完了が必要。wrapper exit0、Semantica query成功、prek summaryのPASSだけでは全品質合格にしない。変更したdotfilesとADH双方の既存回帰も必須。
