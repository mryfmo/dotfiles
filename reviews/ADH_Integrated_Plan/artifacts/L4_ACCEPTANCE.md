# L4 AC／BDD — 受け入れ仕様

[シナリオ台帳](../registers/acceptance_scenarios.json)から生成。各シナリオは代表的な期待動作を規定し、全入力や障害条件を網羅したという意味ではない。Thenは期待、oracleは実際の比較器、TESTはその実装、Evidenceは実行証拠。後続WP20/28はstep定義と独立oracleを実装し、従来の192検査と全subcaseを保持する。構文が通っても製品PASSにはしない。[DG-S03](../sources/DOCUMENT_GUARDRAIL_SOURCES.md)

<a id="ac-r01"></a>
## AC-R01

要求：R01, REQ-R01。oracle参照：V00-02, V08-02, V08-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R01
  Given 入力資料が登録または改訂された状態
  When Baseline Authorityに該当操作を要求する
  Then 登録後のsource digestと要求台帳が原本と一致する
```

<a id="ac-r02"></a>
## AC-R02

要求：R02, REQ-R02。oracle参照：V01-06, V08-01, V19-06, V23-05。状態：NOT_RUN。

```gherkin
Scenario: AC-R02
  Given task実行が要求された状態
  When Supervisorに該当操作を要求する
  Then 委任内実行とreserved decision待ちが区別される
```

<a id="ac-r03"></a>
## AC-R03

要求：R03, REQ-R03。oracle参照：V18-01, V18-02。状態：NOT_RUN。

```gherkin
Scenario: AC-R03
  Given 設計判断に外部資料の主張を採用する状態
  When Researchに該当操作を要求する
  Then claimから取得可能な原本と版へ戻れる
```

<a id="ac-r04"></a>
## AC-R04

要求：R04, REQ-R04。oracle参照：V02-04, V18-06。状態：NOT_RUN。

```gherkin
Scenario: AC-R04
  Given 重要な設計論点を調査する状態
  When Researchに該当操作を要求する
  Then 独立レビューが論点の欠落と根拠の適合を確認する
```

<a id="ac-r05"></a>
## AC-R05

要求：R05, REQ-R05。oracle参照：V18-02, V18-03, V19-02。状態：NOT_RUN。

```gherkin
Scenario: AC-R05
  Given 重要な主張に矛盾または未検証が残っている間
  When Design Gateに該当操作を要求する
  Then 未解決IDが保持される。文書の長さを完了根拠にしない
```

<a id="ac-r06"></a>
## AC-R06

要求：R06, REQ-R06。oracle参照：V09-01, V09-02, V18-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R06
  Given 作業リポジトリを解析する状態
  When SnapshotServiceに該当操作を要求する
  Then dirty内容の変化でfingerprintが変わりmainへすり替わらない
```

<a id="ac-r07"></a>
## AC-R07

要求：R07, REQ-R07。oracle参照：V19-01, V19-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R07
  Given 未確定の実現方式を選ぶ状態
  When Architectに該当操作を要求する
  Then 候補間比較と変更され得る判断条件を独立確認できる
```

<a id="ac-r08"></a>
## AC-R08

要求：R08, REQ-R08。oracle参照：V02-03, V19-02。状態：NOT_RUN。

```gherkin
Scenario: AC-R08
  Given 採用に重要な仮説を検証する状態
  When Experimentに該当操作を要求する
  Then 失敗と未実行を成功と扱わない
```

<a id="ac-r09"></a>
## AC-R09

要求：R09, REQ-R09。oracle参照：V02-02, V19-04, V21-02。状態：NOT_RUN。

```gherkin
Scenario: AC-R09
  Given 解決策の仕様を確定する状態
  When Design Gateに該当操作を要求する
  Then 要求に対する仕様項目と検査参照が欠けない
```

<a id="ac-r10"></a>
## AC-R10

要求：R10, REQ-R10。oracle参照：V02-04, V19-01, V19-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R10
  Given アーキテクチャ上の決定を記録する状態
  When Architectに該当操作を要求する
  Then 重要な決定に出典と結果を逆引きできる
```

<a id="ac-r11"></a>
## AC-R11

要求：R11, REQ-R11。oracle参照：V00-05, V08-02, V08-03, V08-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R11
  Given SolutionBaselineが確定している間
  When Authorityに該当操作を要求する
  Then 正規CR以外ではdigestが不変
