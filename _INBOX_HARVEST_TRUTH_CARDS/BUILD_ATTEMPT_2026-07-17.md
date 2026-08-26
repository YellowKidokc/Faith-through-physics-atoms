# Build Attempt

Date: 2026-07-17

Command:

```text
lake build
```

Working directory:

```text
H:\Desktop 2\LEAN 4\PROFESSIONAL_HANDOFF_2026-07-17\02_PRIMARY_LEAN_REPOS_SOURCE_ONLY\theophysics-lean-main
```

Lean/Lake versions:

```text
Lake version 5.0.0-src+b4812ae (Lean version 4.32.0-rc1)
Lean 4.32.0-rc1
```

Toolchain:

```text
leanprover/lean4:v4.32.0-rc1
```

Result:

The clean source-only build successfully resolved the Lean toolchain, cloned dependencies, and began compiling project modules. Several Theophysics modules built before the run was manually stopped because it expanded into a long dependency/mathlib build on the network drive.

Observed successful project module builds included:

```text
Theophysics_MaxwellTrinity
Theophysics_DelayedChoice
Final_Lean4_From_Excel
Theophysics_Coherence
Theophysics_ChiEvaluator
Theophysics_GodTest
Theophysics_Fracture
Theophysics_LawMechanisms
Theophysics_Fall
Theophysics_Universality
```

Warnings observed:

```text
Final_Lean4_From_Excel.lean: unnecessary simpa / unused variable warnings
Theophysics_LawMechanisms.lean: unused variable warning
```

No source-level Theophysics error was observed before manual stop. The later `Lean exited with code 4294967295` messages were caused by manually stopping child Lean processes, not by a displayed type/proof error.

Recommendation:

For professional review, run the build from a local SSD checkout or with dependency caches already materialized. The network-drive clean build is too slow/noisy for a quick audit.

