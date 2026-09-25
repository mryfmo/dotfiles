# 非機能・構築・運用の統合仕様 v3.1

## 構築順序

管理VMを構築し、Supervisor用ユーザー、local DB、artifact store、公開鍵trust storeを作る。外部公開listenerは作らない。次にユーザー専用native実行VMと、資格情報を持たない検証VMを作る。CLI/OS/依存のdigestを固定したimageを登録し、本人の公式Authをnative環境内で初期設定する。その後、Plugin payload・Skill・Hook・model capabilityをpreflightし、署名可能なVerifierを接続する。

最後に小さいfixture projectで上流・実装・fail/repair・reconcile・受入を通し、native/VM/full-E2Eの必須項目が合格して初めて運用可能にする。本計画ZIPは設計・作業契約であり、この環境の構築スクリプトや実稼働結果を含まない。

## ネットワーク

Researchは外部一次資料を取得するが、private address/metadata/credential endpointへの到達を許さない。必要な社内sourceは明示登録したconnector経路へ分離する。Native model接続は公式製品の正規経路のみ。パッケージ取得は検証済みartifact mirror/allowlist付きbuilder経路へ分ける。検証VMは原則外向き通信なし、E2E用loopback/私設サービスnetだけ許可。Native sandboxの通信禁止で必要な検証が動かない場合は、Runnerの承認済み検証環境を使い、全部のsandboxを解除しない。

## 資格情報と鍵

公式Authは製品のcredential storeに置き、Supervisor DB・report・snapshot・CompactionDBに複製しない。署名secretはVerifierのhost-side signerまたは専用key serviceに置き、実行するrepoコードとは別権限にする。確認済みのpublic key/role/ownerをtrust storeに登録し、鍵revocation時は該当receiptの可用性を再評価する。署名があってもsignerが侵害されれば証拠は偽装できるので、TCBを限定し更新を監査する。

## 監視

task stuck、last-progress、lease、runner alive、budget、unverified MUST、evidence mismatch、Auth失効、native model/skill差、outbox backlogを監視する。監視は単に30秒ごとにLLMへ『続けて』を送る実装にしない。現在の実行・失敗分類・許可された次行動に基づく。進捗は会話の長さではなくartifact/検証/未充足条件の変化で判断する。

## Backup / restore

SQLite稼働中のDB単体だけをコピーしない。DBの整合したbackup方式とartifact storeのhash参照を同じcheckpointで保存する。WALとlocal filesystemの制約を守る（出典索引を参照）。restoreはread-only integrity検査→artifact hash照合→native session存在確認→runner quiescence→outbox再送→許可範囲内再開の順。

## アップグレード

新しいnative/plugin/OS payloadを別資格確認環境へ導入→schema再生成/契約差分→unit/contract/integration/security/E2E→lock更新→署名deployment承認。既存run中にpolicyやSkill本文だけをlive reloadしない。新runから切り替え、旧runは旧hashのまま終了するか明示migrationする。

## 対象外・残余リスク

有限試験で未知バグゼロを保証しない。VM脱出、管理者侵害、侵害された公式配布物、悪意あるVerifier、暗号鍵漏えい、誤った上流要求まで自動的に解決するものではない。適切な権限設計、配布検証、独立review、バックアップと緊急停止で影響を制限する。

## 固定の非機能基準

単一control hostのlocal SQLite WAL。Python3.13系列とuv lock。lease120秒、heartbeat30秒、termination grace10秒を初期設定とし、環境/設定に記録して試験する。durationはmonotonic clock、再起動はepochを照合する。lease期限だけで新writerを開始しない。

有限予算はnative calls、観測token/cost、wall time、並列数、transport retry、repair attemptを別カウンタにする。未知usageは0ではない。絶対値は操作者委任としてbindingし、未設定の有料runを開始しない。通信retryをコード修正成功と混同しない。

性能基準は管理VM4vCPU/8GiB以上・local disk、32並列request/1000task/10分を記録する。初期目標はwarm process crash復旧開始120秒以内、committed eventのprocess crash RPO=0。VM起動・外部待ち・実機電断保証とは分離する。latencyはLLM応答時間を除いて測定する。

全35MUST、必須検証PASS100%、必須SKIP/NOT_RUN/BLOCKED/UNKNOWN/XFAIL=0、受入阻害finding=0。Ruff差分/違反0、Pyright strict error0。本番自作Pythonはline95%以上/branch90%以上、安全重要domainはbranch100%。分母除外や基準緩和でgreenを作らない。6 scenario×3runの実AI全工程、clean install/restore/upgrade/rollback、同一RCの独立監査を必須とする。

これらは設計上の受入基準で、今回達成した実測値ではない。有限試験で未知欠陥不在を保証しない。


## モデル最適化の運用条件

モデルは指定high/xhighのまま。モデル別packの供給byte数・不要発火・停止・時間・利用量を観測する。private thinkingやnative内部cacheの未公開値は収集しない。比較条件/指標/予算/認定は[評価規約](../evaluation/EXPERIMENT_PROTOCOL.md)に従い、未計測を改善済にしない。

モデル最適化用の著者編集目標はspec/06に定める。文字数を超えたというだけでMUSTや重要な例外を削除せず、関連参照へ分割し、真に必要な超過は理由付きで許容する。

## ガードの運用・故障予算

[GR仕様](09_GUARDRAILS.md)の強制点と所管を実配置へ結び付ける。故障中の必須認可・耐久記録をfail-openにしない。純監視の障害は安全spoolで隔離し業務側の成功/失敗を改変しない。各guardのp50/p95遅延、誤拒否、不要承認、滞留、復旧・作用重複を計測する。未指定の業務SLOを架空数値で保証しない。採用環境の有限timeout・再試行上限は実行前に具体値を固定する。

資格鍵、baseline、guard policy、固定oracleはwriterから変更不可。正当な更新はCHGと独立レビューで可能にし、誤規則を永久固定しない。緊急停止・限定例外もactor/target/expiry/revalidationを監査し、未実施検査のPASS化は例外として許可しない。
