import { useState, useRef, useCallback } from "react";

// ─── Hieroglyphs: the classification symbols ───
const GLYPHS = {
  axiom: "𝔸", claim: "ℂ", equation: "∑", variable: "χ",
  proof: "∎", law: "⚖", mirror: "⟷",
  generates: "↓", depends: "→", grounds: "⊢",
  contains: "∈", proves: "∴", derives: "⊳",
  defines: "≜", mirror_edge: "≅",
};

const GRADE_BG = { A: "#22c55e", B: "#3b82f6", C: "#f59e0b", D: "#ef4444", "—": "#6b7280" };
const GRADE_FG = { A: "#052e16", B: "#0a1628", C: "#1a0e00", D: "#1a0000", "—": "#1a1a1a" };
const TYPE_COLORS = { axiom:"#e8a838", claim:"#6d9cff", equation:"#c084fc", variable:"#34d399", proof:"#22c55e", law:"#f97316", mirror:"#ec4899" };

// ─── Atom data with CONTENT inside each block ───
const ATOMS = [
  { id: "GOD", symbol: "G∞", name: "God", type: "axiom", grade: "—", row: 0, col: 4,
    claims: ["Something exists rather than nothing", "The ground must ground itself (A2.2)", "Self-referential Mind is the starting point"],
    evidence: ["Münchhausen Trilemma: every proof ends circular, regress, or dogmatic", "Parity argument: all systems have a root axiom", "No brute facts under theism"],
    kills: ["Construct a model where consciousness arises without any ground", "Show self-grounding is logically incoherent"] },

  { id: "G01", symbol: "Gσ", name: "Self-Ground", type: "claim", grade: "C", row: 1, col: 0,
    claims: ["G must be its own explanation", "Fixed point of the grounding operator: Λ = G(Λ)"],
    evidence: ["Banach contraction: unique fixed point (FINAL-1)", "No infinite regress if ground is self-explanatory"],
    kills: ["Show self-grounding is circular in a vicious (not virtuous) way"] },

  { id: "G06", symbol: "G⊤", name: "Perfection", type: "claim", grade: "C", row: 1, col: 4,
    claims: ["Maximal coherence = perfection", "G is the ceiling of every register"],
    evidence: ["All nine factors at 1 → chi = 1", "No internal contradiction at maximum"],
    kills: ["Show maximal coherence is unstable", "Find a state above chi = 1"] },

  { id: "G07", symbol: "G⊕", name: "Moral Nature", type: "claim", grade: "C", row: 1, col: 6,
    claims: ["G is necessarily moral", "Morality is not contingent feature but essential attribute"],
    evidence: ["Law 9 Noether: moral conservation is non-optional", "CP violation: sin is directional/irreversible"],
    kills: ["Derive moral indifference from the axioms", "Show moral nature is separable from self-knowledge"] },

  { id: "F01", symbol: "∃", name: "Existence", type: "claim", grade: "B", row: 2, col: 0,
    claims: ["Something exists rather than nothing", "Existence is not a brute fact under theism"],
    evidence: ["Leibniz: PSR requires explanation", "No brute facts if God is ground"],
    kills: ["Show nothingness is a stable state"] },

  { id: "F02", symbol: "𝕀", name: "Information", type: "claim", grade: "C", row: 2, col: 2,
    claims: ["Information is ontologically fundamental", "Not derived from matter — matter derived from information"],
    evidence: ["Wheeler: it from bit", "Landauer: information has physical cost", "Shannon Layer 0 of chi"],
    kills: ["Show information supervenes on matter without remainder"] },

  { id: "F03", symbol: "ℭ", name: "Coherence", type: "claim", grade: "C", row: 2, col: 4,
    claims: ["Reality requires order", "Coherence is not accidental but necessary"],
    evidence: ["Phase transition math identical at every scale", "5.7σ cross-domain correlation"],
    kills: ["Show coherence is epiphenomenal", "Produce order from pure randomness without selection"] },

  { id: "F05", symbol: "𝕎", name: "Agency", type: "claim", grade: "C", row: 2, col: 7,
    claims: ["Will is real, not illusory", "Agency = Ω, selection capacity"],
    evidence: ["Chaos as gain structure: small choice → large consequence", "EP-04: love requires the possibility of its absence"],
    kills: ["Show all behavior is fully determined by prior state"] },

  { id: "ME", symbol: "∏χ", name: "Master Equation", type: "equation", grade: "B", row: 3, col: 3,
    claims: ["χ = C_W[G·M·E·S_eff·T·K·R·Q·F·C]", "Product form, not additive", "Any zero collapses the whole (veto)", "Dimensionless ratios, bounded [0,1]"],
    evidence: ["Lean-verified: listProd_eq_zero_iff", "Lean-verified: chi_zero_if_any_factor_zero", "Product structure mirrors reliability engineering, AND gates, survival analysis"],
    kills: ["Show additive form produces equivalent veto", "Show product form is uniquely forced (upgrades 'chosen' to 'necessary')"] },

  { id: "CHI", symbol: "χ₀", name: "χ Properties", type: "claim", grade: "—", row: 3, col: 6,
    claims: ["Measurement instrument, not salvation variable", "Level 1 = snapshot, Level 2 = dynamics", "Wrapper C_W is not a tenth factor", "Free will lives in the derivative, not the snapshot"],
    evidence: ["Thermometer/heater distinction", "Config space vs phase space (physics)", "Sleeping saint has chi but exerts no will"],
    kills: ["Show chi at Level 1 has dynamics", "Show C_W cannot be identity"] },

  { id: "G_var", symbol: "G", name: "Negentropy", type: "variable", grade: "B", row: 4, col: 0,
    claims: ["External input that increases coherence", "Domain: [0, ∞)"],
    evidence: ["Maxwell's demon: external info injection", "Photosynthesis: sunlight drives order", "Battery charging: external current drives chemical order"],
    kills: ["Show coherence increases without external input in closed system"] },

  { id: "M_var", symbol: "M", name: "Alignment", type: "variable", grade: "B", row: 4, col: 1,
    claims: ["Cosine alignment with reference vector", "Domain: [-1, 1]"],
    evidence: ["Malus's law: I = I₀cos²θ", "Spin alignment in B field: E = -μ·B", "Antenna gain pattern"],
    kills: ["Show alignment is redundant with another factor"] },

  { id: "E_var", symbol: "E", name: "Fidelity", type: "variable", grade: "B", row: 4, col: 2,
    claims: ["Signal propagation fidelity", "Domain: [0, ∞)"],
    evidence: ["Shannon capacity C = B·log₂(1+S/N)", "DNA replication fidelity", "Fiber optic attenuation + repeaters"],
    kills: ["Show E is derivable from K (compression)"] },

  { id: "S_var", symbol: "S", name: "Entropy", type: "variable", grade: "B", row: 4, col: 3,
    claims: ["Entropy enters as SUPPRESSION: S_eff = e^(-αS)", "Domain: (0, 1]", "Antitone: more entropy → less contribution"],
    evidence: ["Boltzmann factor e^(-E/kT): same form", "Debye-Waller factor: disorder suppresses signal", "Survival probability S(t) = e^(-λt)"],
    kills: ["Show entropy should enter additively", "Find a system where more entropy increases coherence"] },

  { id: "T_var", symbol: "T", name: "Time", type: "variable", grade: "B", row: 4, col: 4,
    claims: ["Time as accumulator, not face", "Domain: (0, ∞)"],
    evidence: ["Impulse J = ∫F·dt", "Compound interest A = Pe^(rt)", "Dose = ∫(rate)·dt"],
    kills: ["Show time is a fourth face (overturns 'three faces not four' ruling)"] },

  { id: "K_var", symbol: "K", name: "Compression", type: "variable", grade: "B", row: 4, col: 5,
    claims: ["Kolmogorov complexity ratio", "Domain: [0, ∞)", "How much structure survives compression"],
    evidence: ["Crystal = low K (repeating, short description)", "Glass = high K (random, long description)", "Genetic code compression"],
    kills: ["Show K is derivable from E (fidelity)"] },

  { id: "R_var", symbol: "R", name: "Phase", type: "variable", grade: "B", row: 4, col: 6,
    claims: ["Binary phase transition indicator", "Domain: {0, 1}", "Irreversible state change"],
    evidence: ["First-order phase transitions", "Apoptosis: binary, irreversible", "Circuit breaker: trip once"],
    kills: ["Show R should be continuous, not binary"] },

  { id: "Q_var", symbol: "Q", name: "Superposition", type: "variable", grade: "B", row: 4, col: 7,
    claims: ["Unresolved possibility space", "Domain: [0, 1]"],
    evidence: ["Quantum superposition |ψ⟩ = α|0⟩ + β|1⟩", "Stem cell totipotency: undifferentiated = max Q", "Option value in finance"],
    kills: ["Show Q is redundant with F (correlation)"] },

  { id: "F_var", symbol: "F", name: "Correlation", type: "variable", grade: "B", row: 4, col: 8,
    claims: ["Non-local correlation strength", "Domain: [0, 1]"],
    evidence: ["Quantum entanglement: Bell inequality violation", "PEAR-LAB: 6.35σ consciousness-RNG correlation"],
    kills: ["Show F is derivable from Q", "Rule out all non-local effects experimentally"] },

  { id: "C_var", symbol: "C", name: "Integration", type: "variable", grade: "B", row: 4, col: 9,
    claims: ["Total integration measure", "Domain: [0, 1]", "How much system exceeds sum of parts"],
    evidence: ["IIT Φ: min mutual information across partition", "EEG coherence as Φ surrogate"],
    kills: ["Show integration is epiphenomenal to consciousness"] },

  { id: "VETO", symbol: "∎₀", name: "Zero Collapse", type: "proof", grade: "A", row: 5, col: 2,
    claims: ["Any factor = 0 implies χ = 0", "Product annihilation is the veto"],
    evidence: ["Lean: listProd_eq_zero_iff", "Lean: chi_zero_if_any_factor_zero", "Boolean AND gate: any 0 → 0"],
    kills: ["Find a model where one factor at zero doesn't collapse chi"] },

  { id: "GRACE_CHAIN", symbol: "∎→", name: "Grace Chain", type: "proof", grade: "A", row: 5, col: 4,
    claims: ["Grace → Faith → Hope → Salvation is ordered", "Without Grace, chain from zero yields zero"],
    evidence: ["Lean: graceChain compiles with no sorry", "Only grade-A atom in entire corpus"],
    kills: ["Show salvation without grace produces nonzero output"] },

  { id: "LAGRANGIAN", symbol: "ℒ", name: "Lagrangian", type: "proof", grade: "B", row: 5, col: 6,
    claims: ["Lowe Coherence Lagrangian is positive-definite", "Mass matrix verified", "Hamiltonian well-defined"],
    evidence: ["Python runtime: mass matrix eigenvalues all positive", "Hamiltonian derivation succeeds"],
    kills: ["Find negative eigenvalue in mass matrix", "Show Hamiltonian is unbounded below"] },

  { id: "L1", symbol: "⚖₁", name: "Newton-Grace", type: "law", grade: "B", row: 6, col: 0,
    claims: ["Gravitational mechanics maps onto sin/grace dynamics", "Stable orbit = grace path (angular momentum as gift)"],
    evidence: ["Schwarzschild collapse at r=0", "Orbital mechanics: escape vs capture"],
    kills: ["Show gravitational analogy breaks at quantitative level"] },

  { id: "L4", symbol: "⚖₄", name: "Yukawa-Agape", type: "law", grade: "B", row: 6, col: 2,
    claims: ["Strong force maps onto love/captivity", "Confinement increases with distance; freedom inside bond"],
    evidence: ["Cornell potential: V(r) = -α/r + k·r", "Asymptotic freedom at short range"],
    kills: ["Show love behaves as inverse-square, not confining"] },

  { id: "L5", symbol: "⚖₅", name: "Clausius-Judgment", type: "law", grade: "B", row: 6, col: 4,
    claims: ["Free energy maps onto justice/mercy", "Cross = unique point where J=1 AND M=1 simultaneously"],
    evidence: ["R(offense,α): α=1 justice, α=0 mercy, α=0+judge=payer = Cross", "F = E - TS: entropy cost of mercy"],
    kills: ["Find another point where J=1 and M=1 without external cost-bearer"] },

  { id: "L9", symbol: "⚖₉", name: "Fermi-Conservation", type: "law", grade: "B", row: 6, col: 7,
    claims: ["Weak force maps onto moral conservation", "CP violation: sin is directional (irreversible)", "Noether: moral energy is conserved"],
    evidence: ["Three-body decay: ψ → ψ_broken + δ + ν_loss", "Neutrino argument: books demand unseen participant"],
    kills: ["Find moral event where ledger closes without invisible remainder"] },

  { id: "L10", symbol: "⚖χ", name: "Coherence-Christ", type: "law", grade: "B", row: 6, col: 9,
    claims: ["C IS χ. Not symmetric.", "Coherence is sovereign, decoherence is derivative", "No internal duality, no free-will term"],
    evidence: ["Wrapper structure: C_W wraps product", "Veto: coherence at zero = everything at zero"],
    kills: ["Show decoherence is primitive, not derivative"] },

  { id: "ISO_LANG", symbol: "≅L", name: "Langevin", type: "mirror", grade: "L6", row: 7, col: 1,
    claims: ["dx/dt = -μ∇V + noise maps onto dX/dt = W∇χ + η", "Mobility μ ↔ Will W", "Landscape V ↔ χ landscape"],
    evidence: ["Same ODE form", "Same gradient structure", "Same external source"],
    kills: ["Named BREAK: Langevin noise is random; grace (η) is directed. Break IS the theology."] },

  { id: "ISO_BOLTZ", symbol: "≅B", name: "Boltzmann", type: "mirror", grade: "L6", row: 7, col: 3,
    claims: ["e^(-E/kT) has same form as S_eff = e^(-αS)", "Both: exponential suppression of disorder"],
    evidence: ["Identical functional form", "Both convert positive quantity to (0,1] fraction"],
    kills: ["Show the mapping is only formal, not structural"] },

  { id: "ISO_AND", symbol: "≅∧", name: "AND Gate", type: "mirror", grade: "L7", row: 7, col: 7,
    claims: ["Boolean AND = multiplicative veto", "Output = ∏ inputs; any 0 → 0"],
    evidence: ["Lean: listProd_eq_zero_iff already proved", "One definition bridges to Boolean"],
    kills: ["Show veto operates differently from AND in edge cases"] },
];

