# A4 — 独立機械検証

入力は凍結candidate、承認済suite inventory、RunManifestと対象hash。writer停止、別権限の実行領域、source/environment/suiteを確認する。検証コードへ製品認証や署名秘密鍵を渡さない。

commandのargv、cwd、開始終了、exit、signal、timeout、収集/実行/失敗/skip件数、原本artifact hashを直接採取する。AgentのPASS文から結果を作らない。0件・必須SKIP・欠損・途中終了を合格にしない。

model最適化の比較armでも同じ固定oracleを実行する。短いpromptや過去receiptを理由に独立・統合・最終試験を省略しない。原本の内容が同じでも、独立実行の責任を別stageの証拠で代用しない。

画面やモデルへ返す要約は原本と別にし、失敗件数・未充足要件・根拠参照を残す。検証結果の署名は被検証processの外で行う。role/profile/packet/Skill/rendererの版も既存policy hashへ結び付ける。

NOT_RUN、環境待ち、失敗、観測不能を区別し、収集結果と未実施をA1/A3へ返す。最終合格は同一RCと全必須条件で判定する。

各GRの正常許可・禁止・故障・正規復旧を指定tierで実測する。fake secretと制御宛先を用い、判定文ではなく対象側の作用を確認する。文書graphのQAと製品防御の動作を混同しない。


品質configも被検証コードである。保護されたinventoryを用い、凍結candidateを別scopeでcheck-only実行する。node/uv依存をその場で取得せず、source/ReleaseSet/toolchain/profileの実hashと件数を収集する。旧36/24検査は移管表のV4子で確認し、別々の成功件数として加算しない。
