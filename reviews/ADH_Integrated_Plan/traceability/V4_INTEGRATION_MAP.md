# V4移管・統合の対応

旧SI36とDI24の検証を同じ48内包子へ集約した。2つの元計画を別々に読んで実装する必要はない。追加実行回数ではない。

| 入力 | 検査 | V4内包検査 | WP |
|---|---|---|---|
| SI | S01 | V06-01-U4-04, V13-03-U4-16 | WP06, WP13 |
| SI | S02 | V13-03-U4-16 | WP13 |
| SI | S03 | V18-01-U4-09 | WP18 |
| SI | S04 | V18-04-U4-11 | WP18 |
| SI | S05 | V26-04-U4-10 | WP26 |
| SI | S06 | V25-01-U4-14 | WP25 |
| SI | S07 | V18-03-U4-15 | WP18 |
| SI | S08 | V18-03-U4-15 | WP18 |
| SI | S09 | V09-05-U4-12 | WP09 |
| SI | S10 | V22-06-U4-13 | WP22 |
| SI | S11 | V25-02-U4-17 | WP25 |
| SI | S12 | V18-02-U4-20 | WP18 |
| SI | S13 | V18-02-U4-20, V26-04-U4-42 | WP18, WP26 |
| SI | S14 | V18-01-U4-09, V26-02-U4-21 | WP18, WP26 |
| SI | S15 | V18-06-U4-18, V29-05-U4-43 | WP18, WP29 |
| SI | Q01 | V03-01-U4-22 | WP03 |
| SI | Q02 | V06-04-U4-23 | WP06 |
| SI | Q03 | V14-06-U4-26 | WP14 |
| SI | Q04 | V14-06-U4-26 | WP14 |
| SI | Q05 | V06-03-U4-25 | WP06 |
| SI | Q06 | V06-03-U4-25, V24-03-U4-32 | WP06, WP24 |
| SI | Q07 | V03-02-U4-29 | WP03 |
| SI | Q08 | V03-02-U4-29 | WP03 |
| SI | Q09 | V30-06-U4-45 | WP30 |
| SI | Q10 | V14-05-U4-28 | WP14 |
| SI | Q11 | V03-01-U4-22, V29-01-U4-44 | WP03, WP29 |
| SI | Q12 | V20-05-U4-30 | WP20 |
| SI | Q13 | V30-02-U4-31 | WP30 |
| SI | Q14 | V14-06-U4-27 | WP14 |
| SI | Q15 | V29-05-U4-43 | WP29 |
| SI | I01 | V22-02-U4-34 | WP22 |
| SI | I02 | V29-01-U4-44, V23-03-U4-47 | WP23, WP29 |
| SI | I03 | V26-02-U4-35, V28-01-U4-39 | WP26, WP28 |
| SI | I04 | V30-06-U4-45 | WP30 |
| SI | I05 | V30-04-U4-07, V30-04-U4-37 | WP30 |
| SI | I06 | V31-02-U4-46, V31-05-U4-48 | WP31 |
| DI | DV01 | V06-02-U4-01, V31-02-U4-46 | WP06, WP31 |
| DI | DV02 | V06-01-U4-04, V03-01-U4-22 | WP03, WP06 |
| DI | DV03 | V13-03-U4-16, V14-04-U4-24 | WP13, WP14 |
| DI | DV04 | V06-02-U4-01, V30-06-U4-45 | WP06, WP30 |
| DI | DV05 | V03-01-U4-22 | WP03 |
| DI | DV06 | V30-04-U4-07, V30-06-U4-45 | WP30 |
| DI | DV07 | V18-01-U4-09 | WP18 |
| DI | DV08 | V18-03-U4-15, V25-02-U4-17 | WP18, WP25 |
| DI | DV09 | V13-03-U4-16 | WP13 |
| DI | DV10 | V18-04-U4-11 | WP18 |
| DI | DV11 | V09-05-U4-12 | WP09 |
| DI | DV12 | V25-01-U4-14 | WP25 |
| DI | DV13 | V26-02-U4-35 | WP26 |
| DI | DV14 | V26-01-U4-02, V26-02-U4-05, V26-02-U4-21 | WP26 |
| DI | DV15 | V25-02-U4-17, V29-01-U4-44 | WP25, WP29 |
| DI | DV16 | V03-02-U4-29 | WP03 |
| DI | DV17 | V14-04-U4-24, V06-03-U4-25 | WP06, WP14 |
| DI | DV18 | V14-06-U4-26, V24-03-U4-32 | WP14, WP24 |
| DI | DV19 | V06-04-U4-23, V14-06-U4-27 | WP06, WP14 |
| DI | DV20 | V14-05-U4-28 | WP14 |
| DI | DV21 | V20-05-U4-30 | WP20 |
| DI | DV22 | V28-01-U4-39 | WP28 |
| DI | DV23 | V29-05-U4-43 | WP29 |
| DI | DV24 | V31-02-U4-46, V31-05-U4-48 | WP31 |

## 合成経路

### V4-FLOW01: 生成・資格・開始

dotfiles canonical adh profile -> generated native configs -> effective probes -> pinned ReleaseSet -> TaskPacket -> durable dispatch; legacy express cannot satisfy product qualification

検査: V06-02-U4-01, V26-01-U4-02, V15-04-U4-03, V06-01-U4-04, V06-05-U4-08

### V4-FLOW02: 根拠・設計・実装

canonical required closure + ACL-scoped supplemental graph -> cited experiments/ADR/SPEC -> task packet -> implementation -> independent evidence; semantic candidates never authorize

検査: V18-01-U4-09, V26-04-U4-10, V25-02-U4-17, V18-06-U4-18, V28-01-U4-39

### V4-FLOW03: 整形から証拠失効

writer authorized fix -> new snapshot -> stale knowledge and receipts identified -> frozen check-only validation -> integration new receipt

検査: V06-03-U4-25, V14-06-U4-26, V24-03-U4-32, V26-03-U4-33, V22-04-U4-41

### V4-FLOW04: 並列実装・統合

disjoint worktrees -> independent quality and graph candidates -> single index publisher -> serialized ReleaseSet integration -> E2E

検査: V18-04-U4-11, V09-05-U4-12, V14-05-U4-28, V24-05-U4-40

### V4-FLOW05: 知識停止から復旧

graph unavailable -> exact canonical fallback if complete -> continue unrelated permitted tasks -> rebuild -> qualify; missing required source holds only its task

検査: V22-06-U4-13, V25-01-U4-14, V22-02-U4-34

### V4-FLOW06: Hook不稼働・迂回

absent/bypassed local hook -> protected independent inventory -> defect still found -> repair without disable-all

検査: V26-02-U4-21, V20-05-U4-30, V30-02-U4-31, V29-01-U4-44

### V4-FLOW07: 学習と配布

raw evidence -> candidate learning -> evaluation and authorized promotion -> new release -> no live policy swap

検査: V25-02-U4-36, V30-04-U4-37, V17-01-U4-38, V23-03-U4-47

### V4-FLOW08: 最終RC受け入れ

same two repository revisions + same scope + fixed checks + independent A3/A4 + operations restore -> single acceptance; NOT_RUN is never PASS

検査: V30-04-U4-07, V28-01-U4-39, V22-04-U4-41, V29-05-U4-43, V30-06-U4-45, V31-02-U4-46, V31-05-U4-48