const EDGES = [
  { from: "GOD", to: "G01" }, { from: "GOD", to: "G06" }, { from: "GOD", to: "G07" },
  { from: "GOD", to: "F01" }, { from: "F01", to: "F02" }, { from: "F02", to: "F03" },
  { from: "F03", to: "F05" }, { from: "F02", to: "ME" }, { from: "F03", to: "ME" },
  { from: "G06", to: "ME" }, { from: "ME", to: "CHI" },
  { from: "ME", to: "G_var" }, { from: "ME", to: "M_var" }, { from: "ME", to: "E_var" },
  { from: "ME", to: "S_var" }, { from: "ME", to: "T_var" }, { from: "ME", to: "K_var" },
  { from: "ME", to: "R_var" }, { from: "ME", to: "Q_var" }, { from: "ME", to: "F_var" },
  { from: "ME", to: "C_var" },
  { from: "CHI", to: "VETO" }, { from: "G_var", to: "GRACE_CHAIN" },
  { from: "ME", to: "LAGRANGIAN" },
  { from: "ME", to: "L1" }, { from: "ME", to: "L4" }, { from: "ME", to: "L5" },
  { from: "ME", to: "L9" }, { from: "ME", to: "L10" },
  { from: "CHI", to: "ISO_LANG" }, { from: "S_var", to: "ISO_BOLTZ" },
  { from: "VETO", to: "ISO_AND" },
];