```

<a id="ac-r12"></a>
## AC-R12

要求：R12, REQ-R12。oracle参照：V02-04, V19-04, V19-05。状態：NOT_RUN。

```gherkin
Scenario: AC-R12
  Given 実装計画を受け入れる状態
  When Plannerに該当操作を要求する
  Then 未対応・矛盾を解消するまでplan受入しない
```

<a id="ac-r13"></a>
## AC-R13

要求：R13, REQ-R13。oracle参照：V01-01, V15-01, V15-06, V16-02, V26-01。状態：NOT_RUN。

```gherkin
Scenario: AC-R13
  Given 公式Agentを起動または再開する状態
  When NativeAdapterに該当操作を要求する
  Then Auth bytesをSupervisor/別providerに複製しない
```

<a id="ac-r14"></a>
## AC-R14

要求：R14, REQ-R14。oracle参照：V06-02, V06-06, V15-04, V26-02。状態：NOT_RUN。

```gherkin
Scenario: AC-R14
  Given 必須拡張を利用するrunを開始する状態
  When Qualificationに該当操作を要求する
  Then install指定だけではqualifiedにしない
```

<a id="ac-r15"></a>
## AC-R15

要求：R15, REQ-R15。oracle参照：V01-04, V06-01, V26-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R15
  Given runを開始する状態
  When Qualificationに該当操作を要求する
  Then 無断fallbackとlive driftで資格が無効になる
```

<a id="ac-r16"></a>
## AC-R16

要求：R16, REQ-R16。oracle参照：V10-05, V13-02, V14-01, V14-05, V24-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R16
  Given writerが作業領域を所有している間
  When Runnerに該当操作を要求する
  Then 並列taskは別binding、停止未確認では再割当なし
```

<a id="ac-r17"></a>
## AC-R17

要求：R17, REQ-R17。oracle参照：V07-01, V10-01, V10-02, V10-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R17
  Given taskをclaimまたはresultを受け入れる状態
  When Schedulerに該当操作を要求する
  Then 二重claim/旧result/依存未達を拒否する
```

<a id="ac-r18"></a>
## AC-R18

要求：R18, REQ-R18。oracle参照：V22-01, V28-01, V28-02, V28-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R18
  Given 有効な委任と予算の範囲に未完了作業がある間
  When AgentとSupervisorに該当操作を要求する
  Then 通常失敗で完了や放棄にせず修正へ進む
```

<a id="ac-r19"></a>
## AC-R19

要求：R19, REQ-R19。oracle参照：V01-05, V14-04, V22-02, V28-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R19
  Given 検証の環境不足を検出した状態
  When Runnerに該当操作を要求する
  Then 構築可能を実施不能とせず実機不足をmockで代替認定しない
```

<a id="ac-r20"></a>
## AC-R20

要求：R20, REQ-R20。oracle参照：V20-01, V20-05, V26-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R20
  Given 候補成果物を検証する状態
  When Verifierに該当操作を要求する
  Then 自己報告ではなくコマンド/件数/内容の証拠がある
```

<a id="ac-r21"></a>
## AC-R21

要求：R21, REQ-R21。oracle参照：V21-01, V21-02, V21-03, V21-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R21
  Given 候補成果物を意味レビューする状態
  When Review Serviceに該当操作を要求する
  Then 自己reviewを独立reviewと表示しない
```

<a id="ac-r22"></a>
## AC-R22

要求：R22, REQ-R22。oracle参照：V04-02, V04-04, V20-03, V20-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R22
  Given 検証結果を発行し受け入れる状態
  When SignerとSupervisorに該当操作を要求する
  Then 偽署名・対象相違・古いchallengeを拒否する
```

<a id="ac-r23"></a>
## AC-R23

要求：R23, REQ-R23。oracle参照：V21-05, V22-01, V22-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R23
  Given 候補の必須検証またはレビューが不合格の場合
  When Supervisorに該当操作を要求する
  Then 失敗をPASSに変えず新候補を再検証する
```

<a id="ac-r24"></a>
## AC-R24

要求：R24, REQ-R24。oracle参照：V14-01, V22-04, V23-02, V23-06, V30-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R24
  Given runの異常終了またはlease失効が起きた場合
  When Recoveryに該当操作を要求する
  Then ACKのみやleaseのみで二重実行しない
