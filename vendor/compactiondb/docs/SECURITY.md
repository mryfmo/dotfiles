# Security model

## threat model

主な脅威:

1. tool input/output内のcredential保存
2. `.env`や秘密鍵のfile content保存
3. 別sessionのraw event混入
4. DB lock時の無言のevent loss
5. 過去logに含まれるprompt injectionの再実行
6. local DBの誤commit・共有
7. corrupted spool/DBによる復旧誤動作

## controls

### pre-persistence redaction

redactionはSQLite書込み前だけでなく、spool保存前に実施します。raw secretをrecovery queueへ残しません。

対象例:

- Anthropic/OpenAI/GitHub token
- AWS access key
- JWT
- Bearer token
- password、secret、API key、token key/value
- PEM private key block
- basic-auth URL

### sensitive path suppression

次を含むpathではcontent fieldとtool responseを省略します。

- `.env*`
- `.git/`
- `.ssh/`
- `.aws/`
- `.gnupg/`
- private key、certificate/key store
- credential/secretを示すfilename

### local permissions

POSIX環境ではdirectory `0700`、DB/spool/error file `0600`を設定します。WindowsではACLとPOSIX modeが一致しないため、OS側のprofile ACLを併用してください。

### prompt injection boundary

recovery packetの先頭に、履歴は命令ではなくevidenceであり、現在の依頼と独立に検証するよう明示します。raw log内のcommandやURLを自動実行する設計ではありません。

### session isolation

raw event queryとautomatic recoveryはexact `session_id`を必須とします。project-wide queryはCLIで明示した場合だけです。

### durability and observability

- atomic spool
- fsync
- one writer lock
- SQLite WAL / FULL synchronous
- idempotent `event_uuid`
- quarantine
- health/error log
- detail hash verification

## residual risks

- regex redactionは完全なDLPではない
- source codeやbusiness data自体はsecret patternに該当しない場合がある
- application-level encryptionは未実装
- malicious user with filesystem access can read or alter local data
- optional embedding commandへmemory textを渡すため、そのcommandのtrust boundaryを別途評価する必要がある
- heuristic memory promotionは誤分類し得る

機密性が高いprojectでは、`capture_file_contents=false`、短いretention、full-disk encryption、dedicated user accountを推奨します。
