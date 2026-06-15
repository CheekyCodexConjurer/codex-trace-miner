# Trace Fusion Scorecard

Score each category from 0 to 3.

| Category | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Mode selection | Always uses same mode | Mode chosen vaguely | Mode matches rough risk | Smallest mode that reduces real risk |
| Role clarity | Agents overlap | Roles named only | Roles mostly scoped | Each agent has bounded purpose and stop condition |
| One write owner | Multiple overlapping writers | Ownership unclear | One writer claimed | One writer verified and scoped |
| Independent evidence | Consensus by agreement | Evidence shallow | Evidence checked | Independent evidence and disagreement synthesis |
| Context routing | Reads randomly | Reads obvious files | Reads relevant files | Names read, skipped, fallback, and uncertainty |
| Validation | No validation | Assertion only | Targeted checks | Checks plus evidence or explicit blocker |
| Final review | Summary only | Checks some items | Finds real gaps | Blocks unresolved requirements/risks |
| Runtime overhead | Slows trivial work | Often too heavy | Usually proportional | Adapts none/mini/full/critical correctly |

## Adoption Rule

- Adopt Trace Fusion when it improves evidence, scope control, validation, or review quality without adding unnecessary ceremony.
- Revise if it improves review quality but slows trivial or low-risk work.
- Reject a Fusion mode for a task if it creates multiple write owners or hides uncertainty.

## Run Record

| Field | Baseline | Trace Fusion |
| --- | --- | --- |
| Prompt |  |  |
| Repo fixture |  |  |
| Date |  |  |
| Mode |  |  |
| Agents |  |  |
| Validation commands |  |  |
| Total score |  |  |
| Regressions |  |  |