```

<a id="ac-r25"></a>
## AC-R25

要求：R25, REQ-R25。oracle参照：V11-03, V11-04, V11-05, V22-05。状態：NOT_RUN。

```gherkin
Scenario: AC-R25
  Given 利用者停止・必要権限不足・予算超過の状態状態
  When Supervisorに該当操作を要求する
  Then 目標activeを理由に自動解除しない
```

<a id="ac-r26"></a>
## AC-R26

要求：R26, REQ-R26。oracle参照：V24-02, V24-03, V28-05。状態：NOT_RUN。

```gherkin
Scenario: AC-R26
  Given 個別候補を統合する状態
  When Integratorに該当操作を要求する
  Then 個別PASSを足し合わせず統合不合格なら修正する
```

<a id="ac-r27"></a>
## AC-R27

要求：R27, REQ-R27。oracle参照：V30-01, V30-05, V31-01, V31-05。状態：NOT_RUN。

```gherkin
Scenario: AC-R27
  Given 成果物を受け入れる状態
  When Release Gateに該当操作を要求する
  Then 必須成果物欠落や提出版相違で受入しない
```

<a id="ac-r28"></a>
## AC-R28

要求：R28, REQ-R28。oracle参照：V08-06, V23-05, V31-06。状態：NOT_RUN。

```gherkin
Scenario: AC-R28
  Given push/merge/publish/deploy等の外部反映を要求する状態
  When Effect Serviceに該当操作を要求する
  Then 公開未許可なら開発完了を保ち外部作用を行わない
```

<a id="ac-r29"></a>
## AC-R29

要求：R29, REQ-R29。oracle参照：V25-01, V25-02。状態：NOT_RUN。

```gherkin
Scenario: AC-R29
  Given UA/CompactionDB/SDD等の記録を利用する状態
  When Contextに該当操作を要求する
  Then 記憶や要約から逆にbaseline/完了状態を書き換えない
```

<a id="ac-r30"></a>
## AC-R30

要求：R30, REQ-R30。oracle参照：V18-05, V20-02, V29-01。状態：NOT_RUN。

```gherkin
Scenario: AC-R30
  Given 外部Web/README/tool outputを読み込む状態
  When Contextに該当操作を要求する
  Then 保護作用の認可は独立。悪意文の検出完全性は主張しない
```

<a id="ac-r31"></a>
## AC-R31

要求：R31, REQ-R31。oracle参照：V03-06, V17-01, V25-03, V25-04, V25-06。状態：NOT_RUN。

```gherkin
Scenario: AC-R31
  Given runの状態や実行証拠を記録する状態
  When Observerに該当操作を要求する
  Then 相関が辿れ、未実行は未実行、秘密は配布されない
```

<a id="ac-r32"></a>
## AC-R32

要求：R32, REQ-R32。oracle参照：V01-06, V11-01, V22-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R32
  Given runと反復処理を実施している間
  When Budget Serviceに該当操作を要求する
  Then 上限やunknown利用量を完了/ゼロ利用へ変換しない
```

<a id="ac-r33"></a>
## AC-R33

要求：R33, REQ-R33。oracle参照：V01-04, V06-01, V26-03, V30-04。状態：NOT_RUN。

```gherkin
Scenario: AC-R33
  Given CLI/plugin/skill/policy/環境を更新する状態
  When Qualificationに該当操作を要求する
  Then 旧資格を流用せず新runへ適用する
```

<a id="ac-r34"></a>
## AC-R34

要求：R34, REQ-R34。oracle参照：V03-01, V09-01, V20-01, V26-06, V30-03。状態：NOT_RUN。

```gherkin
Scenario: AC-R34
  Given 検証を再実行する状態
  When Verifierに該当操作を要求する
  Then 同じ対象の独立再実行結果を比較できる
```

<a id="ac-r35"></a>
## AC-R35

要求：R35, REQ-R35。oracle参照：V00-06, V03-03, V20-05, V31-02。状態：NOT_RUN。

```gherkin
Scenario: AC-R35
  Given 試験や完成状態を報告する状態
  When Reporterに該当操作を要求する
  Then 文書QA・過去試験・署名形式だけを製品合格にしない
```
