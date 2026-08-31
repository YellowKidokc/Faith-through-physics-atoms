-- Claim Atom Expansion Canon v1.1 — SQLite target schema
-- Four primary object layers: CLAIM, EVIDENCE, PROOF, PROCESS
-- Generated from THE_CLAIM_ATOM_EXPANSION_CANON_v1_1_FOUR_OBJECT_LAYERS_FULL.md
--
-- This is an additive target schema. It does NOT migrate or overwrite
-- _canon/index.sqlite. Legacy IDs and legacy proof_label values are preserved.

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

BEGIN;

CREATE TABLE IF NOT EXISTS schema_registry (
  schema_id          TEXT PRIMARY KEY,
  schema_version     TEXT NOT NULL,
  canon_document     TEXT NOT NULL,
  canon_hash         TEXT,
  created_at         TEXT NOT NULL,
  description        TEXT NOT NULL,
  is_active          INTEGER NOT NULL DEFAULT 0 CHECK (is_active IN (0,1))
);

CREATE TABLE IF NOT EXISTS controlled_terms (
  vocabulary         TEXT NOT NULL,
  term               TEXT NOT NULL,
  label              TEXT,
  definition         TEXT NOT NULL,
  introduced_version TEXT NOT NULL,
  retired_version    TEXT,
  sort_order         INTEGER,
  PRIMARY KEY (vocabulary, term)
);

