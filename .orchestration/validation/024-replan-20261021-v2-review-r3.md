現案だけでは無人で完遂できません。改訂 3 で直接の循環依存は直っていますが、別の停止条件、実装工程の欠落、検証前の機能使用、見積りの不整合が残っています。

`gh` は接続に失敗しましたが、GitHub コネクタで [open PR 23 本](https://api.github.com/repos/mryfmo/dotfiles/pulls?state=open&per_page=100)、[#447](https://github.com/mryfmo/dotfiles/pull/447) の head・チェック成功、[#396](https://github.com/mryfmo/dotfiles/pull/396) と [#412](https://github.com/mryfmo/dotfiles/pull/412) の異なる base を確認しました。

以下の位置はすべて [.orchestration/plans/024-replan-20261021-v2.md](~/Workspace/dotfiles/.orchestration/plans/024-replan-20261021-v2.md) です。修正文は本文への追加・置換案です。

1. **P1・確信度: 高 — `024-replan-20261021-v2.md:106`**  
   `chain-integrate.sh` は security review を実行しません。実装は local review・sweep・記録・audit までなので、R0-1/2/6 の書き方では必須レビューが欠落します。  
   **修正文:**「R0 の各 mechanism PR は、chain が確定した最終 head に対する独立した security-profile review と task-level audit の両方を揃えてから統合する。chain 自体は security review を実行しない。」

2. **P1・確信度: 高 — `024-replan-20261021-v2.md:75`**  
   `chain-integrate.sh` は audit で終了し、最終 disposition・acceptance・integration gate・merge は行いません。「chain → merge」だけでは必須工程を飛ばせます。  
   **修正文:**「chain 後は Orchestrator Playbook step 10 の順で全所見の disposition、最終 acceptance、3 種の evidence と review receipt を渡す gate を完了し、その gate が認めた head だけをマージする。」

3. **P1・確信度: 高 — `024-replan-20261021-v2.md:105`**  
   sweep 後に最新 head を取得してそのままマージするため、sweep 対象と異なる新 head を承認済みとして扱えます。`--match-head-commit` だけではこの間隙を閉じません。  
   **修正文:**「`head40` は検証済み feedback evidence の `head_sha` から取得し、GitHub の現在 head と一致することを確認する。不一致なら sweep と disposition をやり直し、その同一 head を `--match-head-commit` に渡す。」

4. **P1・確信度: 高 — `024-replan-20261021-v2.md:132`**  
   「段階 B 完了まで Codex 依存タスクを解放しない」は、B に至るための Codex 担当 slice・a05 まで止める読み方になり、循環を再導入します。  
   **修正文:**「段階 B 待ちは新しい Codex network/permgate 設定を必要とする後続タスクに限る。R1-2、R1-3、R1-5、R1-8、R1-11 は表の個別前提を満たせば transport 付きで先行できる。」

5. **P1・確信度: 高 — `024-replan-20261021-v2.md:171`**  
   R3 は「R2 の後」なのに、実証対象は R2 で既に実装・マージ済みとなるタスクです。同じタスクを実装波として再実行できません。  
   **修正文:**「実証は R2 の指定タスクを送達・実装・受理する実際の 2 波に重ね、R3 はその記録の判定と退出処置を行う。指定波を実施するまで該当 R2 行を完了扱いにしない。」

6. **P1・確信度: 高 — `024-replan-20261021-v2.md:171`**  
   第 2 波の R2-14 は R2-13 に依存するため、この 4 本を同時開始して DoD-P1 h を実証できません。  
   **修正文:**「第 2 波から R2-13 の後継である R2-14 を外し、他の 3 本と依存関係も allowed_files の重複もない別タスクを配賦表で確定する。」

7. **P1・確信度: 高 — `024-replan-20261021-v2.md:147`**  
   verdict a04 は shadow 専用で、未作成の `dotfiles-T133-verdict-apply-a01` に application を明示的に分離しています。この残件が計画になく、P1-4a の元の機能範囲を完了できません。  
   **修正文:**「`dotfiles-T133-verdict-apply-a01` を独立行に追加し、shadow 校正合格後の application、席証跡の受理、実 caller 接続を担当 identity・検証 selector・merge 条件付きで実装する。」

8. **P1・確信度: 高 — `024-replan-20261021-v2.md:171`**  
   差分監査の使用と、その有効化前に必要な全差分監査との比較順がありません。DoD-P1 j は比較 2 件が揃うまで差分監査を無効としています。  
   **修正文:**「初期は全差分監査を正本とし、差分監査は判定に使わない shadow として比較する。所見差 0 を 2 件記録してから有効化し、その後に DoD-P1 i の所要時間を測る。」

9. **P1・確信度: 高 — `024-replan-20261021-v2.md:134`**  
   `records-sync-pr-a01` の allowed_files は `records-sync.py`・そのテスト・記録だけです。本文は API による task text 同期を要求し、`boundary.sh` の実装もローカル git 操作も許可していません。  
   **修正文:**「records-sync-pr-a01 は既存仕様の task text 同期として実装する。boundary.sh の明示リスト・マスク・上限・照合・PR 作成は別の正規 task に分離し、その task の完了後に boundary-list.sh を廃止する。」

10. **P1・確信度: 高 — `024-replan-20261021-v2.md:156`**  
    #412 は未送達の `anthropic-auth-route-check-followup-a07` による reset・実装修正待ちです。update-branch と再監査だけでは現在 head の問題を直せません。a07 は 314 行で分割対象でもあります。  
    **修正文:**「#412 は a07 の分割・本文レビュー・reset anchor・a012 への送達・実装・RESULT を経て統合する。現 head 2b6fc7fc の update-branch だけでは完了にしない。」

11. **P1・確信度: 高 — `024-replan-20261021-v2.md:162`**  
    descendants の完了後に guard/delivery 等の「依存する配置」を解放するとしていますが、段階 A はそれらを既に配置・使用して network タスクを解放します。どの配置を止めるのか未確定です。  
    **修正文:**「段階 A で使う各 hook と実行体を列挙し、既存 binding のまま許容する範囲・残余・代替制御を明示する。完全 binding を必要とする機能だけを R2-15c 待ちとし、段階 A 自体との循環を作らない。」

12. **P1・確信度: 高 — `024-replan-20261021-v2.md:131`**  
    hooks・pins・binding・descendants のマージ後に、実機へ適用する工程がありません。特に hooks が段階 B より後に入れば、段階 B の再着席では有効になりません。binding は manifest 準備・cache seed・実ホスト検査も要求します。  
    **修正文:**「これらの最終マージ後に canonical clone 更新、make update、必要な manifest 準備・明示 cache seed・offline 配置検査、影響席の再着席を行い、実ホスト検証が成功してから各配置行を閉じる。」

13. **P2・確信度: 高 — `024-replan-20261021-v2.md:146`**  
    record-ledger-carry 本文163行は accepted trusted parent・resolver・safe-YAML を dispatch 前提としますが、R2-3 の依存には resolver も #436 もありません。  
    **修正文:**「record-ledger-carry の送達前提に R0-3、R2-15a、resolver とその caller 準備の完了を追加し、実際に使用する trusted parent と依存 provisioning の証跡を Checks に貼る。」

14. **P2・確信度: 高 — `024-replan-20261021-v2.md:146`**  
    `record-json-sync-a01` は「取り込み」としか書かれず、D-024-37 の hold 解除、C-88 による再執筆、レビュー、送達の工程がありません。段階 A だけでは #436 の成立も保証しません。  
    **修正文:**「record-json-sync-a01 は #436 と launcher slice のマージ後に C-88 で再執筆・C-80・送達・実装するか、撤回して同じ要件を P1-6 の名前付き後継 task へ移管する。」

15. **P2・確信度: 高 — `024-replan-20261021-v2.md:150`**  
    loop-limits は送達済み・blocked の Codex 指定本文ですが、ここでは a011 に移しています。既存本文は245行・allowed_files 10件で、新本文として再送する場合は方針 C にも収まりません。  
    **修正文:**「loop-limits は a012 が既存本文の前提成立後に再開する。a011 へ変更する場合は担当・境界前提を再計画し、200 行・8 entries 以下へ分割した正式な後継本文をレビューして送る。」

16. **P2・確信度: 高 — `024-replan-20261021-v2.md:150`**  
    loop-limits に必要な vocabulary と orchestrator 所有の `family:` 分類について、作成担当・完了条件・依存辺がありません。pool が語彙を作る工程とも未接続です。  
    **修正文:**「loop-limits は R2-1 の語彙マージ後とし、orchestrator が全 class の family を確定して保存する。欠落・未知 class の検査が成功してから再開する。」

17. **P2・確信度: 高 — `024-replan-20261021-v2.md:150`**  
    loop-limits と P1-6 は writer・dispatcher を共有します。既存本文が要求する直列化が表にないため、a008 と a011 が同時編集できます。provenance 変更も同じ writer を触ります。  
    **修正文:**「共有 writer/dispatcher のマージ順は P1-6 → loop-limits → provenance とし、各後続は直前の main を取り込んでから実装・検証する。」

18. **P2・確信度: 高 — `024-replan-20261021-v2.md:149`**  
    3 前提をまとめたままで、task_id・selector がなく、「orchestrator 所有の別変更」と担当 a009 も一致しません。r2 #10 の独立した実行行になっていません。  
    **修正文:**「caller 移行、CI Python provisioning、consumer fixture を3行に分け、各行に正規 task_id、a009 または orchestrator の一方、allowed_files、検証 selector、証跡 path を記入する。」

19. **P2・確信度: 高 — `024-replan-20261021-v2.md:74`**  
    dispatch 許可には task_id が必須なのに、second-opinion、P1-6 slice2/3、integrate-seat、global cap、記録形式、provenance、timeout、handoff、限定 checker 等には正規 task_id がありません。配賦表の R1-1 は主に WWB の分割表です。  
    **修正文:**「配賦表は R1〜R3 の全未完了実装行を対象とし、正規 task_id・本文 path・担当・使用枠・依存・検証・証跡を固定する。未記入行は dispatch 不可とする。」

20. **P2・確信度: 高 — `024-replan-20261021-v2.md:129`**  
    「a010 or a012」、R1-9 の二択、R2-15a の Claude 代替、R3 の「Codex 1 席」が未確定です。誰がいつ割当を決めるのかもありません。  
    **修正文:**「orchestrator が各送達前に実行 identity を一つに固定して配賦表へ記録する。代替席への変更時は元席の hold と task の runtime 前提を確認してから再割当する。」

21. **P2・確信度: 高 — `024-replan-20261021-v2.md:162`**  
    「配置検査の selector」は selector の実体ではありません。R2-9 の「S-R4 が機械で効く」、R2-13 の「alarm wrapper 不要」等も合否コマンドが未確定です。  
    **修正文:**「各行の完了条件に実在または作成予定の完全な test selector と検証コマンド、期待 rc、保存先を記入する。R2-15c は対象4系統それぞれの実行体・入力・拒否検査を列挙する。」

22. **P2・確信度: 高 — `024-replan-20261021-v2.md:126`**  
    22 paths・90 threat entries の配賦表と中間 CI 成立条件は依然未作成です。4 分割は仮説のままで、J2 の費用と R1 見積りの基礎にはできません。  
    **修正文:**「4 分割とその費用は未検証の候補とする。配賦表と各中間状態の検証結果を添付してから分割数・task 数・見積りを確定し、成立しなければ dispatch 前に改訂する。」

23. **P2・確信度: 高 — `024-replan-20261021-v2.md:74`**  
    active が8本のときも dispatch を許すため、後継 PR が開くと9本になります。将来作成される PR の枠を予約していません。  
    **修正文:**「dispatch 判定は active PR と、まだ PR を作っていない実装中タスクの予約枠の合計で行い、新規割当後も8以下となる場合だけ送達する。」

24. **P2・確信度: 高 — `024-replan-20261021-v2.md:156`**  
    完了条件の「open PR ≤ 8」は、第6節の active 上限8と別物です。#395、Phase 2 drafts、continue PR を残したまま active を8本使うと満たせません。  
    **修正文:**「完了条件は active＋予約枠≤8、未分類0、保持 PR は台帳の保持理由と owner があることとする。open 総数を制限する場合は別の上限と close 対象を定める。」

25. **P2・確信度: 高 — `024-replan-20261021-v2.md:114`**  
    #432 の残件を移す Phase 2 owner が名前付きで存在せず、P1-2 の元の完了条件を何の証拠で満たすかも未確定です。PR close だけでは P1-2 は閉じません。  
    **修正文:**「P1-2 の監査継承・lint CI 実行条件を該当 merge と CI 証跡で検証する。#432 の全未解決所見は正規の Phase 2 owner task に移し、その task_id を分類表と progress に記録する。」

26. **P2・確信度: 高 — `024-replan-20261021-v2.md:226`**  
    a07 本文78・274行は #396 を #412 の merge まで保持すると要求します。J12 の早期 close と既存 worker 契約が矛盾します。  
    **修正文:**「J12 採用時は a07 の #396 保持条項も後継本文で更新し、worker に同じ close 方針を送達する。更新前に旧契約と異なる close を実施しない。」

27. **P2・確信度: 高 — `024-replan-20261021-v2.md:114`**  
    既承認の #417 close を J11/J12 の合意待ちにまとめ、第14節の「返答を待たず進める」と衝突しています。  
    **修正文:**「#417 close は D-024-47 の既承認として単独実施する。#432 と #396 の close だけを各 J の合意待ちに分ける。」

28. **P2・確信度: 高 — `024-replan-20261021-v2.md:105`**  
    sandbox 内で行う既承認 #447 merge にまで操作者在席を必須化し、第14節の既承認運用を止めています。C-122 が要求する不在制限は sandbox 外操作です。  
    **修正文:**「既承認の sandbox 内 merge は日中に自律実行する。sandbox が拒否した場合だけ、holds/PING 後に操作者在席を確認して許された再試行を行う。」

29. **P2・確信度: 高 — `024-replan-20261021-v2.md:115`**  
    記載された `boundary-list.sh <list-file> <branch>` は、現存 glue が必須とする第3引数 `<title>` を欠くため usage error になります。  
    **修正文:**「暫定入口は `.agents/worklog/orchestrator-glue/boundary-list.sh <list-file> <branch> <title> [--dry-run]` とし、この実体と引数で拒否・正常系を検証する。」

30. **P2・確信度: 高 — `024-replan-20261021-v2.md:115`**  
    全 task text に bus の TASK hash を要求すると、送達しない advisory owner の task file を境界へ運べません。現存 glue の owner-file 例外とも不一致です。  
    **修正文:**「送達済み本文は最新 TASK hash と照合する。未送達の owner-only 本文は別区分とし、正規 task_id・レビュー済み bytes/hash・所有関係を確認して運ぶ。名前の suffix だけでは免除しない。」

31. **P2・確信度: 高 — `024-replan-20261021-v2.md:116`**  
    transport の契約が task・PR・branch を結びません。現存 glue は head を含む PONG を読まず、worktree tip の祖先も受理するため、「別 head 拒否」だけでは誤 branch・古い PONG を防げません。  
    **修正文:**「transport は task_id・PR・worker identity を入力または正本から解決し、最新 PONG/RESULT の head、対象 worktree tip、PR head branch の対応を照合する。不一致・古い送信・別 branch を拒否するテストを加える。」

32. **P2・確信度: 高 — `024-replan-20261021-v2.md:119`**  
    PRECHECK_REQUIRED の保存場所を将来の report に委ね、なければ「全 caller の明示環境」としていますが、caller 一覧も設定ファイルも決まっていません。  
    **修正文:**「切替前に強制旗の正本ファイルと全受理 caller を列挙し、各起動・再起動経路が同じ値を消費するよう設定する。設定場所、caller 一覧、再起動後の拒否出力を evidence に保存する。」

33. **P2・確信度: 高 — `024-replan-20261021-v2.md:106`**  
    C-113/D-024-46 が要求する「毎 RESULT の判断前」の glue 検査は、R0-1 にしか明記されていません。恒久化前の他 RESULT で M-04 が再発し得ます。  
    **修正文:**「R2-17 と入口接続の完了までも、全 RESULT の判断前に `result-evidence-check.sh <task> <head40> <pr>` を必須実行し、非ゼロなら受理・chain を開始しない。」

34. **P2・確信度: 高 — `024-replan-20261021-v2.md:165`**  
    Make が実行する境界 checker は `scripts/check-regime-boundary.sh` です。R2-18 は counters と Make だけを対象とし、実際の違反列挙入口への scope 適用が作業範囲から落ちています。  
    **修正文:**「限定実行は `scripts/check-regime-boundary.sh`、必要な counters、Make 入口とテストを対象とし、各違反種別に同一 scope が適用されること、全体判定を失わないことを検証する。」

35. **P2・確信度: 高 — `024-replan-20261021-v2.md:172`**  
    却下6件を一括して「後継本文の anchor accept」で処理するのは不十分です。元 acceptance は R02/R04/R06/R10 を V3a 待ち、R08 を owner disposition 後の再レビュー、R12 を本文修正後の再 anchor と区別しています。  
    **修正文:**「R02/R04/R06/R10 は固定済み本文を書き換えず waiver、R08 は既存 owner disposition を確認して一項目再レビュー、R12 は2所見修正後に再 anchor とする。各対象の旧 hash・証跡・checker 結果を個別に記録する。」

36. **P2・確信度: 高 — `024-replan-20261021-v2.md:185`**  
    「旧系統65」は T133 以外の数であり、first TASK 日時による旧系統数ではありません。未実施と明記した判定を、waiver 承認対象では確定値として再使用しています。  
    **修正文:**「waiver 対象数は R0-15 の確定後に記入する。reset_of を辿った系統の first TASK と日付の timezone を明示し、旧65という接頭辞集計を承認対象数に使わない。」

37. **P2・確信度: 高 — `024-replan-20261021-v2.md:213`**  
    費用列は揃っていません。特に J3/J5/J9/J10/J11/J12/J13 では task/PR、レビュー、依存、作業時間、待ち、未計測が双方にありません。  
    **修正文:**「各 J の既定・代替に同じ費用欄を設け、ゼロは0、未計測は未計測と記す。J11 は移管先 reset、J12 は a07 再計画、J13 は代替制御実装まで含めて比較する。」

38. **P2・確信度: 高 — `024-replan-20261021-v2.md:219`**  
    「secret pattern 0」は第1節の secret-pattern 修正1件と矛盾します。実際の cea358ea の差分は python-pin acceptance 中の変数代入例のマスクで、列挙された token-prefix grep は validator の全パターン検査ではありません。  
    **修正文:**「初回履歴には home path と validator の secret-pattern に一致する変数代入例があった。実 credential の有無は公開各 commit を validator と内容分類で確認し、その証跡に基づいて残存受容を判断する。」

39. **P2・確信度: 高 — `024-replan-20261021-v2.md:203`**  
    記載式は `(40〜90)×8＋30×3＋10×8` 分＝490〜890分、約8.2〜14.8時間で、7〜14時間になりません。  
    **修正文:**「この式だけの R0 は8時間10分〜14時間50分とする。境界回数・重複計上・追加工程を確定した後に幅を再計算する。」

40. **P2・確信度: 高 — `024-replan-20261021-v2.md:204`**  
    記載された R1 の項別合計は28〜49時間で、30〜52時間との追加差分が説明されていません。操作者待ちは別途加算なのかも不明です。  
    **修正文:**「R1 の項別合計は28〜49時間であり、追加の予備2〜3時間を置くならその根拠を別項にする。操作者待ちは工程別に別計上し、合計への算入方法を示す。」

41. **P2・確信度: 高 — `024-replan-20261021-v2.md:205`**  
    R2 は枝番を含め23行で、18行ではありません。26 task の内訳もなく、7波×5〜8時間は35〜56時間で、36〜60時間と一致しません。  
    **修正文:**「全23行から実装 task、操作者作業、重複 owner を分け、分割後 task 数を配賦表から集計する。その DAG と席制約で波数を計算し、予備時間を別表示する。」

42. **P2・確信度: 高 — `024-replan-20261021-v2.md:207`**  
    85〜146時間を1日8〜10時間で処理するなら約9〜19日です。上限15日は146時間÷8時間/日から導けず、夜間停止・操作者待ちの扱いも不明です。  
    **修正文:**「暦日は担当別の実作業時間と並行実行可能時間から再計算する。単純換算を示す場合は約9〜19日＋未計測待ちとし、夜間停止を二重加算しない。」

43. **P2・確信度: 高 — `024-replan-20261021-v2.md:204`**  
    R1 見積りの列挙には author-loop、records-sync、glue 昇格、参照走査、a08 の実装・統合がありません。J7 の本文約14本・10〜16時間の配賦先も不明で、orchestrator 負荷を再び数え落としています。  
    **修正文:**「R1-1〜11 の全行について orchestrator・worker・review 文脈・操作者の手番時間を分け、J7 の執筆時間を対応行に配賦する。重複を除いた資源別合計と待ち行列を見積りに含める。」

44. **P2・確信度: 高 — `024-replan-20261021-v2.md:197`**  
    C-80 15〜30分は保存ファイルの時刻だけでは所要時間を実証できません。また1 PR 40〜90分、slice 3.5〜6時間、各波5〜8時間など、合計に使う入力の種別・導出がありません。  
    **修正文:**「各入力を実測・仮定・未計測に分類し、実測は開始終了を対応付けた標本と集計出力を示す。実証できない所要は仮定へ変更し、修正率50%をどこへ算入したかも式で示す。」

45. **P3・確信度: 高 — `024-replan-20261021-v2.md:15`**  
    保存なしの PR 件数、worktree 件数等が「未検証」と表示されず、観測日時も `10:1x` 等です。`ls *-design-reset.md` は累積33件で、当日11件の抽出規則を示しません。自ら定めた証跡規則を満たしていません。  
    **修正文:**「保存出力のない過去値は未検証と表示する。当日 reset 11件は日付による抽出条件と対象名を保存し、各観測を確定した ISO8601 時刻・head・実行コマンド・出力 path に結び付ける。」

46. **P3・確信度: 高 — `024-replan-20261021-v2.md:32`**  
    reset 記録11件・anchor review12件から「reset12系統」は導けません。「欠陥数が本文の大きさに比例」も比較標本のない因果の断定です。  
    **修正文:**「当日 reset 記録11件、batch anchor review12件、accept6/reject6を別の単位で記載する。大本文と所見増加の関係は仮説とし、系統別の行数・所見数・ラウンド数で検証する。」

47. **P2・確信度: 高 — `024-replan-20261021-v2.md:159`**  
    このホストには `timeout` も `gtimeout` もありません。C-115 もその事実を記録しており、P1-9 の `timeout 60` をそのまま実行できません。  
    **修正文:**「履歴読みは既存の Perl alarm 方式で60秒に制限する。`perl -e 'alarm shift; exec @ARGV' 60 <history-command> …` の実コマンド・終了状態・保存先を記録する。」

過去所見97件の本文照合結果は以下です。「対応確認」は要求された修正を本文で確認した意味で、関連工程全体の正しさを保証するものではありません。

| レビュー | 本文で対応確認 | 部分対応・未解消 |
|---|---|---|
| r1・47件 | 1–8、11、13、15、17–19、24、26、29、31、33–34、36–37、40–45 | 9、10、12、14、16、20–23、25、27–28、30、32、35、38–39、46–47 |
| r2・50件 | 1–9、11、13–14、17–22、25、27、30–31、35–38、45、47–50 | 10、12、15–16、23–24、26、28–29、32–34、39–44、46 |

残件の対応先は、r1では 9→所見29–30、10→14、12→12、14→11/21、16→35、20→32、21→10/26、22→25、23→5–8/20–21、25→13/16–18、27→22、28→19/23、30→10/15、32→33、35→23–24、38→39–44、39→19–21/37、46–47→45–46です。r2では 10→18、12→11/21、15→19、16→35、23→22、24→32、26→25、28→8/21、29→5–6/20、32→19–21、33→29–30、34→31、39→44–45、40→41、41→42–43、42→27–28、43→37、44→38、46→45です。

第14節の「無回答は承認ではない」と、R1-3 → 配置A → network → 配置Bという抽象的な順序自体は修正されています。ただし、既承認操作への追加待ちと Codex 一括凍結の文言が、その修正を実行上で崩しています。

📝 まとめ: 原典・既存タスク・bus・Git・GitHub状態・過去97件を照合し、47件の修正点を報告しました。  
未実施: ファイル変更、実装テスト、実機配置。未保存の過去集計・所要時間分布は未検証で、現案には停止・検証漏れ・退出不能のリスクが残ります。  
Verdict: incorrect