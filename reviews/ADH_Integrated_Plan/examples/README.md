# 契約の記載例

全exampleは架空のfixtureで、実行権限、本人資格、稼働manifestではない。example://参照を実行へ渡してはならない。実際のタスクではWP01/05/17で確認済みのpath/hash/grantを使う。

model-execution.schema.jsonはADH内部契約であり、native APIへそのまま送らない。描画・qualified adapterは後続の本番実装範囲である。

## V3.1追加例

[TaskPacket](task_packet.example.json)に文書graph/closure/適用guard参照を追加した。[操作意図](operation_intent.example.json)、[GuardDecision](guard_decision.example.json)、[未資格確認](guard_qualification.example.json)を追加。全てexample_only/NOT_RUN相当であり認可や実証拠ではない。GuardDecision例はHOLDで、許可された署名tokenを含まない。

JSON Schema適合だけでは権限が有効にならない。実行時には現actor/grant/target/payload/policy/expiryを実サービスで再検証する。
