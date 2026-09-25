# Role profileと実効設定

`model_profiles.json`は利用者要求と役割の検査用viewであり、公式CLIへそのまま渡す設定ではない。実装時の編集正本はdotfiles `home/dot_agents/agent-config.yaml` のADH専用profile。ADH側のdesired constraintsと比較し、生成したnative設定・launcher・選択Skill・実metadataをReleaseSetへ束ねる。

A1/A3はFable-5.1/high、A2はGPT-6 Astra/xhigh。公式availabilityは実binaryと本人アカウントで確認し、能力未知を有効にしない。他用途profileは保持できるがADH実行へ流用しない。詳細は[配布仕様](../spec/11_DISTRIBUTION_AND_COMPOSITION.md)。
