# V4統合評価と実製品受け入れ

## 判定を混ぜない

文書QA、component contract試験、実library/CLI試験、本人Auth、実VM、実AI E2E、性能比較を区分する。48統合subcaseは既存192親の中に割当済み。旧SI36＋DI24は対応元の別名であり追加の実証件数ではない。

## モデル最適化

元の72セル（H00/H10/H01/H11 × U/B/E/R/I/C ×3）と48公開入力はbyte同一で保持。対照promptに過去版ラベルがあっても試験入力として固定したもので、現在の仕様正本ではない。すべてのarmにV4の同じ強制policy、ReleaseSet、knowledge backend、quality rules、input/source、権限、予算を適用し、promptの効果だけを測る。H11の18runと製品18runの共有は同じ最終条件とrun IDのときだけ。モデルとeffortは変更しない。

新2Skills用の12公開事例はstack_skill_routing_cases.jsonにある。旧48と合わせ60件各3回、別途A3が凍結後に未見群を封印する。負例は初期routeの判断であり、正当な後続作業に別Skillが必要になることを禁止しない。語句を含むだけで必須発火としない。

## 知識K0/K1

knowledge_cases.jsonの12fixtureを各3回・2条件で計72照会run。K0は原本と明示closureのみ、K1は同じ必須closure＋Semantica補足。source/ACL/source時点/問い/モデル/予算を同じにする。測定前にfixtureの具体的IDと期待集合・禁止集合・版をA4が作りA3が凍結し、評価対象Agentへgoldを渡さない。

必須根拠欠落0、誤引用0、ACL漏えい0、authority変更0が最低条件。時間、取得bytes、tokenが観測可能な範囲、不要原本読取、stale/再構築、失敗を全保存する。3反復は統計的最適性の保証ではなく最低回帰。改善が確認できなければ速度優位とは表示しない。知識機能の適合と性能優位を別に判定する。

## 品質Q0/Q1

quality_cases.jsonの8fixtureを、既存適合経路とprek/Oxc適合経路、cold/warm、各3回で96実行cell。対象file集合・必要rule・型条件・例外・入力内容・CPU/メモリを固定する。必要な残余checkerを含めて比較し、対象やruleを減らして高速化しない。cold/warmは依存取得有無、process/cache状態を明示する。チェック本体は事前準備後offlineで再現する。

必須欠陥検出と対象一致、元index/working無変更、formatter冪等、秘密漏えい0、終了状態の正しい分類を先に満たす。end-to-end時間、p50/p95の参考値、メモリ、診断数を記録する。少数反復で安定p95や倍率保証を主張しない。実データが悪い場合は適合profileを見直して新RCで再試験し、旧失敗を消さない。

## 合成E2E

U/B/E/R/I/Cの既存oracleにV4-FLOW01〜08の対応を加える。Semanticaの候補が正本へ昇格する、format後の古いreceiptを使う、Hook不実行でCIまで通る、AutoSkillがmodel/guardを更新する、二repo片側更新をactiveにする、という負例が必ず不合格になること。期待動作・原本・ファイル・process・操作結果をA4が外から確認する。

各試験のrun metadataにはReleaseSet、source snapshot、必須規範closure、quality/knowledge/profile/native/asset版、actor/attempt/fenceとraw artifactを含める。probeに一度成功しても配布物更新後は該当資格を再確認する。実行できないtierを低いtierへ置換しない。
