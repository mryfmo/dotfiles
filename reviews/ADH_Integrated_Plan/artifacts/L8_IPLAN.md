# L8 IPLAN — 再開可能なAgent実行計画

[32WP](../registers/work_packages.json)、[検証台帳](../registers/verification_cases.json)、[実行順序](../docs/03_BOOTSTRAP_AND_RUN_ORDER.md)が正本。文書分類のL1→L10順をtask順へそのまま転記しない。taskは前提のaccepted、scope非重複、資格、資源、予算を満たして解放する。

各taskには対応R/REQ/AC/IC/MO/DG/GR、入力baseline/文書closure、Worktree/binding、実model/effort、許可/禁止、作業step、成果物、検査、checkpoint、復旧、完了条件を持たせる。普通の修正は逐次の「続けて」を待たず、真正な外部待ちは対象だけ保持する。

## 今回の追加を実装する順

WP00–02で原本・実能力・文書/脅威契約を固定→WP03/04で検査とschema→WP05/06でbootstrap配送・最小指示・実効guard→WP07/08で状態/権限/CHG→WP09–17で領域・dispatch・native強制→WP18/19で上流文書graph→WP20/21で独立合否→WP22–25で復旧/統合/観測→WP26/27で実資格/自己ホスト→WP28/29で全工程・故障→WP30/31で同RC配布・受入。

これは既存DAGを短絡する順序ではない。準備だけ可能なE0/E1はPREPARED_ONLYで進め、依存受入を偽らない。各guard全体の後期実AI資格を早期schema WPの完了前提にして循環を作らない。


## V4全体統合

計画実行はWP00–31に統一。旧SI/DIを別実行せず、repo-qualified scopeとReleaseSetでdotfiles配布とADH本体をまとめて変更する。
