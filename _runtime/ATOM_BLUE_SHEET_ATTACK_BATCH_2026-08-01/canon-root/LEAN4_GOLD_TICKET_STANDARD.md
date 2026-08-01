# Lean 4 Gold Ticket Standard

Status: canon display rule  
Purpose: make formal proof receipts visible without overstating what they prove

## The Rule

A document may show a **Lean 4 Gold Ticket** only when all four conditions are true:

1. A `.lean` file exists.
2. The `.lean` file has been compiled in the current environment.
3. A report exists naming what Lean checked.
4. The ticket states what Lean did **not** prove.

Gold does not mean:

- theology proved
- physics proved
- history proved
- bridge proved
- public-ready

Gold means:

> The formal claim named in the ticket compiled under Lean 4, and the limits are visible.

## Markdown Ticket

Use this block in Markdown documents:

```md
> **LEAN 4 GOLD TICKET**
>
> **Status:** compiled locally  
> **Lean file:** `path/to/file.lean`  
> **Report:** `path/to/report.md`  
> **What Lean checked:** short plain-language statement  
> **What Lean did not prove:** short plain-language boundary  
```

## HTML Class

When converting to HTML, render the ticket with this class:

```html
<aside class="lean-gold-ticket">
  <div class="lean-ticket-label">LEAN 4 GOLD TICKET</div>
  <p><strong>Status:</strong> compiled locally</p>
  <p><strong>What Lean checked:</strong> ...</p>
  <p><strong>What Lean did not prove:</strong> ...</p>
</aside>
```

Suggested style:

```css
.lean-gold-ticket {
  border: 1px solid rgba(212, 175, 55, .75);
  background: linear-gradient(180deg, rgba(212,175,55,.14), rgba(212,175,55,.045));
  box-shadow: 0 0 0 1px rgba(255,255,255,.04), 0 12px 36px rgba(212,175,55,.10);
  border-radius: 8px;
  padding: 16px 18px;
}
.lean-ticket-label {
  color: #e7c65a;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
}
```

## Proof Labels

Use these labels consistently:

| Label | Meaning |
|---|---|
| `LEAN_FORMAL_PROOF` | Lean proves the named formal theorem under stated definitions/assumptions. |
| `LEAN_CONDITIONAL_PROOF` | Lean proves the conclusion if the listed assumptions are granted. |
| `LEAN_GUARDRAIL_SUPPORTED` | Lean supports a boundary, distinction, or proof-discipline rule. |
| `LEAN_CANDIDATE_ONLY` | Lean is mentioned or planned, but no current compiled receipt exists. |

## Current Gold Tickets

As of 2026-07-31:

1. `P-00-opening-postulates`
   - Lean file: `D:\DONT TOUCH HTML\theophysics-canon\lean\P00_OpeningPostulates.lean`
   - Report: `D:\DONT TOUCH HTML\theophysics-canon\lean\P00_OpeningPostulates_REPORT.md`
   - Label: `LEAN_GUARDRAIL_SUPPORTED`

2. `T-01-the-hard-questions`
   - Lean file: `D:\DONT TOUCH HTML\theophysics-canon\lean\T01_HardQuestions_Posture.lean`
   - Report: `D:\DONT TOUCH HTML\theophysics-canon\lean\T01_HardQuestions_Posture_REPORT.md`
   - Label: `LEAN_GUARDRAIL_SUPPORTED`

## Clean Line

> If the ticket is gold, the formal receipt exists. If the receipt does not exist, the ticket stays gray.
