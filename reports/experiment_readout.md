# Experiment Readout: First gate at level 40 vs level 30

| | |
|---|---|
| **Status** | Complete. Recommendation: **do not ship** |
| **Owner** | Product Analytics |
| **Players** | 90,188 (44,699 control / 45,489 treatment) |
| **Duration** | First 14 days after install for each player |

## Hypothesis
Moving the first gate from level 30 to level 40 will increase 7-day retention, because players get further into the game before they are interrupted.

## Result
**The hypothesis is rejected.** The level-40 gate *lowered* 7-day retention.

| Metric | Control (30) | Treatment (40) | Change | Significant? |
|---|---|---|---|---|
| 7-day retention (primary) | 19.02% | 18.20% | −0.82 pp (−4.3%) | Yes, p = 0.002 |
| 1-day retention | 44.82% | 44.23% | −0.59 pp | No, p = 0.07 |
| Rounds played (guardrail) | 51.3 | 51.3 | none | No |

## Trust checks
- ✅ Test had enough power for the primary metric (MDE 0.74 pp < observed 0.82 pp)
- ✅ One bot-like outlier (49,854 rounds) removed; conclusions are unchanged with or without it
- ⚠️ **Sample-ratio mismatch** (49.6/50.4 split, p = 0.009). The size is small, but assignment logging should be verified before the experiment is archived

## Impact
Shipping the level-40 gate would cost about **818 day-7 active players per 100,000 installs**.

## Decision and next steps
1. **Keep the gate at level 30.**
2. Engineering to investigate the SRM (owner: platform team).
3. Next test: gate at level 25, and a separate test on gate wait time.
4. Add revenue per user to the metric set for future gate experiments.
