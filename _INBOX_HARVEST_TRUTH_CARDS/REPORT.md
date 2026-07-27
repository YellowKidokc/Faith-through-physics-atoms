# Evolution Simulation Replication Report
Generated in the ChatGPT Python/container environment.
## 1. Self-consistency audit
- from_reported_Ne_required: 7050
- from_reported_mu_required: 7048.8
- from_reported_s_required: 7048.8
- from_reported_haldane_705: 705

**Finding:** the reported inverse-solver table is not internally single-target consistent. Reported Ne and the Haldane 705-innovation row imply ~705 events; reported mutation rate and selection coefficient imply ~7,050 events.

## 2. Recomputed baseline values
### Events = 705
- Ne_required: 89015.2
- mu_required: 9.79167e-08
- s_required: 0.0890152
- Haldane generations needed: 211500
### Events = 7050
- Ne_required: 890152
- mu_required: 9.79167e-07
- s_required: 0.890152
- Haldane generations needed: 2.115e+06

## 3. Coherence multiplier check
- Combined multiplier = 2200
- 1500 / combined = 0.681818
- 0.89 / 44 = 0.0202273

## 4. Human-chimp / ENCODE Haldane budget
- Human-lineage functional substitutions = 1.4e+06
- Haldane budget = 933.333
- Ratio = 1500
- Adaptive fraction threshold to fit = 0.000666667 (0.0667%)

## 5. Monte Carlo capacity sweep
- Events 705: success rate 0.5135
- Events 7050: success rate 0.2721

## Files
- cambrian_waiting_grid.csv
- g1000_adaptive_fraction.csv
- generation_time_sensitivity.csv
- monte_carlo_uncertainty_sweep.csv
- neanderthal_budget.csv
- results.json
