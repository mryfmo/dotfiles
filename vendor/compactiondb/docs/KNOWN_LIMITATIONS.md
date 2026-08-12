# Known limitations

1. **Claude Code実機E2E未実施**  
   この生成環境にはClaude Code executableがないため、hook JSON schemaに対するunit/integration testは実施しましたが、Claude Code UI上の `/hooks`、実際のauto-compaction、resumeを含むE2Eは未実施です。

2. **heuristic memory extraction**  
   automatic extractionはkeywordとexplicit markerを使用します。heuristic candidateは高確度でもsession scopeに限定されますが、LLMによる意味理解、矛盾判定、entity resolutionは行いません。cross-session利用には明示markerまたは手動promotionが必要です。

3. **application-level encryptionなし**  
   filesystem permissionとOSのdisk encryptionを前提とします。

4. **semantic searchはoptional adapter**  
   embedding modelは同梱しません。外部commandを設定しない限りFTS5 searchだけです。

5. **redactionはbest effort**  
   未知形式のcredential、business-sensitive text、画像・binary内のsecretを完全には検出できません。

6. **SQLiteはsingle-node local store**  
   network shareや複数machineからの同時利用を想定していません。

7. **hierarchical summaryはextractive**  
   LLM abstractionではなく、deduplicated bounded text projectionです。原本は`memories`に残ります。

8. **Windows ACL**  
   Windowsでのprocess lock pathは実装していますが、本成果物の自動testはLinux上で実行しています。Windows ACLの実効permissionは環境ごとに確認が必要です。
