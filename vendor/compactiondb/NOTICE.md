# Notice and provenance

CompactionDB 2.0.0 is a clean-room reimplementation derived from the functional requirements and failure analysis of the user-provided `CompactionDB.zip`.

The design also applies general software-engineering patterns used by append-only ledgers, durable spooling, event sourcing, bounded context projections, and hierarchical caches. The VictorTaelin/OptMem source code is **not copied, vendored, translated, or included** in this distribution. OptMem was used only as an externally reviewed design comparison; its repository did not expose a license at the time of the analysis, so this package deliberately contains no OptMem code.

This distribution is licensed under the MIT License in `LICENSE`. Third-party embedding models or commands configured by an operator are not included and remain subject to their own licenses and terms.
