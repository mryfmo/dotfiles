このままでは、依存待ちで停止する工程と、実行しても退出条件を満たせない工程があります。以下、修正が必要な点です。位置はすべて対象文書の現行139行版です。

1. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:114`**  
   J8 は、D-024-31 が明示的に撤回した asks-only slice を復活させています。D-024-47 の「a05」を slice1 と読み替える根拠はありません。  
   **変更文:** 「make update は、D-024-14 の承認対象である ask 削除と同期 hook を一体で含む P1-14 a05 のマージ後とする。撤回済み slice1 をその代替にしない。」

2. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:84`**  
   slice1 は `dispatch_status: blocked-pending-premise-reconciliation` で、validator の前提不成立と生成 settings の allowed_files 漏れが残っています。reset metadata の追加だけでは送れません。  
   **追加文:** 「slice1 本文108–109行の未解決前提と生成物の編集範囲を解消し、承認対象との一致を確認するまで dispatch しない。」

3. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:85`**  
   make update と Codex 再着席だけでは P1-15 の配置は完了しません。a04 本文644–648行が要求する managed settings の管理者配置、専用ログイン、permgate 変更、起動検証が欠落しています。  
   **追加文:** 「P1-15 の配置は make update、install-managed-settings、操作者による管理者配置・専用ログイン・Codex escape-denial 適用、影響する Claude/Codex 席の再起動と実効設定検証までを含み、完了前は依存タスクを解放しない。」

4. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:85`**  
   `codex-worker-network-a01` が R0～R2 にありません。再着席だけでは manifest の `network_access: false` は直らず、transport 終了条件を満たせません。  
   **追加文:** 「P1-15 後に codex-worker-network-a01 を Claude 席へ割り当て、実装・監査・マージを終えてから make update と Codex 再着席を行う。」

5. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:72`**  
   #410 の a04 は未送達で、`after: [worker-write-boundary-a02]` を持つ P1-15 待ちです。R0 の update-branch → chain だけでは完成しません。  
   **変更文:** 「#410 は P1-15 の後継依存と配置完了を確認後、a04 の送達・worker 実装・RESULT を経て統合する。R0 の即時統合対象から外す。」

6. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:72`**  
   #439 の a07 は D-024-41 で停止済みです。private object store の実装修正を含む a08 reset が必要で、古い a07 の chain 再実行では解消しません。  
   **変更文:** 「#439 は a08 の reset review・送達・実装・RESULT 後に統合し、a07 の残存 P1 と S2 を chain の再実行で済ませない。」

7. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:87`**  
   `records-sync-pr-a01` は `security: true` です。P1-15 前に Claude 席へ出す救済案は D-024-20/25 と矛盾します。  
   **変更文:** 「救済タスクの security 判定と送達条件を確定し、security:true の Claude 席への送達は P1-15 の配置完了後とする。前倒しする場合は、素な allowed_files を持つ Codex 席へ明示的に割り当てる。」

8. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:50`**  
   現在の `boundary.sh:67` は `gh pr merge --squash --auto` を実行します。必須化すると、1本ずつの `--match-head-commit` マージ規則に反します。  
   **変更文:** 「boundary.sh は PR 作成までとし、auto-merge を予約しない。境界 PR も sweep 後の確認済み head を --match-head-commit で直列にマージする。」

9. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:76`**  
   現在の boundary.sh は変更された `.orchestration` 全体を収集し、対象リストを受け取れません。照合表を作っても、未承認本文や除外対象 task dir を運んでしまいます。  
   **変更文:** 「R1-6 前の境界も、照合済みファイルの明示リストだけを入力にできる経路を用意する。送達済み本文はマスクで書き換えず、bus hash と不一致なら拒否する。」

10. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:70`**  
    pre-send-check のマージを「P1-6 merged」としていますが、P1-6 の本体である記録生成と次タスク割当は完了しません。record-ledger-carry、record-json-sync、後続 slice の行もありません。  
    **変更文:** 「#442 は P1-6 の pre-send 部分のみ完了とする。record-ledger-carry、必要な JSON 同期、acceptance-front-matter --from-result、dispatch --next/default_after の実装・接続・実証を別行で完了するまで P1-6 を閉じない。」

11. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:95`**  
    #410 a04 は verdict 専用で、audit-pool は別タスクです。R2 に `audit-pool-a02` がなく、P1-10 の `--second-opinion` も同タスクの対象外です。  
    **追加文:** 「audit-pool-a02 と second-opinion の実装をそれぞれ残作業に追加し、integrate-seat は verdict・pool の必要機能がマージされた後に実装する。」

12. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:85`**  
    P1-7 のマージ済みタスクは hooksPath を明示的に除外しています。`worker-hooks-path-a01` が計画から抜け、DoD-P1 n は再着席しても満たせません。  
    **追加文:** 「worker-hooks-path-a01 を launcher 系列の後に実装・マージし、配置後に対象全席で実効 core.hooksPath=.githooks を検証する。」

13. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:68`**  
    #440 a06-checker は checker とテストだけを扱い、task-from-plan.py と plan-check.py を明示的に除外しています。「P1-12 merged」は元の完了条件を満たしません。  
    **変更文:** 「#440 は P1-12 checker 部分の完了とする。task-from-plan、plan-check、分類表と progress の同期検査を別タスクとして割り当て、元の P1-12 完了条件を検証する。」

14. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:107`**  
    J1 は owner 文を作るだけです。元の所見は owner の実装と依存配置の拘束を要求し、既存 binding-a01 自体も残作業表にありません。  
    **追加文:** 「trusted-entrypoint-binding-a01 と descendants-followup-a01 の対象・担当・依存・テスト・マージ順を残作業表に追加し、依存する guard/delivery/formatter/map の配置をその完了後に拘束する。」

15. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:110`**  
    J4 の「解消できない行だけ例外」は、DoD-P1 を変えないという宣言と全項目必須規則に反します。D-024-48 は plan 024 対象行の任意免除を認めていません。  
    **変更文:** 「plan 024 対象行は記録だけで例外化しない。必要な機構を第1段階へ移すか、対象と承認を明示して DoD を正式改訂するまで退出しない。」

16. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:99`**  
    却下された `result-precheck-a02→a03` が脱落しています。また task-generator a02 の却下理由は削除条項ではなく dispatch 前提の矛盾で、fixture のマージ済み本文も自由に変更できません。  
    **変更文:** 「対象を task_id・却下理由・固定済み本文の hash ごとに列挙し、result-precheck-a02 を含める。マージ済み・停止済み本文は書き換えず、正当な後継 reset または正式な waiver で処理する。」

17. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:100`**  
    旧65系統を第2段階へ残す一方、現行 checker 全体の rc 0 を要求しています。現行スクリプトには D-024-48 の日付による限定実行がなく、そのままでは退出できません。  
    **追加文:** 「D-024-48 の first TASK 日時による対象判定を検証した限定チェックを用意し、全体の raw rc と限定対象の判定を分けて記録する。task 番号の T133/それ以前では分類しない。」

18. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:100`**  
    S2 と着席以外にも、17行目の閉鎖 PR 9件、未追跡ファイル、残存 workspace 等が boundary check の違反になります。それらを解消する工程がありません。  
    **追加文:** 「退出前に boundary 出力を違反種別ごとの処置表へ展開し、閉鎖 PR の anchor、全 checkout の未追跡記録、workspace・identity・server 残存を所有者付きで解消する。未保存作業を破棄して緑にしない。」

19. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:35`**  
    M-05/C-114 の根本対策がありません。4スクリプトの昇格では、finding の kind を audit id に潰して S1 の件数を過少計上する問題は直りません。  
    **追加文:** 「require-crit-review.py と acceptance-front-matter.py の ledger grammar に provenance を保持するタスクを追加し、同一 head・番号の ci/worker/security 行が衝突せず全件計上される回帰テストを設ける。」

20. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:100`**  
    PRECHECK_REQUIRED を1へ切り替える工程がありません。最後に測るだけでは、DoD-P1 m の祖先確認と切替記録は生成されません。  
    **追加文:** 「P1-5 後、受理対象全席の branch head に対して P1-5 merge commit の祖先確認を行い、全件成功後に PRECHECK_REQUIRED=1 として時刻・head・コマンドを記録する。」

21. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:75`**  
    #378/#396/#404/#412 を再分類するだけで、その後の実装・統合がありません。D-024-47 は #378 merge、#396/#404 continue を既に決めており、同表には #412 の処置がありません。  
    **変更文:** 「#378 は統合担当と順番、#396/#404 は継続担当・依存・RESULT/merge 条件、#412 は後継 lineage との関係を個別行に記し、再分類の記録だけでは完了にしない。」

22. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:97`**  
    #432 の stop+hold と第1段階後の reset は D-024-44/47 にありますが、progress の P1-2 は同系統を未完了扱い、DoD-P1 a は hold を #395 のみに限定しています。整合処理がありません。  
    **追加文:** 「P1-2 の既達成範囲と #432 の残件を分離し、第2段階の owner 行へ移す。DoD-P1 a の #432 の扱いも D-024-47 に合わせて明示する。」

23. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:100`**  
    e/h/i/j/k は測定だけでなく実証作業が必要です。4席同時稼働、連続2波、shadow一致4件、全差分との比較2件、監査同時2本の計画がありません。95行目は h を「統合2件」と誤引用しています。  
    **追加文:** 「退出前に4席の実証波を2波設定し、対象 PR・測定窓・担当・shadow比較4件・差分/全差分比較2件・監査同時2本と全閾値を検証する。h の条件は4席同時稼働とする。」

24. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:56`**  
    S-R2 と C-115 は handoff、再起動、履歴 timeout、25ツール上限の代替になりません。C-115 自体も恒久 timeout の worker task を要求しています。  
    **変更文:** 「P1-9 は handoff/再起動記録、履歴読みの時間制限、20分・25ツール制約と無応答処置を検証して閉じる。local-review/chain の恒久 timeout と失敗通知も別タスクで実装する。」

25. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:96`**  
    「P1-15 の後」だけでは依存が不足します。dispositions は a05、hold は resolver、loop-limits は checker・helper・vocabulary・契約準拠 caller を必要とします。  
    **追加文:** 「各タスクを個別行に分け、P1-14 a05→dispositions、ci-efficiency resolver→hold/loop-limits、checker・contract helper・vocabulary・caller移行→loop-limits の順と実在する後継 task_id を記す。」

26. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:83`**  
    #431 の既存ブランチには広い a03 実装が残ります。本文だけを4分割して同ブランチをマージしても、slice1 に全差分が混入します。また75/97行目の #431 close とも衝突します。  
    **変更文:** 「元ブランチを保存したうえで各 slice の変更だけを対応 PR に抽出し、各 PR の base・allowed_files・numstat を検証する。#431 を継続するか置換するかは一方に統一する。」

27. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:82`**  
    4スライスへの要求配賦表がなく、Makefile、validator、orchestrator-only hook、`.claude/settings.json` 等の所属と中間状態の成立条件が不明です。依存本文の古い a02 参照更新も未計画です。  
    **追加文:** 「a04 の全 allowed_files・threat 行・受入所見を slice ごとに対応付け、各 merge 時点の render/test 成立を示す。全 consumer の after/premises を最終後継 task_id に更新して再検査する。」

28. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:49`**  
    新しい系統本文の禁止に対し J1 は新 owner 本文を要求し、R0 は dispatch なし、R1 は並行送達としています。停止対象と例外の境界が確定していません。  
    **変更文:** 「dispatch 凍結は未列挙の実装系統に適用する。必要な owner/review 本文、承認した継続・救済タスクを task_id で列挙し、各送達可能時点を定める。」

29. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:51`**  
    「a04 を653行のまま送る」は R1-1/J2 と矛盾し、200行・Checks込み230行・S-R4の200行拒否も不一致です。J2 のC-80「1～3回」も同じ行の最大2回と食い違います。  
    **変更文:** 「a04 は4スライスに再計画する。本文全体の上限は Checks 込み200行、allowed_files 8件とし、C-80 は最大2回、worker修正回数と同一クラス所見数は別々に記録する。」

30. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:113`**  
    #442 の pre-send は自己宣言 cap を検査するだけで、200行・8ファイルの全体上限を実装しません。上限実装の担当もなく、R2 の既存本文を免除するかも不明です。  
    **追加文:** 「global cap の実装を別タスクに割り当て、境界値と allowed_files 件数をテストする。既存本文の適用対象を列挙し、対象なら verdict 376行、pool 262行、hold 309行、dispositions 287行等を送達前に分割する。」

31. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:86`**  
    glue の pre-send にある C-112 の caller矛盾検査と C-116 の既存id検査は #442 a02 の仕様に含まれません。repo版呼出しへの移行で対策が落ちます。  
    **追加文:** 「pre-send の昇格差分として C-112/C-116 を明示的に引き継ぎ、mandatory環境＋caller編集禁止、既存id衝突、正当な amendment/reset の回帰テストを追加する。」

32. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:86`**  
    ファイルの昇格と wrapper 化だけでは「同類ミスがCIで止まる」は成立しません。全 RESULT・revise・chain の入口への接続と、raw dispatch の迂回防止が未定義です。D-024-46 の P1-5 owner との重複も未整理です。  
    **変更文:** 「各入口を送信前検査・pr-task解決・RESULT証跡検査へ接続し、その拒否を実際の caller からテストする。result-evidence の2検査は D-024-46 の P1-5 owner と統合し、撤回済み系統を重複作成しない。」

33. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:52`**  
    夜間 merge は「日中測定が通れば可能」と読めますが、60行目では無条件停止です。herdr/codex exec の例外表現と S-R3 の全 mutation 禁止も一致しません。  
    **変更文:** 「本計画では22:00～07:00 JSTのmergeを停止する。sandbox外操作は種類にかかわらず操作者不在時には開始せず、例外を設ける場合は対象と条件を別途明記する。」

34. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:52`**  
    日中でも操作者は不在になり得ます。C-122 が要求する「不可避の gate-bound 呼出し前に holds/PING を送る」がなく、6時間停止の原因が残ります。  
    **追加文:** 「gate-bound 操作の前に操作者の対応可能性を確認し、holds/PINGと独立作業を先に開始する。不在時は時刻に関係なくキューへ回す。」

35. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:49`**  
    WIP の「マージ予定8本」は後続予定の5本や #439 を含むか不明で、救済2本も別枠です。GitHub の23本に対する update-branch 対象制御と実行期限がありません。  
    **追加文:** 「active WIP の PR 番号集合と除外集合を保存し、救済を含む上限・dispatch判定コマンド・超過時の停止動作を定める。held/parked PR は更新対象から外し、close/reclassify の期限を定める。」

36. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:73`**  
    2マージごとの実施は境界の大きさの上限ではありません。また gate-ready code より境界を優先すると C-110 の再発になります。  
    **追加文:** 「境界はファイル数・総bytesの上限で分割し、超過時は拒否する。gate-ready code PR がある場合、当該 code の regime 前提となる境界以外は後回しにする。」

37. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:60`**  
    head別ログ数を chain 起動回数・修正ラウンド数と混同しています。同一起動の update-branch 前後ログが重複し、18行目の4標本も incorrect/local P1 で停止しています。  
    **変更文:** 「chain は起動単位で重複排除し、head数・worker修正回数と分ける。7～20分は停止までの観測値として扱い、security review・audit・disposition・gateを含む完了時間を別集計する。」

38. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:60`**  
    R0-0～6 は #439 を含め9PRで、8本ではありません。追加境界、R1/R2、配置、実証波の所要がなく、orchestrator の処理量を再び数え落としています。  
    **変更文:** 「同じ40～90分/PRの仮定でもR0本体は9PRで6～13.5時間とし、境界は別計上する。R1/R2と実証波を含む担当別の作業量・並列枠・臨界路・日中/夜間待ちを見積もる。」

39. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:103`**  
    J1/J3/J4/J5/J7/J8 は既定・代替それぞれの追加実装、レビュー、操作者作業、待ち時間が不足しています。「review profile」「空き席」「もう一方」も実行主体として未確定です。  
    **追加文:** 「各判断に既定と代替の task/PR数、依存、レビュー数、操作者操作、追加待ち時間と不確実性を記す。各作業行は identity・task_id・完了selector・使用枠を確定する。」

40. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:101`**  
    R2-2 は既に空行で、「同じスライス」の参照先がありません。救済の scope/cap と出力消費者への影響も不明で、境界が2回通るだけでは正規化の検証になりません。  
    **変更文:** 「R2-9 は対象スクリプトの実在パス・allowed_files・担当・依存を持つ独立行とする。home/secret/NUL/不正UTF-8のfixture、head/task/verdictの保持、既存consumer互換を検証する。」

41. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:138`**  
    「返答による合意後」と「1時間無回答なら開始」が矛盾します。project-map の既定表示規則は、この計画や権限変更への承認を与えません。  
    **変更文:** 「既存承認の範囲内で進める操作と、新たな合意を必要とする変更を分ける。後者は無回答を承認と扱わず、既承認の独立作業を続ける。」

42. **P1・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:111`**  
    squash 後のブランチ削除で公開commitが到達不能になるという J5 の前提は誤りです。PR refs、キャッシュ、取得済みcloneに残り得ます。[GitHub公式説明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)。  
    **変更文:** 「squash は main の祖先への混入だけを防ぐ。c1566ff5 は PR refs・キャッシュ・cloneに残り得るため、露出内容と残存の受容を判断し、必要なら Support に削除可否を照会する。」

43. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:112`**  
    「remove/addで操作者プロンプト6回」は未実測で、D-024-32 の「add は操作者操作不要」および85行目の1回/席と不一致です。席転換も commit 済み作業の破棄を必然にはしません。  
    **変更文:** 「remove/add の操作数は実測し、拒否時のみ操作者へ提示する。既存commit・branch・lineageを保持し、転換費用は再着席と文脈引継ぎの時間として示す。」

44. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:15`**  
    現在の #447 は初回commit＋修正4commitです。初回変更blobのNUL混入は5ファイルで、「追加3本」「NUL1」、101行目の「NUL6」は一致しません。  
    **変更文:** 「boundary 26 は初回319→最終320ファイル、追加修正4commit、NUL混入5ファイル（確認head 75828c96、07:32:34 JST以降）」とし、32/101行目も統一する。

45. **P2・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:22`**  
    DoD-P1 c は未計測ではありません。progress.tsv の DoD-P1 行に23:00の `chezmoi verify rc 1` と canonical clone の遅れが記録されています。  
    **変更文:** 「cは未達（直近23:00 JSTにrc 1、canonical 60a6fb2b が origin/main f7f38067 より古い）。配置後に再計測する。」

46. **P3・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:13`**  
    `07:28Z` は16:28 JSTで、観測時刻と9時間ずれます。「全数値は07:1x以前」も後続更新と両立せず、34行目のopen 20は12行目の23と時点未分離です。  
    **変更文:** 「観測は項目ごとにISO8601日時・head・保存済み出力pathを記す。席表は07:28 JST、open 20は過去値と明記し、一律07:1x以前という断定を削除する。」

47. **P3・確信度: 高 — `.orchestration/plans/024-replan-20261021.md:17`**  
    27,975行ログの保存先がなく、72/7/65、閉鎖PR9、未追跡698/27,834を当該時点へ再照合できません。29行目のreset12対記録11、32行目の737にも具体的な出所が不足します。  
    **追加文:** 「各件数に集計対象・単位・除外規則・実行コマンド・保存出力を添付し、reset件数とanchor review件数を分離する。出力のない数値は未検証と表示する。」

📝 まとめ: 読み取り専用レビューを完了し、47件を指摘しました。ファイル変更・実装テスト・実機配置検証は未実施で、保存先不明の過去集計は未検証です。現案には実行停止と退出条件未達のリスクが残ります。
Verdict: incorrect