CREATE TABLE IF NOT EXISTS actors (
  actor_id            TEXT PRIMARY KEY,
  actor_type          TEXT NOT NULL CHECK (actor_type IN
                         ('HUMAN','AI','PROCESS','INSTITUTION','INSTRUMENT','UNKNOWN')),
  display_name        TEXT NOT NULL,
  authority_scope     TEXT,
  identity_uri        TEXT,
  metadata_json       TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS source_objects (
  source_id           TEXT PRIMARY KEY,
  source_uri          TEXT,
  media_type          TEXT,
  byte_size           INTEGER CHECK (byte_size IS NULL OR byte_size >= 0),
  acquired_at         TEXT,
  source_hash         TEXT,
  original_filename   TEXT,
  preservation_state  TEXT NOT NULL DEFAULT 'PRESERVED',
  surrogate_reason    TEXT,
  information_loss    TEXT,
  created_by_actor_id TEXT REFERENCES actors(actor_id),
  metadata_json       TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS source_spans (
  span_id             TEXT PRIMARY KEY,
  source_id           TEXT NOT NULL REFERENCES source_objects(source_id),
  locator_type        TEXT NOT NULL,
  locator_start       TEXT,
  locator_end         TEXT,
  exact_text          TEXT,
  span_hash           TEXT,
  ordinal             INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS custody_events (
  custody_event_id    TEXT PRIMARY KEY,
  source_id           TEXT NOT NULL REFERENCES source_objects(source_id),
  prior_event_id      TEXT REFERENCES custody_events(custody_event_id),
  custodian_actor_id  TEXT REFERENCES actors(actor_id),
  started_at          TEXT,
  ended_at            TEXT,
  transfer_method     TEXT,
  integrity_check     TEXT,
  transformation      TEXT,
  prior_hash          TEXT,
  resulting_hash      TEXT,
  known_gap           TEXT,
  ordinal             INTEGER NOT NULL
);

-- Immutable family identity. Truth, admission, and grade never live here.
CREATE TABLE IF NOT EXISTS atoms (
  atom_id             TEXT PRIMARY KEY,
  object_type         TEXT NOT NULL CHECK (object_type IN
                         ('CLAIM','EVIDENCE','PROOF','PROCESS')),
  legacy_id           TEXT,
  atom_family         TEXT,
  created_at          TEXT NOT NULL,
  created_by_actor_id TEXT REFERENCES actors(actor_id),
  retired_at          TEXT,
  identity_note       TEXT,
  UNIQUE (legacy_id)
);

-- Optional canonical address; legacy objects may remain unresolved/unmigrated.
CREATE TABLE IF NOT EXISTS atom_addresses (
  address_id          TEXT PRIMARY KEY,
  atom_id             TEXT NOT NULL REFERENCES atoms(atom_id),
  address_text        TEXT NOT NULL,
  layer_code          TEXT,
  component_code      TEXT,
  parent_address_id   TEXT REFERENCES atom_addresses(address_id),
  child_role          TEXT,
  ordinal             INTEGER,
  resolver_version    TEXT NOT NULL,
  migration_state     TEXT NOT NULL DEFAULT 'UNMIGRATED',
  is_current          INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
  UNIQUE (address_text, resolver_version)
);

-- Version rows are immutable after sealed=1. A new material state is a new row.
CREATE TABLE IF NOT EXISTS atom_versions (
  atom_version_id             TEXT PRIMARY KEY,
  atom_id                     TEXT NOT NULL REFERENCES atoms(atom_id),
  version                     TEXT NOT NULL,
  schema_id                   TEXT NOT NULL REFERENCES schema_registry(schema_id),
  content_hash                TEXT NOT NULL,
  raw_statement               TEXT,
  statement_technical         TEXT,
  statement_plain             TEXT,
  scope_text                  TEXT,
  formalization_boundary      TEXT,
  lifecycle_state             TEXT NOT NULL,
  proof_class                 TEXT NOT NULL,
  register_code               TEXT NOT NULL,
  ic_grade                    TEXT,
  why_outcome                 TEXT,
  completion_state            TEXT NOT NULL DEFAULT 'DISCOVERY_INCOMPLETE',
  terminus_type               TEXT CHECK (terminus_type IS NULL OR terminus_type IN
                                   ('PRIMITIVE','INDEPENDENT_EMPIRICAL_INPUT','OPEN')),
  legacy_proof_label          TEXT,
  one_axiom_classification    TEXT,
  inherited_labels_json       TEXT NOT NULL DEFAULT '[]',
  emergent_labels_json        TEXT NOT NULL DEFAULT '[]',
  unresolved_json             TEXT NOT NULL DEFAULT '[]',
  legacy_payload_json         TEXT,
  created_at                  TEXT NOT NULL,
  created_by_actor_id         TEXT REFERENCES actors(actor_id),
  prior_atom_version_id       TEXT REFERENCES atom_versions(atom_version_id),
  sealed                      INTEGER NOT NULL DEFAULT 0 CHECK (sealed IN (0,1)),
  UNIQUE (atom_id, version)
);

CREATE TRIGGER IF NOT EXISTS sealed_atom_version_no_update
BEFORE UPDATE ON atom_versions
WHEN OLD.sealed = 1
BEGIN
  SELECT RAISE(ABORT, 'sealed atom versions are immutable; create a successor version');
END;

CREATE TRIGGER IF NOT EXISTS sealed_atom_version_no_delete
BEFORE DELETE ON atom_versions
WHEN OLD.sealed = 1
BEGIN
  SELECT RAISE(ABORT, 'sealed atom versions cannot be deleted');
END;

CREATE TABLE IF NOT EXISTS atom_version_sources (
  atom_version_id     TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  source_id           TEXT NOT NULL REFERENCES source_objects(source_id),
  span_id             TEXT REFERENCES source_spans(span_id),
  source_role         TEXT NOT NULL,
  author_or_witness   TEXT,
  date_received       TEXT,
  ai_contribution_declared TEXT,
  ordinal             INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (atom_version_id, source_id, source_role, ordinal)
);

-- Repeated envelope values that require identity, ordering, or independent review.
CREATE TABLE IF NOT EXISTS atom_items (
  item_id             TEXT PRIMARY KEY,
  atom_version_id     TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  item_kind           TEXT NOT NULL,
  ordinal             INTEGER NOT NULL DEFAULT 0,
  item_text           TEXT,
  item_json           TEXT NOT NULL DEFAULT '{}',
  item_hash           TEXT,
  review_state        TEXT NOT NULL DEFAULT 'UNREVIEWED',
  UNIQUE (atom_version_id, item_kind, ordinal)
);

-- CLAIM extension
CREATE TABLE IF NOT EXISTS claim_extensions (
  atom_version_id     TEXT PRIMARY KEY REFERENCES atom_versions(atom_version_id),
  register_anatomy_json TEXT NOT NULL DEFAULT '{}',
  truth_conditions_json TEXT NOT NULL DEFAULT '[]',
  quantifiers_json    TEXT NOT NULL DEFAULT '[]',
  exact_negations_json TEXT NOT NULL DEFAULT '[]',
  boundary_conditions_json TEXT NOT NULL DEFAULT '[]',
  identity_conditions_json TEXT NOT NULL DEFAULT '[]'
);

-- EVIDENCE extension
CREATE TABLE IF NOT EXISTS evidence_extensions (
  atom_version_id     TEXT PRIMARY KEY REFERENCES atom_versions(atom_version_id),
  protocol_text       TEXT,
  conditions_json     TEXT NOT NULL DEFAULT '[]',
  raw_record_source_id TEXT REFERENCES source_objects(source_id),
  discrimination_statement TEXT,
  limitations_json    TEXT NOT NULL DEFAULT '[]',
  completion_failure_state TEXT
);

CREATE TABLE IF NOT EXISTS derived_artifacts (
  artifact_id         TEXT PRIMARY KEY,
  evidence_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  source_id           TEXT NOT NULL REFERENCES source_objects(source_id),
  parent_artifact_id  TEXT REFERENCES derived_artifacts(artifact_id),
  process_version_id  TEXT,
  parameters_json     TEXT NOT NULL DEFAULT '{}',
  operator_actor_id   TEXT REFERENCES actors(actor_id),
  output_hash         TEXT NOT NULL,
  information_removed TEXT,
  information_added  TEXT,
  reversibility      TEXT,
  restoration_path   TEXT,
  validation_state   TEXT NOT NULL DEFAULT 'UNREVIEWED'
);

CREATE TABLE IF NOT EXISTS evidence_controls (
  control_id          TEXT PRIMARY KEY,
  evidence_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  control_type        TEXT NOT NULL,
  preregistered_at    TEXT,
  expected_result     TEXT,
  observed_result     TEXT,
  result_state        TEXT NOT NULL DEFAULT 'NOT_RUN',
  receipt_id          TEXT,
  limitations         TEXT
);

CREATE TABLE IF NOT EXISTS independence_clusters (
  cluster_id          TEXT PRIMARY KEY,
  cluster_name        TEXT NOT NULL,
  common_cause_type   TEXT NOT NULL,
  common_cause_description TEXT NOT NULL,
  assessment_method   TEXT,
  metadata_json       TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS evidence_independence (
  evidence_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  cluster_id          TEXT NOT NULL REFERENCES independence_clusters(cluster_id),
  dependence_dimension TEXT NOT NULL,
  dependence_strength TEXT,
  rationale           TEXT,
  PRIMARY KEY (evidence_atom_version_id, cluster_id, dependence_dimension)
);

-- PROOF extension
CREATE TABLE IF NOT EXISTS proof_extensions (
  atom_version_id     TEXT PRIMARY KEY REFERENCES atom_versions(atom_version_id),
  specification       TEXT,
  formal_statement    TEXT NOT NULL,
  conclusion_atom_version_id TEXT REFERENCES atom_versions(atom_version_id),
  interpretation_boundary TEXT NOT NULL,
  receipt_class       TEXT NOT NULL,
  what_checked_json   TEXT NOT NULL DEFAULT '[]',
  what_not_proved_json TEXT NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS proof_premises (
  proof_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  premise_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  premise_role        TEXT NOT NULL,
  premise_class       TEXT NOT NULL,
  ordinal             INTEGER NOT NULL,
  is_load_bearing     INTEGER NOT NULL DEFAULT 1 CHECK (is_load_bearing IN (0,1)),
  PRIMARY KEY (proof_atom_version_id, ordinal)
);

CREATE TABLE IF NOT EXISTS proof_steps (
  proof_step_id       TEXT PRIMARY KEY,
  proof_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  ordinal             INTEGER NOT NULL,
  inference_license   TEXT NOT NULL,
  input_refs_json     TEXT NOT NULL DEFAULT '[]',
  output_ref          TEXT,
  step_text           TEXT NOT NULL,
  verification_state  TEXT NOT NULL DEFAULT 'UNVERIFIED',
  UNIQUE (proof_atom_version_id, ordinal)
);

CREATE TABLE IF NOT EXISTS proof_assumptions (
  assumption_id       TEXT PRIMARY KEY,
  proof_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  assumption_class    TEXT NOT NULL,
  statement           TEXT NOT NULL,
  source_ref          TEXT,
  formulation_only    INTEGER NOT NULL DEFAULT 0 CHECK (formulation_only IN (0,1)),
  sensitivity         TEXT,
  ordinal             INTEGER NOT NULL
);

-- PROCESS extension and immutable process version contract
CREATE TABLE IF NOT EXISTS process_extensions (
  atom_version_id     TEXT PRIMARY KEY REFERENCES atom_versions(atom_version_id),
  purpose             TEXT NOT NULL,
  inputs_json         TEXT NOT NULL DEFAULT '[]',
  preconditions_json  TEXT NOT NULL DEFAULT '[]',
  outputs_json        TEXT NOT NULL DEFAULT '[]',
  discriminating_power TEXT NOT NULL,
  cannot_distinguish  TEXT NOT NULL,
  process_version     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS process_steps (
  process_step_id     TEXT PRIMARY KEY,
  process_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  ordinal             INTEGER NOT NULL,
  step_type           TEXT NOT NULL,
  step_text           TEXT NOT NULL,
  reads_json          TEXT NOT NULL DEFAULT '[]',
  writes_json         TEXT NOT NULL DEFAULT '[]',
  preserves_json      TEXT NOT NULL DEFAULT '[]',
  decision_actor_type TEXT,
  UNIQUE (process_atom_version_id, ordinal)
);

CREATE TABLE IF NOT EXISTS process_failure_modes (
  failure_mode_id     TEXT PRIMARY KEY,
  process_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  failure_code        TEXT NOT NULL,
  description         TEXT NOT NULL,
  detection           TEXT NOT NULL,
  safe_halt_behavior  TEXT NOT NULL,
  preserved_artifacts TEXT,
  recovery_path       TEXT,
  false_success_risk  TEXT
);

CREATE TABLE IF NOT EXISTS process_runs (
  run_id              TEXT PRIMARY KEY,
  process_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  started_at          TEXT NOT NULL,
  ended_at            TEXT,
  operator_actor_id   TEXT REFERENCES actors(actor_id),
  configuration_json  TEXT NOT NULL DEFAULT '{}',
  environment_json    TEXT NOT NULL DEFAULT '{}',
  input_refs_json     TEXT NOT NULL DEFAULT '[]',
  input_hashes_json   TEXT NOT NULL DEFAULT '[]',
  step_outcomes_json  TEXT NOT NULL DEFAULT '[]',
  warnings_json       TEXT NOT NULL DEFAULT '[]',
  deviations_json     TEXT NOT NULL DEFAULT '[]',
  output_refs_json    TEXT NOT NULL DEFAULT '[]',
  output_hashes_json  TEXT NOT NULL DEFAULT '[]',
  exit_state          TEXT NOT NULL,
  establishes         TEXT NOT NULL,
  does_not_establish  TEXT NOT NULL
);

-- First-class typed relations. Identity is separate from versioned payload.
CREATE TABLE IF NOT EXISTS edges (
  edge_id             TEXT PRIMARY KEY,
  source_atom_id      TEXT NOT NULL REFERENCES atoms(atom_id),
  predicate           TEXT NOT NULL,
  target_atom_id      TEXT NOT NULL REFERENCES atoms(atom_id),
  created_at          TEXT NOT NULL,
  created_by_actor_id TEXT REFERENCES actors(actor_id),
  UNIQUE (source_atom_id, predicate, target_atom_id, edge_id)
);

CREATE TABLE IF NOT EXISTS edge_versions (
  edge_version_id     TEXT PRIMARY KEY,
  edge_id             TEXT NOT NULL REFERENCES edges(edge_id),
  version             TEXT NOT NULL,
  source_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  target_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  lifecycle_state     TEXT NOT NULL,
  warrant_metadata_json TEXT NOT NULL DEFAULT '{}',
  content_hash        TEXT NOT NULL,
  created_at          TEXT NOT NULL,
  created_by_actor_id TEXT REFERENCES actors(actor_id),
  prior_edge_version_id TEXT REFERENCES edge_versions(edge_version_id),
  sealed              INTEGER NOT NULL DEFAULT 0 CHECK (sealed IN (0,1)),
  UNIQUE (edge_id, version)
);

CREATE TRIGGER IF NOT EXISTS sealed_edge_version_no_update
BEFORE UPDATE ON edge_versions
WHEN OLD.sealed = 1
BEGIN
  SELECT RAISE(ABORT, 'sealed edge versions are immutable; create a successor version');
END;

CREATE TRIGGER IF NOT EXISTS sealed_edge_version_no_delete
BEFORE DELETE ON edge_versions
WHEN OLD.sealed = 1
BEGIN
  SELECT RAISE(ABORT, 'sealed edge versions cannot be deleted');
END;

CREATE TABLE IF NOT EXISTS evidence_edge_payloads (
  edge_version_id     TEXT PRIMARY KEY REFERENCES edge_versions(edge_version_id),
  direction_state     TEXT NOT NULL CHECK (direction_state IN
                         ('SUPPORTS','CONTRADICTS','FALSIFIES','TESTS')),
  discrimination_statement TEXT NOT NULL,
  rival_or_negation   TEXT NOT NULL,
  expected_if_claim   TEXT,
  expected_if_rival   TEXT,
  observed_feature    TEXT,
  comparison_rule     TEXT,
  conditions_json     TEXT NOT NULL DEFAULT '[]',
  independence_cluster_id TEXT REFERENCES independence_clusters(cluster_id),
  weight_method       TEXT,
  weight_value        TEXT,
  uncertainty         TEXT,
  kill_condition_id   TEXT,
  reviewer_ruling_id  TEXT
);

CREATE TABLE IF NOT EXISTS proof_edge_payloads (
  edge_version_id     TEXT PRIMARY KEY REFERENCES edge_versions(edge_version_id),
  proof_relation      TEXT NOT NULL CHECK (proof_relation IN ('PROVES','DERIVED_FROM')),
  premise_role        TEXT,
  proof_receipt_id    TEXT,
  exact_statement_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS process_edge_payloads (
  edge_version_id     TEXT PRIMARY KEY REFERENCES edge_versions(edge_version_id),
  process_relation    TEXT NOT NULL CHECK (process_relation IN ('GENERATED_BY','AUDITED_BY')),
  process_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  run_id              TEXT NOT NULL REFERENCES process_runs(run_id)
);

CREATE TABLE IF NOT EXISTS bridge_edge_payloads (
  edge_version_id     TEXT PRIMARY KEY REFERENCES edge_versions(edge_version_id),
  source_register     TEXT NOT NULL,
  target_register     TEXT NOT NULL,
  forward_mapping_json TEXT NOT NULL,
  reverse_mapping_json TEXT,
  reverse_map_kind    TEXT NOT NULL,
  preserved_structure_json TEXT NOT NULL,
  lost_structure_json TEXT NOT NULL,
  boundary_conditions_json TEXT NOT NULL,
  bridge_grade        TEXT NOT NULL,
  ic_grade            TEXT,
  why_outcome         TEXT NOT NULL,
  next_test           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bridge_tests (
  bridge_test_id      TEXT PRIMARY KEY,
  edge_version_id     TEXT NOT NULL REFERENCES edge_versions(edge_version_id),
  test_type           TEXT NOT NULL,
  preregistration_receipt_id TEXT,
  expected_result     TEXT,
  observed_result     TEXT,
  verdict             TEXT NOT NULL,
  receipt_id          TEXT,
  ordinal             INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bridge_rivals (
  rival_id            TEXT PRIMARY KEY,
  edge_version_id     TEXT NOT NULL REFERENCES edge_versions(edge_version_id),
  rival_name          TEXT NOT NULL,
  mapping_json        TEXT NOT NULL,
  preserved_json      TEXT NOT NULL DEFAULT '[]',
  lost_json           TEXT NOT NULL DEFAULT '[]',
  result              TEXT,
  ordinal             INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS why_gate_records (
  why_record_id       TEXT PRIMARY KEY,
  edge_version_id     TEXT REFERENCES edge_versions(edge_version_id),
  atom_version_id     TEXT REFERENCES atom_versions(atom_version_id),
  outcome             TEXT NOT NULL CHECK (outcome IN ('WHY_CLOSED','WHY_FAILED','WHY_OPEN')),
  closure_level       TEXT,
  non_restatement_pass INTEGER CHECK (non_restatement_pass IN (0,1)),
  explanation_types_json TEXT NOT NULL DEFAULT '[]',
  ladder_levels_json  TEXT NOT NULL DEFAULT '[]',
  next_discriminating_test TEXT,
  CHECK ((edge_version_id IS NOT NULL) <> (atom_version_id IS NOT NULL))
);

-- Discovery, truth space, gauntlet, and explicit open knowledge.
CREATE TABLE IF NOT EXISTS invariant_signatures (
  signature_id        TEXT PRIMARY KEY,
  atom_version_id     TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  anonymized          INTEGER NOT NULL DEFAULT 0 CHECK (anonymized IN (0,1)),
  identities_json     TEXT NOT NULL DEFAULT '[]',
  distinctions_json   TEXT NOT NULL DEFAULT '[]',
  relations_json      TEXT NOT NULL DEFAULT '[]',
  operations_json     TEXT NOT NULL DEFAULT '[]',
  dependencies_json   TEXT NOT NULL DEFAULT '[]',
  constraints_json    TEXT NOT NULL DEFAULT '[]',
  invariants_json     TEXT NOT NULL DEFAULT '[]',
  collapse_conditions_json TEXT NOT NULL DEFAULT '[]',
  consequences_json   TEXT NOT NULL DEFAULT '[]',
  deblinding_key_hash TEXT
);

CREATE TABLE IF NOT EXISTS countermodels (
  countermodel_id     TEXT PRIMARY KEY,
  target_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  refuted_statement   TEXT NOT NULL,
  construction       TEXT NOT NULL,
  assumptions_json   TEXT NOT NULL DEFAULT '[]',
  minimal_failing_feature TEXT,
  receipt_id          TEXT,
  repair_options_json TEXT NOT NULL DEFAULT '[]',
  retained_after_successor INTEGER NOT NULL DEFAULT 1 CHECK (retained_after_successor IN (0,1))
);

CREATE TABLE IF NOT EXISTS kill_conditions (
  kill_condition_id   TEXT PRIMARY KEY,
  target_atom_version_id TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  condition_text      TEXT NOT NULL,
  blast_radius        TEXT,
  preregistered_at    TEXT,
  preregistration_receipt_id TEXT,
  state               TEXT NOT NULL DEFAULT 'OPEN',
  fired_by_evidence_atom_version_id TEXT REFERENCES atom_versions(atom_version_id),
  ruling_id           TEXT
);

CREATE TABLE IF NOT EXISTS open_items (
  open_item_id        TEXT PRIMARY KEY,
  atom_version_id     TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  exact_question      TEXT NOT NULL,
  candidates_json     TEXT NOT NULL DEFAULT '[]',
  evidence_json       TEXT NOT NULL DEFAULT '[]',
  failed_attempts_json TEXT NOT NULL DEFAULT '[]',
  next_discriminating_test TEXT NOT NULL,
  downstream_affected_json TEXT NOT NULL DEFAULT '[]',
  state               TEXT NOT NULL DEFAULT 'OPEN'
);

-- Generic reproducibility and review receipts.
CREATE TABLE IF NOT EXISTS receipts (
  receipt_id          TEXT PRIMARY KEY,
  receipt_type        TEXT NOT NULL,
  subject_kind        TEXT NOT NULL,
  subject_id          TEXT NOT NULL,
  subject_hash        TEXT,
  repository_revision TEXT,
  source_file         TEXT,
  theorem_or_entrypoint TEXT,
  toolchain_json      TEXT NOT NULL DEFAULT '{}',
  command_text        TEXT,
  exit_code           INTEGER,
  warning_count       INTEGER,
  admission_count     INTEGER,
  runtime_environment_json TEXT NOT NULL DEFAULT '{}',
  operator_actor_id   TEXT REFERENCES actors(actor_id),
  started_at          TEXT,
  finished_at         TEXT,
  what_checked_json   TEXT NOT NULL DEFAULT '[]',
  what_not_proved_json TEXT NOT NULL DEFAULT '[]',
  output_hash         TEXT,
  body_json           TEXT NOT NULL DEFAULT '{}'
);

-- Candidate and admitted are distinct graph memberships, never a Boolean truth flag.
CREATE TABLE IF NOT EXISTS graph_memberships (
  membership_id       TEXT PRIMARY KEY,
  atom_version_id     TEXT NOT NULL REFERENCES atom_versions(atom_version_id),
  graph_name          TEXT NOT NULL CHECK (graph_name IN ('CANDIDATE','ADMITTED')),
  state               TEXT NOT NULL,
  effective_from      TEXT NOT NULL,
  effective_to        TEXT,
  ruling_id           TEXT,
  UNIQUE (atom_version_id, graph_name, effective_from)
);

CREATE TABLE IF NOT EXISTS rulings (
  ruling_id           TEXT PRIMARY KEY,
  target_kind         TEXT NOT NULL,
  target_id           TEXT NOT NULL,
  action              TEXT NOT NULL CHECK (action IN
                         ('ADMIT','RETURN','CORRECT','WEAKEN','WITHDRAW','REJECT','DEFER','MODIFY')),
  ruler_actor_id      TEXT NOT NULL REFERENCES actors(actor_id),
  authority_scope     TEXT NOT NULL,
  ruled_at            TEXT NOT NULL,
  rationale           TEXT NOT NULL,
  dissent_or_open_issue TEXT,
  effective_graph_state TEXT NOT NULL,
  packet_hash         TEXT,
  receipt_id          TEXT
);

CREATE TABLE IF NOT EXISTS corrections (
  correction_id       TEXT PRIMARY KEY,
  target_kind         TEXT NOT NULL CHECK (target_kind IN ('ATOM_VERSION','EDGE_VERSION')),
  target_id           TEXT NOT NULL,
  defect_class        TEXT NOT NULL CHECK (defect_class IN
                         ('LOCAL_DEFINITE_FIX','SUBSTANTIVE_CORRECTION','WITHDRAWAL','RECLASSIFICATION')),
  defect_statement    TEXT NOT NULL,
  evidence_refs_json  TEXT NOT NULL DEFAULT '[]',
  proposed_text_or_action TEXT NOT NULL,
  proposed_payload_hash TEXT,
  staged_diff         TEXT,
  state               TEXT NOT NULL DEFAULT 'PROPOSED',
  ruling_id           TEXT REFERENCES rulings(ruling_id),
  restoration_path   TEXT NOT NULL,
  receipt_id          TEXT,
  created_at          TEXT NOT NULL,
  created_by_actor_id TEXT REFERENCES actors(actor_id)
);

CREATE TABLE IF NOT EXISTS correction_impacts (
  correction_id       TEXT NOT NULL REFERENCES corrections(correction_id),
  downstream_kind     TEXT NOT NULL,
  downstream_id       TEXT NOT NULL,
  impact_state        TEXT NOT NULL CHECK (impact_state IN
                         ('UNAFFECTED','REVIEW_REQUIRED','WEAKENED','UPSTREAM_FALSIFIED',
                          'PROJECTION_REBUILD_REQUIRED','RERUN_OWED')),
  rationale           TEXT,
  ordinal             INTEGER NOT NULL,
  PRIMARY KEY (correction_id, downstream_kind, downstream_id)
);

CREATE TABLE IF NOT EXISTS projections (
  projection_id       TEXT PRIMARY KEY,
  atom_version_id     TEXT REFERENCES atom_versions(atom_version_id),
  edge_version_id     TEXT REFERENCES edge_versions(edge_version_id),
  projection_type     TEXT NOT NULL,
  generator_process_version_id TEXT REFERENCES atom_versions(atom_version_id),
  generator_run_id    TEXT REFERENCES process_runs(run_id),
  output_uri          TEXT NOT NULL,
  output_hash         TEXT NOT NULL,
  generated_at        TEXT NOT NULL,
  is_current          INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
  CHECK ((atom_version_id IS NOT NULL) <> (edge_version_id IS NOT NULL))
);

CREATE INDEX IF NOT EXISTS idx_atom_versions_atom ON atom_versions(atom_id, created_at);
CREATE INDEX IF NOT EXISTS idx_atom_versions_axes ON atom_versions(lifecycle_state, proof_class, register_code);
CREATE INDEX IF NOT EXISTS idx_atom_addresses_atom ON atom_addresses(atom_id, is_current);
CREATE INDEX IF NOT EXISTS idx_atom_items_kind ON atom_items(atom_version_id, item_kind, ordinal);
CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_atom_id, predicate);
CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_atom_id, predicate);
CREATE INDEX IF NOT EXISTS idx_edge_versions_edge ON edge_versions(edge_id, created_at);
CREATE INDEX IF NOT EXISTS idx_kill_conditions_target ON kill_conditions(target_atom_version_id, state);
CREATE INDEX IF NOT EXISTS idx_open_items_target ON open_items(atom_version_id, state);
CREATE INDEX IF NOT EXISTS idx_receipts_subject ON receipts(subject_kind, subject_id);
CREATE INDEX IF NOT EXISTS idx_corrections_target ON corrections(target_kind, target_id, state);
CREATE INDEX IF NOT EXISTS idx_graph_memberships_active ON graph_memberships(graph_name, state, effective_to);

CREATE VIEW IF NOT EXISTS current_atom_versions AS
SELECT av.*
FROM atom_versions av
WHERE NOT EXISTS (
  SELECT 1 FROM atom_versions newer
  WHERE newer.prior_atom_version_id = av.atom_version_id
);

CREATE VIEW IF NOT EXISTS candidate_graph_atoms AS
SELECT av.*, gm.state AS membership_state
FROM current_atom_versions av
JOIN graph_memberships gm ON gm.atom_version_id = av.atom_version_id
WHERE gm.graph_name = 'CANDIDATE' AND gm.effective_to IS NULL;

CREATE VIEW IF NOT EXISTS admitted_graph_atoms AS
SELECT av.*, gm.state AS membership_state
FROM current_atom_versions av
JOIN graph_memberships gm ON gm.atom_version_id = av.atom_version_id
WHERE gm.graph_name = 'ADMITTED' AND gm.effective_to IS NULL;

CREATE VIEW IF NOT EXISTS unresolved_canon_work AS
SELECT av.atom_version_id, av.atom_id, av.version,
       av.lifecycle_state, av.proof_class, av.register_code,
       av.why_outcome, av.completion_state,
       (SELECT COUNT(*) FROM open_items oi
        WHERE oi.atom_version_id = av.atom_version_id AND oi.state = 'OPEN') AS open_item_count,
       (SELECT COUNT(*) FROM kill_conditions kc
        WHERE kc.target_atom_version_id = av.atom_version_id AND kc.state = 'OPEN') AS open_kill_condition_count
FROM current_atom_versions av
WHERE av.completion_state <> 'FULLY_OPENED'
   OR av.why_outcome = 'WHY_OPEN'
   OR EXISTS (SELECT 1 FROM open_items oi
              WHERE oi.atom_version_id = av.atom_version_id AND oi.state = 'OPEN');

-- Seed vocabularies are registries for UI and validation. They do not assign
-- any term to any atom and do not migrate legacy values automatically.
INSERT OR IGNORE INTO controlled_terms VALUES
  ('object_type','CLAIM','Claim','Asserts one independently gradable proposition.','1.1',NULL,1),
  ('object_type','EVIDENCE','Evidence','Preserved record that discriminates among claims or rivals.','1.1',NULL,2),
  ('object_type','PROOF','Proof','Inspectable derivation from named premises to one exact conclusion.','1.1',NULL,3),
  ('object_type','PROCESS','Process','Versioned operation that generates, transforms, audits, or tests.','1.1',NULL,4),

  ('lifecycle','RAW','Raw','Received but not yet preserved or decomposed.','1.1',NULL,1),
  ('lifecycle','PRESERVED','Preserved','Source bytes, location, span, and hash retained.','1.1',NULL,2),
  ('lifecycle','DECOMPOSED','Decomposed','Independently failing components separated.','1.1',NULL,3),
  ('lifecycle','OPENED','Opened','Native burdens and dependencies exposed.','1.1',NULL,4),
  ('lifecycle','TESTED','Tested','At least one declared test has been executed.','1.1',NULL,5),
  ('lifecycle','CANDIDATE','Candidate','Eligible for human review; not admitted.','1.1',NULL,6),
  ('lifecycle','HUMAN_REVIEW','Human review','Currently before an authorized human ruler.','1.1',NULL,7),
  ('lifecycle','ADMITTED','Admitted','Explicitly admitted under a recorded ruling.','1.1',NULL,8),
  ('lifecycle','RETURNED','Returned','Returned for revision or missing work.','1.1',NULL,9),
  ('lifecycle','WITHDRAWN','Withdrawn','Removed from current use while history remains.','1.1',NULL,10),
  ('lifecycle','FALSIFIED','Falsified','A valid kill condition or refutation fired.','1.1',NULL,11),
  ('lifecycle','SUPERSEDED','Superseded','A successor is current; this version remains resolvable.','1.1',NULL,12),
  ('lifecycle','DEPRECATED','Deprecated','Retained but discouraged for new use.','1.1',NULL,13),

  ('proof_class','NOT_ATTEMPTED','Not attempted','No formal or proof-theoretic attempt recorded.','1.1',NULL,1),
  ('proof_class','SPECIFICATION_ONLY','Specification only','A formal-looking specification without a completed derivation.','1.1',NULL,2),
  ('proof_class','INFORMAL_ARGUMENT','Informal argument','Discursive reasoning, not kernel verification.','1.1',NULL,3),
  ('proof_class','FORMALIZED_NOT_BUILT','Formalized not built','Encoded source exists but has no passing build receipt.','1.1',NULL,4),
  ('proof_class','BUILT_WITH_ASSUMPTIONS','Built with assumptions','Build passes with material declared assumptions.','1.1',NULL,5),
  ('proof_class','BUILT_WITH_SORRY','Built with sorry','Build accepts admissions or sorry placeholders.','1.1',NULL,6),
  ('proof_class','BUILT_ZERO_SORRY','Built zero sorry','Build receipt reports no sorry/admission holes.','1.1',NULL,7),
  ('proof_class','COUNTERMODEL_FOUND','Countermodel found','A model refutes the overstrong target statement.','1.1',NULL,8),
  ('proof_class','FALSIFIED','Falsified','The exact claim has been refuted under its stated burden.','1.1',NULL,9),

  ('register','FORMAL','Formal or mathematical','Formal, mathematical, or proof-theoretic assertion.','1.1',NULL,1),
  ('register','EMPIRICAL','Empirical or physical','Measurement or physical-world assertion.','1.1',NULL,2),
  ('register','HISTORICAL','Historical','Event, witness, transmission, or documentary assertion.','1.1',NULL,3),
  ('register','INFORMATIONAL','Informational','Information-theoretic assertion.','1.1',NULL,4),
  ('register','CONSCIOUSNESS','Consciousness or first-person','First-person or consciousness assertion.','1.1',NULL,5),
  ('register','MORAL','Moral or normative','Normative, moral, or duty-bearing assertion.','1.1',NULL,6),
  ('register','THEOLOGICAL','Theological or confessional','Scriptural, doctrinal, or confessional assertion.','1.1',NULL,7),
  ('register','BRIDGE','Bridge or cross-register','Mapping or interpretation connecting distinct registers.','1.1',NULL,8),
  ('register','INTERPRETIVE','Interpretive','Meaning assignment without proof transfer.','1.1',NULL,9),
  ('register','PREDICTIVE','Predictive','Forward prediction with declared conditions.','1.1',NULL,10),
  ('register','PROTOCOL','Protocol','Method or procedure burden.','1.1',NULL,11),

  ('ic_grade','IC-0','IC-0','Vocabulary proximity only.','1.1',NULL,0),
  ('ic_grade','IC-1','IC-1','Local feature correspondence; relations mostly unspecified.','1.1',NULL,1),
  ('ic_grade','IC-2','IC-2','Multiple explicit relations; dependencies or operations incomplete.','1.1',NULL,2),
  ('ic_grade','IC-3','IC-3','Substantial correspondence; rivals or collapse behavior insufficient.','1.1',NULL,3),
  ('ic_grade','IC-4','IC-4','Shared dependency and capability structure with losses named.','1.1',NULL,4),
  ('ic_grade','IC-5','IC-5','IC-4 plus matched collapse/translation behavior surviving controls.','1.1',NULL,5),

  ('why_outcome','WHY_CLOSED','Why closed','Applicable why-ladder levels close with non-restatement.','1.1',NULL,1),
  ('why_outcome','WHY_FAILED','Why failed','Offered explanation collapses, conflicts, or loses to a rival.','1.1',NULL,2),
  ('why_outcome','WHY_OPEN','Why open','Correspondence may remain while explanation is underdetermined.','1.1',NULL,3),

  ('terminus','PRIMITIVE','Primitive','Declared model, logical, methodological, or theological floor.','1.1',NULL,1),
  ('terminus','INDEPENDENT_EMPIRICAL_INPUT','Independent empirical input','Observed input used but not derived.','1.1',NULL,2),
  ('terminus','OPEN','Open','Unresolved dependency, rival, mechanism, or test.','1.1',NULL,3),

  ('graph','CANDIDATE','Candidate graph','Proposed or automated structure awaiting human admission.','1.1',NULL,1),
  ('graph','ADMITTED','Admitted graph','Only explicitly human-admitted current structure.','1.1',NULL,2);

COMMIT;