const COLS = 10;
const CELL_W = 105;
const CELL_H = 88;
const GAP = 6;
const PAD = 16;
const ROW_LABELS = ["GROUND", "GOD PROPERTIES", "FOUNDATIONS", "EQUATION", "VARIABLES", "PROOFS", "TEN LAWS", "PHYSICS MIRRORS"];

function getThread(ids) {
  const t = new Set();
  function up(id) { if (t.has(id)) return; t.add(id); EDGES.filter(e => e.to === id).forEach(e => up(e.from)); }
  function down(id) { if (t.has(id)) return; t.add(id); EDGES.filter(e => e.from === id).forEach(e => down(e.to)); }
  ids.forEach(id => { up(id); down(id); });
  return t;
}

function AtomBlock({ atom, isPinned, inThread, hasThread, isExpanded, onPin, onExpand }) {
  const bg = isPinned ? "#ef444420" : (inThread ? "#ffffff08" : "#0d0e16");
  const border = isPinned ? "#ef4444" : (GRADE_BG[atom.grade] || TYPE_COLORS[atom.type]);
  const opacity = hasThread ? (inThread ? 1 : 0.08) : 1;
  const glyph = GLYPHS[atom.type];

  return (
    <div
      onClick={(e) => { e.stopPropagation(); onPin(atom.id, e.shiftKey); }}
      onDoubleClick={(e) => { e.stopPropagation(); onExpand(atom.id); }}
      style={{
        position: "absolute",
        left: PAD + atom.col * (CELL_W + GAP),
        top: PAD + 20 + atom.row * (CELL_H + GAP + 6),
        width: CELL_W, minHeight: isExpanded ? "auto" : CELL_H,
        background: bg, border: `1.5px solid ${border}`,
        borderRadius: 6, padding: "6px 8px",
        opacity, cursor: "pointer", zIndex: isExpanded ? 100 : 1,
        transition: "all 0.2s ease",
        boxShadow: isPinned ? `0 0 16px ${border}40` : (inThread && hasThread ? `0 0 8px ${border}30` : "none"),
      }}
    >
      {/* Header row: glyph + symbol + grade */}
      <div style={{ display: "flex", alignItems: "center", gap: 4, marginBottom: 3 }}>
        <span style={{ fontSize: 11, color: TYPE_COLORS[atom.type], fontWeight: 700 }}>{glyph}</span>
        <span style={{ fontSize: 16, fontWeight: 800, color: "#e2e8f0", fontFamily: "monospace", letterSpacing: "-0.05em", flex: 1 }}>{atom.symbol}</span>
        <span style={{
          fontSize: 9, fontWeight: 800, padding: "1px 5px", borderRadius: 3,
          background: GRADE_BG[atom.grade], color: GRADE_FG[atom.grade],
        }}>{atom.grade}</span>
      </div>

      {/* Name */}
      <div style={{ fontSize: 10, color: "#94a3af", fontWeight: 500, marginBottom: 2 }}>{atom.name}</div>

      {/* Type badge */}
      <div style={{ fontSize: 7, color: TYPE_COLORS[atom.type], textTransform: "uppercase", letterSpacing: "0.08em", fontWeight: 700, marginBottom: isExpanded ? 6 : 0 }}>
        {atom.type}
      </div>

      {/* Expanded content */}
      {isExpanded && (
        <div style={{ borderTop: `1px solid ${border}30`, paddingTop: 6, marginTop: 4 }}>
          {atom.claims.length > 0 && (
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontSize: 8, color: "#22c55e", fontWeight: 700, letterSpacing: "0.06em", marginBottom: 2 }}>ℂ CLAIMS</div>
              {atom.claims.map((c, i) => (
                <div key={i} style={{ fontSize: 10, color: "#c8ccd4", padding: "2px 0", paddingLeft: 8, borderLeft: "2px solid #22c55e30", marginBottom: 2, lineHeight: 1.4 }}>{c}</div>
              ))}
            </div>
          )}
          {atom.evidence.length > 0 && (
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontSize: 8, color: "#6d9cff", fontWeight: 700, letterSpacing: "0.06em", marginBottom: 2 }}>∴ EVIDENCE</div>
              {atom.evidence.map((e, i) => (
                <div key={i} style={{ fontSize: 10, color: "#9ca3af", padding: "2px 0", paddingLeft: 8, borderLeft: "2px solid #6d9cff30", marginBottom: 2, lineHeight: 1.4 }}>{e}</div>
              ))}
            </div>
          )}
          {atom.kills.length > 0 && (
            <div>
              <div style={{ fontSize: 8, color: "#ef4444", fontWeight: 700, letterSpacing: "0.06em", marginBottom: 2 }}>✕ KILL CONDITIONS</div>
              {atom.kills.map((k, i) => (
                <div key={i} style={{ fontSize: 10, color: "#f8717180", padding: "2px 0", paddingLeft: 8, borderLeft: "2px solid #ef444430", marginBottom: 2, lineHeight: 1.4 }}>{k}</div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function PeriodicTable() {
  const [pinned, setPinned] = useState(new Set());
  const [expanded, setExpanded] = useState(new Set());
  const thread = pinned.size > 0 ? getThread([...pinned]) : null;

  const onPin = useCallback((id, shift) => {
    setPinned(prev => {
      const next = new Set(shift ? prev : []);
      if (prev.has(id) && !shift) { next.delete(id); }
      else if (prev.has(id) && shift) {
        // Shift+click pinned = select whole row
        const atom = ATOMS.find(a => a.id === id);
        const row = ATOMS.filter(a => a.row === atom.row);
        const allPinned = row.every(a => prev.has(a.id));
        if (allPinned) row.forEach(a => next.delete(a.id));
        else row.forEach(a => next.add(a.id));
      } else { next.add(id); }
      return next;
    });
  }, []);

  const onExpand = useCallback((id) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  }, []);

  const totalW = PAD * 2 + COLS * (CELL_W + GAP);
  const totalH = PAD * 2 + 40 + 8 * (CELL_H + GAP + 6) + 200;

  return (
    <div style={{ width: "100%", height: "100vh", background: "#08090e", overflow: "auto", fontFamily: "'Inter', sans-serif" }}>
      {/* Title bar */}
      <div style={{ padding: "12px 20px", borderBottom: "1px solid #1a1b25", display: "flex", alignItems: "center", gap: 12, position: "sticky", top: 0, background: "#08090e", zIndex: 200 }}>
        <span style={{ fontSize: 16, fontWeight: 800, background: "linear-gradient(135deg, #e8a838, #ef4444)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
          Theophysics Periodic Table
        </span>
        <span style={{ fontSize: 10, color: "#4b5563" }}>{ATOMS.length} atoms · {EDGES.length} edges</span>
        <div style={{ marginLeft: "auto", display: "flex", gap: 12, fontSize: 10, color: "#6b7280" }}>
          <span><b style={{ color: "#c8ccd4" }}>Click</b> pin</span>
          <span><b style={{ color: "#c8ccd4" }}>Shift</b> multi</span>
          <span><b style={{ color: "#c8ccd4" }}>Double</b> expand</span>
        </div>
      </div>

      {/* Legend */}
      <div style={{ padding: "8px 20px", display: "flex", gap: 14, flexWrap: "wrap", borderBottom: "1px solid #1a1b2510" }}>
        {Object.entries(TYPE_COLORS).map(([t, c]) => (
          <div key={t} style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 10 }}>
            <span style={{ color: c, fontWeight: 700, fontSize: 12 }}>{GLYPHS[t]}</span>
            <span style={{ color: "#6b7280" }}>{t}</span>
          </div>
        ))}
        <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
          {Object.entries(GRADE_BG).filter(([g]) => g !== "—").map(([g, c]) => (
            <span key={g} style={{ fontSize: 9, fontWeight: 800, padding: "1px 6px", borderRadius: 3, background: c, color: GRADE_FG[g] }}>{g}</span>
          ))}
        </div>
      </div>

      {/* Thread summary */}
      {pinned.size > 0 && thread && (
        <div style={{ padding: "6px 20px", background: "#ef444408", borderBottom: "1px solid #ef444420", display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 10, color: "#ef4444", fontWeight: 700 }}>THREAD</span>
          <span style={{ fontSize: 10, color: "#9ca3af" }}>
            {[...pinned].map(id => ATOMS.find(a => a.id === id)?.symbol).join(" + ")} → {thread.size} nodes in chain
          </span>
          <button onClick={() => { setPinned(new Set()); }} style={{ marginLeft: "auto", fontSize: 10, color: "#6b7280", background: "transparent", border: "1px solid #2d3040", borderRadius: 4, padding: "2px 8px", cursor: "pointer" }}>Clear</button>
        </div>
      )}

      {/* Grid */}
      <div style={{ position: "relative", minWidth: totalW, minHeight: totalH, padding: PAD }} onClick={() => { setPinned(new Set()); }}>
        {/* Row labels */}
        {ROW_LABELS.map((label, i) => (
          <div key={i} style={{
            position: "absolute", left: -2,
            top: PAD + 20 + i * (CELL_H + GAP + 6) + CELL_H / 2 - 6,
            fontSize: 8, color: "#2d3040", fontWeight: 700, letterSpacing: "0.08em",
            writingMode: "vertical-rl", textOrientation: "mixed", transform: "rotate(180deg)",
          }}>{label}</div>
        ))}

        {/* SVG edges layer */}
        <svg style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none", zIndex: 0 }}>
          {EDGES.map((edge, i) => {
            const fn = ATOMS.find(a => a.id === edge.from);
            const tn = ATOMS.find(a => a.id === edge.to);
            if (!fn || !tn) return null;
            const x1 = PAD + fn.col * (CELL_W + GAP) + CELL_W / 2;
            const y1 = PAD + 20 + fn.row * (CELL_H + GAP + 6) + CELL_H;
            const x2 = PAD + tn.col * (CELL_W + GAP) + CELL_W / 2;
            const y2 = PAD + 20 + tn.row * (CELL_H + GAP + 6);
            const inT = thread ? (thread.has(fn.id) && thread.has(tn.id)) : true;
            const alpha = thread ? (inT ? 0.7 : 0.04) : 0.12;
            const col = TYPE_COLORS[fn.type];
            return (
              <line key={i} x1={x1} y1={y1} x2={x2} y2={y2}
                stroke={col} strokeWidth={inT && thread ? 2.5 : 1} opacity={alpha}
                markerEnd={inT && thread ? "" : ""} />
            );
          })}
        </svg>

        {/* Atom blocks */}
        {ATOMS.map(atom => (
          <AtomBlock
            key={atom.id} atom={atom}
            isPinned={pinned.has(atom.id)}
            inThread={thread ? thread.has(atom.id) : false}
            hasThread={!!thread}
            isExpanded={expanded.has(atom.id)}
            onPin={onPin} onExpand={onExpand}
          />
        ))}
      </div>
    </div>
  );
}
