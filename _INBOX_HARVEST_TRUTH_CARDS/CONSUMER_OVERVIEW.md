# Consumer Overview

This folder is for readers who want the meaning of the Lean work without having
to become Lean 4 users first.

## What We Did

We took several Theophysics claims and translated their structure into Lean 4,
a proof assistant used to check whether mathematical definitions and theorems
are internally consistent.

The current work does three things:

1. Defines the formal objects used by the argument.
2. Proves narrow statements about those objects.
3. Builds adversarial controls that should fail if the structure is real.

The third point is the most important. A weak formalization can make almost
anything pass. This project tries to make close false positives fail.

## The Main Implication

The Lean work moves the project from "this sounds structurally similar" toward
"here is the exact structure, here are the guards, here are the cases that fail,
and here is the boundary of what has actually been proved."

That matters because it turns debate into inspection. A reviewer can now ask:

- Are the definitions faithful?
- Are the rejection controls strong enough?
- Are the assumptions too convenient?
- Does a better false positive pass the gate?
- Does the theorem prove more than the prose claims?

Those are the right questions. The proof assistant does not remove the need for
judgment; it tells us where judgment must focus.

## The Strongest Current Piece

The strongest current file is `ResurrectionFormal/MaxwellTrinity.lean`.

It formalizes a triadic gate for the Maxwell/quaternion EM and Trinity claim.
The code checks that the intended candidate satisfies the gate, while several
nearby false positives fail:

- vector-only Heaviside-style EM fails the coupling guard;
- modalism fails relational distinctness;
- static single-field EM fails dynamic-field requirements;
- arbitrary three-part systems fail role-profile requirements;
- relabeled roles fail because labels alone do not preserve structure.

The point is not that a theorem settles theology or physics. The point is that
the proposed structure now has explicit load-bearing constraints.

## What This Does Not Prove

It does not prove Christianity from physics. It does not prove new physics. It
does not prove that every source document has been perfectly encoded into Lean.

It proves narrower, inspectable statements about the formal system we wrote.
That is still valuable because it gives reviewers a real target.

