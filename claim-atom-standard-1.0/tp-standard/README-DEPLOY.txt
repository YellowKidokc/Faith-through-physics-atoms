CLAIM-ATOM STANDARD 1.0 — DEPLOY NOTES
======================================

WHAT THIS IS
Static files. No build step, no dependencies. Drop the folder into
Cloudflare Pages (or any static host) rooted at faiththruphysics.com.

LAYOUT -> URLS
  index.html                      -> /                      (standard landing)
  vocab/context.jsonld            -> /vocab/context.jsonld  (the vocabulary — canonical)
  resolver/map.json               -> /resolver/map.json     (ID -> address indirection)
  claims/A042/L9/C{1,2,3}.html    -> /claims/A042/L9/C1 ... (human view, JSON-LD embedded)
  claims/A042/L9/C{1,2,3}.jsonld  -> raw records for machine readers
  papers/POF2828-2026-0001.html   -> /papers/...            (paper = tour over claims)

CLOUDFLARE PAGES SPECIFICS
1. New Pages project -> direct upload (or push this folder to the
   faiththruphysics-site-data repo and connect it).
2. Custom domain: faiththruphysics.com (or mount under a subpath and
   update resolver/map.json "resolves_to" accordingly — that's the
   whole point of the resolver).
3. Optional _headers file for clean content types:
     /vocab/context.jsonld
       Content-Type: application/ld+json
     /claims/*
       Access-Control-Allow-Origin: *
   (CORS open on claims lets other people's tools resolve your IDs.)
4. Clean URLs: Pages serves C1.html at /claims/A042/L9/C1 automatically
   with "clean urls" behavior; if not, keep .html in links (already done).

MINTING NEW CLAIMS
Copy any C*.jsonld as a template. Rules:
- @id and claimID must agree through the resolver map.
- claimClass from the enum in vocab (floor-axiom | definition | theorem |
  bridge | empirical-anchor | prediction | boundary).
- dependsOn: full URLs of parents. Never cite a claim you depend on
  only in prose.
- falsificationCondition: required. No port, no publication — it's
  commentary, and gets claimClass accordingly.
- verificationStatus: "machine-verified" ONLY with kernelChecked true
  and a named system. Everything else is "informal". Lie here and the
  whole instrument is worthless.
- challengeStatus starts "unchallenged". That's honest, leave it.

EDGES (building on / disputing)
Human picks one of two intents; the type is computed:
  build-on  + same domainType as parent  -> expands
  build-on  + different domainType       -> bridgesTo (grade it: Part D ladder)
  dispute   + targets the falsification  -> challenges
  dispute   + different answer           -> forksFrom

PROPAGATION (manual until tooling exists)
When a claim goes verificationStatus="falsified": walk everything whose
dependsOn chain reaches it, set challengeStatus="upstream-falsified".
One SQL pass against Postgres once the graph is imported; by hand until then.

NEXT
- Import the axiom tables from PG17 (laptop, port 5432, trust auth,
  guide at A:\_protocols\active\INFRASTRUCTURE_CONNECTION_GUIDE.md)
  and mint records for the floor + schemata. That's the seed population.
- Point the GTQ pages' JSON-LD at claim IDs as they get minted.
