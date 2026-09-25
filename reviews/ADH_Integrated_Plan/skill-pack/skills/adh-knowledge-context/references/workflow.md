# 来歴付き文脈取得

同じproject/trust-domain/baseline/source snapshotに照会する。必須REQ/AC/SPEC/TEST/guardは正本の明示closureで取得し、Semanticaは補足に使う。短縮情報にはsource hash/range/retrieval refを保持する。

結果がstale/invalidなら原本へ戻る。原本が揃えば許可作業を継続、欠ければ該当taskだけHOLD。confidence、approved文字列、graph policyを権限やPASSに変換しない。query/extract/rebuildは異なる操作で、毎Edit/commitに再構築を混ぜない。

実装予定入口はADH `context` operationであり、Semantica公式CLIの架空subcommandではない。配置・実効呼出は資格確認後のみ。詳細は[知識仕様](../../../../spec/12_KNOWLEDGE_AND_CONTEXT.md)。
