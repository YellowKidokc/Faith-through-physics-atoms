import { useState, useRef, useEffect, useCallback } from "react";

const NODES = [
  { id: "GOD", label: "God (Axiom)", type: "axiom", x: 500, y: 30, grade: "—", row: 0, desc: "The one axiom. Self-grounding ground." },
  { id: "G01", label: "Self-Grounding", type: "claim", x: 100, y: 120, grade: "C", row: 1, desc: "G must ground itself" },
  { id: "G02", label: "Omniscience", type: "claim", x: 240, y: 120, grade: "C", row: 1, desc: "G knows all that is knowable" },
  { id: "G03", label: "Omnipotence", type: "claim", x: 380, y: 120, grade: "C", row: 1, desc: "G can actualize any consistent state" },
  { id: "G06", label: "Perfection", type: "claim", x: 540, y: 120, grade: "C", row: 1, desc: "Maximal coherence = perfection" },
  { id: "G07", label: "Moral Nature", type: "claim", x: 700, y: 120, grade: "C", row: 1, desc: "G is necessarily moral" },
  { id: "G08", label: "Divine Negation", type: "claim", x: 860, y: 120, grade: "C", row: 1, desc: "What G cannot do" },
  { id: "F01", label: "Existence", type: "claim", x: 80, y: 230, grade: "B", row: 2, desc: "Why something rather than nothing" },
  { id: "F02", label: "Information", type: "claim", x: 230, y: 230, grade: "C", row: 2, desc: "Information is fundamental" },
  { id: "F03", label: "Coherence", type: "claim", x: 380, y: 230, grade: "C", row: 2, desc: "The coherence imperative" },
  { id: "F04", label: "Actuality", type: "claim", x: 550, y: 230, grade: "C", row: 2, desc: "Potentiality to actualization" },
  { id: "F05", label: "Agency", type: "claim", x: 720, y: 230, grade: "C", row: 2, desc: "Agency is real" },
  { id: "ME", label: "Master Equation\nχ = C_W[∏ Xᵢ]", type: "equation", x: 400, y: 350, grade: "B", row: 3, desc: "The full product form" },
  { id: "CHI", label: "χ Properties", type: "claim", x: 640, y: 350, grade: "—", row: 3, desc: "Bounded, product, veto, dimensionless" },
  { id: "G_var", label: "G\nNegentropy", type: "variable", x: 40, y: 470, grade: "B", row: 4, desc: "External negentropy influx. Mirror: Maxwell's demon, photosynthesis." },
  { id: "M_var", label: "M\nAlignment", type: "variable", x: 140, y: 470, grade: "B", row: 4, desc: "Alignment cosine. Mirror: Malus's law, spin alignment." },
  { id: "E_var", label: "E\nFidelity", type: "variable", x: 240, y: 470, grade: "B", row: 4, desc: "Signal fidelity. Mirror: Shannon capacity, DNA replication." },
  { id: "S_var", label: "S_eff\nEntropy", type: "variable", x: 340, y: 470, grade: "B", row: 4, desc: "Entropy suppression. Mirror: Boltzmann factor e^(-αS)." },
  { id: "T_var", label: "T\nTime", type: "variable", x: 440, y: 470, grade: "B", row: 4, desc: "Temporal integration. Mirror: impulse, compound interest." },
  { id: "K_var", label: "K\nCompression", type: "variable", x: 540, y: 470, grade: "B", row: 4, desc: "Info compression. Mirror: Kolmogorov complexity, crystal vs glass." },
  { id: "R_var", label: "R\nPhase", type: "variable", x: 640, y: 470, grade: "B", row: 4, desc: "Phase transition. Mirror: apoptosis, circuit breaker." },
  { id: "Q_var", label: "Q\nSuperposition", type: "variable", x: 740, y: 470, grade: "B", row: 4, desc: "Unresolved possibility. Mirror: stem cell totipotency." },
  { id: "F_var", label: "F\nCorrelation", type: "variable", x: 840, y: 470, grade: "B", row: 4, desc: "Non-local correlation. Mirror: quantum entanglement." },
  { id: "C_var", label: "C\nIntegration", type: "variable", x: 940, y: 470, grade: "B", row: 4, desc: "Integration measure. Mirror: IIT Phi." },
  { id: "VETO", label: "Zero Collapse\n(Lean ✓)", type: "proof", x: 200, y: 590, grade: "A", row: 5, desc: "Any factor = 0 → χ = 0. Lean-verified." },
  { id: "GRACE_CHAIN", label: "Grace Chain\n(Lean ✓)", type: "proof", x: 400, y: 590, grade: "A", row: 5, desc: "Grace → Faith → Hope → Salvation." },
  { id: "LAGRANGIAN", label: "Lowe Lagrangian\n(Python ✓)", type: "proof", x: 600, y: 590, grade: "B", row: 5, desc: "Mass matrix + Hamiltonian verified" },
  { id: "FORMAL_SPEC", label: "Formal Spec", type: "proof", x: 800, y: 590, grade: "B", row: 5, desc: "Lean guardrail supported" },
  { id: "H01", label: "Constitution", type: "claim", x: 40, y: 700, grade: "C", row: 6, desc: "Body, Soul, Spirit" },
  { id: "H03", label: "Soul Field", type: "claim", x: 170, y: 700, grade: "C", row: 6, desc: "S as enduring bearer" },
  { id: "H06", label: "Consciousness\n& Φ", type: "claim", x: 310, y: 700, grade: "C", row: 6, desc: "Consciousness and integrated information" },
  { id: "FRUITS", label: "Fruits of Spirit\n(9 terms)", type: "claim", x: 500, y: 700, grade: "C", row: 6, desc: "Lean conditional (has sorry)" },
  { id: "GRACE_OP", label: "Grace Operator\n(sorry)", type: "claim", x: 690, y: 700, grade: "C", row: 6, desc: "grace_injective incomplete" },
  { id: "L1", label: "Law 1\nNewton-Grace", type: "law", x: 40, y: 810, grade: "B", row: 7, desc: "Near-isomorphic" },
  { id: "L4", label: "Law 4\nYukawa-Agape", type: "law", x: 200, y: 810, grade: "B", row: 7, desc: "Derived (confinement)" },
  { id: "L5", label: "Law 5\nClausius-Judgment", type: "law", x: 360, y: 810, grade: "B", row: 7, desc: "Derived (Cross uniqueness)" },
  { id: "L6", label: "Law 6\nShannon-Logos", type: "law", x: 520, y: 810, grade: "B", row: 7, desc: "Split (Shannon + Kolmogorov)" },
  { id: "L9", label: "Law 9\nFermi-Conservation", type: "law", x: 680, y: 810, grade: "B", row: 7, desc: "Derived (Noether + CP)" },
  { id: "L10", label: "Law 10\nCoherence-Christ", type: "law", x: 840, y: 810, grade: "B", row: 7, desc: "Definitional (wrapper)" },
  { id: "ISO_LANG", label: "Langevin\nDynamics", type: "mirror", x: 100, y: 920, grade: "L6", row: 8, desc: "Maps AND breaks. Grace ≠ noise." },
  { id: "ISO_BOLTZ", label: "Boltzmann\nFactor", type: "mirror", x: 260, y: 920, grade: "L6", row: 8, desc: "S_eff = e^(-αS). Same form." },
  { id: "ISO_ISING", label: "Ising Model", type: "mirror", x: 420, y: 920, grade: "L6", row: 8, desc: "Fruits critical behavior" },
  { id: "ISO_SHANNON", label: "Shannon\nCapacity", type: "mirror", x: 580, y: 920, grade: "L7", row: 8, desc: "E IS this. Definitional." },
  { id: "ISO_AND", label: "AND Gate", type: "mirror", x: 740, y: 920, grade: "L7", row: 8, desc: "Veto IS AND. Lean proved." },
  { id: "ISO_APOP", label: "Apoptosis", type: "mirror", x: 900, y: 920, grade: "L5", row: 8, desc: "Binary irreversible. Maps onto R." },
];

const EDGES = [
  { from: "GOD", to: "G01", type: "generates" }, { from: "GOD", to: "G02", type: "generates" },
  { from: "GOD", to: "G03", type: "generates" }, { from: "GOD", to: "G06", type: "generates" },
  { from: "GOD", to: "G07", type: "generates" }, { from: "GOD", to: "G08", type: "generates" },
  { from: "GOD", to: "F01", type: "generates" },
  { from: "F01", to: "F02", type: "depends" }, { from: "F02", to: "F03", type: "depends" },
  { from: "F03", to: "F04", type: "depends" }, { from: "F04", to: "F05", type: "depends" },
  { from: "F02", to: "ME", type: "grounds" }, { from: "F03", to: "ME", type: "grounds" },
  { from: "G06", to: "ME", type: "grounds" }, { from: "ME", to: "CHI", type: "defines" },
  { from: "ME", to: "G_var", type: "contains" }, { from: "ME", to: "M_var", type: "contains" },
  { from: "ME", to: "E_var", type: "contains" }, { from: "ME", to: "S_var", type: "contains" },
  { from: "ME", to: "T_var", type: "contains" }, { from: "ME", to: "K_var", type: "contains" },
  { from: "ME", to: "R_var", type: "contains" }, { from: "ME", to: "Q_var", type: "contains" },
  { from: "ME", to: "F_var", type: "contains" }, { from: "ME", to: "C_var", type: "contains" },
  { from: "CHI", to: "VETO", type: "proves" }, { from: "G_var", to: "GRACE_CHAIN", type: "proves" },
  { from: "ME", to: "LAGRANGIAN", type: "proves" }, { from: "ME", to: "FORMAL_SPEC", type: "proves" },
  { from: "C_var", to: "H06", type: "grounds" }, { from: "F05", to: "H01", type: "grounds" },
  { from: "H01", to: "H03", type: "depends" }, { from: "H01", to: "H06", type: "depends" },
  { from: "ME", to: "FRUITS", type: "derives" }, { from: "G_var", to: "GRACE_OP", type: "derives" },
  { from: "FRUITS", to: "GRACE_OP", type: "depends" },
  { from: "ME", to: "L1", type: "derives" }, { from: "ME", to: "L4", type: "derives" },
  { from: "ME", to: "L5", type: "derives" }, { from: "ME", to: "L6", type: "derives" },
  { from: "ME", to: "L9", type: "derives" }, { from: "ME", to: "L10", type: "derives" },
  { from: "CHI", to: "ISO_LANG", type: "mirror" }, { from: "S_var", to: "ISO_BOLTZ", type: "mirror" },
  { from: "FRUITS", to: "ISO_ISING", type: "mirror" }, { from: "E_var", to: "ISO_SHANNON", type: "mirror" },
  { from: "VETO", to: "ISO_AND", type: "mirror" }, { from: "R_var", to: "ISO_APOP", type: "mirror" },
];

const TC = { axiom:"#e8a838", claim:"#6d9cff", equation:"#c084fc", variable:"#34d399", proof:"#22c55e", law:"#f97316", mirror:"#ec4899" };
const GB = { A:"#22c55e", B:"#6d9cff", C:"#f59e0b", D:"#ef4444" };
const EC = { generates:"#e8a838", depends:"#6d9cff", grounds:"#c084fc", contains:"#34d399", proves:"#22c55e", derives:"#f97316", defines:"#c084fc", mirror:"#ec4899" };
const ROW_LABELS = ["Ground", "God Properties", "Foundations", "Equation", "Variables", "Proofs", "Ontology / Fruits", "Ten Laws", "Physics Mirrors"];

function getThread(ids) {
  const t = new Set();
  function up(id) { if (t.has(id)) return; t.add(id); EDGES.filter(e => e.to === id).forEach(e => up(e.from)); }
  function down(id) { if (t.has(id)) return; t.add(id); EDGES.filter(e => e.from === id).forEach(e => down(e.to)); }
  ids.forEach(id => { up(id); down(id); });
  return t;
}

function getPaths(sourceIds) {
  const paths = [];
  function trace(id, path) {
    const nexts = EDGES.filter(e => e.from === id);
    if (nexts.length === 0) { paths.push([...path]); return; }
    nexts.forEach(e => { if (!path.includes(e.to)) trace(e.to, [...path, e.to]); });
  }
  // Walk up to roots first
  function findRoots(id, visited) {
    if (visited.has(id)) return [];
    visited.add(id);
    const parents = EDGES.filter(e => e.to === id);
    if (parents.length === 0) return [id];
    return parents.flatMap(e => findRoots(e.from, visited));
  }
  const roots = new Set();
  sourceIds.forEach(id => findRoots(id, new Set()).forEach(r => roots.add(r)));
  roots.forEach(r => trace(r, [r]));
  return paths.filter(p => sourceIds.some(s => p.includes(s)));
}

export default function AtomMap() {
  const cvs = useRef(null);
  const [pan, setPan] = useState({ x: 20, y: 10 });
  const [zoom, setZoom] = useState(0.78);
  const [drag, setDrag] = useState(null);
  const [moved, setMoved] = useState(false);
  const [sel, setSel] = useState(null);
  const [hov, setHov] = useState(null);
  const [nodes, setNodes] = useState(NODES);
  const [pinned, setPinned] = useState(new Set()); // multi-select set
  const last = useRef({ x: 0, y: 0 });

  const thread = pinned.size > 0 ? getThread([...pinned]) : null;
  const threadEdgeSet = thread ? new Set(EDGES.map((e, i) => thread.has(e.from) && thread.has(e.to) ? i : -1).filter(i => i >= 0)) : null;
  const routePaths = pinned.size > 0 ? getPaths([...pinned]) : [];

  const ts = useCallback((x, y) => ({ sx: x * zoom + pan.x, sy: y * zoom + pan.y }), [zoom, pan]);
  const tw = useCallback((sx, sy) => ({ x: (sx - pan.x) / zoom, y: (sy - pan.y) / zoom }), [zoom, pan]);

  const draw = useCallback(() => {
    const c = cvs.current; if (!c) return;
    const ctx = c.getContext("2d");
    const dpr = window.devicePixelRatio || 2;
    const W = c.offsetWidth, H = c.offsetHeight;
    c.width = W * dpr; c.height = H * dpr;
    ctx.scale(dpr, dpr);
    ctx.fillStyle = "#0c0d12"; ctx.fillRect(0, 0, W, H);

    // Row bands
    const rows = {};
    nodes.forEach(n => { if (!rows[n.row]) rows[n.row] = []; rows[n.row].push(n); });
    for (let r = 0; r <= 8; r++) {
      const band = nodes.filter(n => n.row === r);
      if (band.length === 0) continue;
      const minY = Math.min(...band.map(n => n.y)) - 25;
      const maxY = Math.max(...band.map(n => n.y)) + 35;
      const { sy: sy1 } = ts(0, minY); const { sy: sy2 } = ts(0, maxY);
      ctx.fillStyle = r % 2 === 0 ? "#0f101808" : "#10111a08";
      ctx.fillRect(0, sy1, W, sy2 - sy1);
      ctx.fillStyle = "#1e203020";
      ctx.font = "9px Inter, sans-serif"; ctx.textAlign = "left";
      ctx.fillText(ROW_LABELS[r] || "", 6, sy1 + 12);
    }

    // Background edges
    EDGES.forEach((e, ei) => {
      const fn = nodes.find(n => n.id === e.from), tn = nodes.find(n => n.id === e.to);
      if (!fn || !tn) return;
      const f = ts(fn.x, fn.y), t = ts(tn.x, tn.y);
      const inT = thread ? threadEdgeSet.has(ei) : true;
      const isSel = sel && (e.from === sel || e.to === sel);
      ctx.globalAlpha = thread ? (inT ? 0.5 : 0.04) : (isSel ? 0.6 : 0.15);
      ctx.strokeStyle = EC[e.type] || "#444";
      ctx.lineWidth = 1;
      ctx.setLineDash(e.type === "mirror" ? [4, 3] : []);
      ctx.beginPath(); ctx.moveTo(f.sx, f.sy); ctx.lineTo(t.sx, t.sy); ctx.stroke();
    });
    ctx.setLineDash([]);

    // Route paths — thick glowing lines showing the actual route
    if (pinned.size > 0 && routePaths.length > 0) {
      const pathColors = ["#ef4444", "#22c55e", "#6d9cff", "#e8a838", "#c084fc", "#ec4899", "#facc15"];
      const drawn = new Set();
      routePaths.forEach((path, pi) => {
        const col = pathColors[pi % pathColors.length];
        for (let i = 0; i < path.length - 1; i++) {
          const edgeKey = path[i] + ">" + path[i + 1];
          if (drawn.has(edgeKey)) continue;
          drawn.add(edgeKey);
          const fn = nodes.find(n => n.id === path[i]), tn = nodes.find(n => n.id === path[i + 1]);
          if (!fn || !tn) continue;
          const f = ts(fn.x, fn.y), t = ts(tn.x, tn.y);
          // Glow
          ctx.globalAlpha = 0.3; ctx.strokeStyle = col; ctx.lineWidth = 8;
          ctx.beginPath(); ctx.moveTo(f.sx, f.sy); ctx.lineTo(t.sx, t.sy); ctx.stroke();
          // Core
          ctx.globalAlpha = 0.9; ctx.lineWidth = 2.5;
          ctx.beginPath(); ctx.moveTo(f.sx, f.sy); ctx.lineTo(t.sx, t.sy); ctx.stroke();
          // Arrow
          const a = Math.atan2(t.sy - f.sy, t.sx - f.sx);
          const mx = t.sx - Math.cos(a) * 22 * zoom, my = t.sy - Math.sin(a) * 22 * zoom;
          ctx.beginPath();
          ctx.moveTo(mx, my); ctx.lineTo(mx - 10 * Math.cos(a - 0.35), my - 10 * Math.sin(a - 0.35));
          ctx.moveTo(mx, my); ctx.lineTo(mx - 10 * Math.cos(a + 0.35), my - 10 * Math.sin(a + 0.35));
          ctx.stroke();
        }
      });
      ctx.globalAlpha = 1;
    }

    // Nodes
    for (const n of nodes) {
      const { sx, sy } = ts(n.x, n.y);
      const isPinned = pinned.has(n.id);
      const inT = thread ? thread.has(n.id) : true;
      const isSel = sel === n.id;
      const isHov = hov === n.id;
      const w = n.type === "equation" ? 82 : n.type === "axiom" ? 72 : 56;
      const h = n.label.includes("\n") ? 36 : 26;
      ctx.globalAlpha = thread ? (inT ? 1 : 0.07) : 1;

      if ((inT && thread) || isHov || isSel) { ctx.shadowColor = isPinned ? "#ef4444" : TC[n.type]; ctx.shadowBlur = isPinned ? 18 : 8; }

      ctx.fillStyle = isPinned ? "#ef444418" : (isSel ? TC[n.type] + "15" : "#14151e");
      ctx.strokeStyle = isPinned ? "#ef4444" : (GB[n.grade] || TC[n.type] || "#333");
      ctx.lineWidth = isPinned ? 2.5 : 1;
      ctx.beginPath(); ctx.roundRect(sx - w, sy - h, w * 2, h * 2, 6); ctx.fill(); ctx.stroke();
      ctx.shadowBlur = 0;

      if (isPinned) { ctx.fillStyle = "#ef4444"; ctx.beginPath(); ctx.arc(sx + w - 7, sy - h + 7, 4, 0, Math.PI * 2); ctx.fill(); }

      if (n.grade && n.grade !== "—") {
        ctx.fillStyle = GB[n.grade] || "#555"; ctx.font = "bold 8px Inter"; ctx.textAlign = "right";
        ctx.fillText(n.grade, sx + w - (isPinned ? 14 : 4), sy - h + 12);
      }

      ctx.fillStyle = inT || !thread ? "#c8ccd4" : "#c8ccd410";
      ctx.font = `${isSel ? "bold " : ""}10px Inter, sans-serif`; ctx.textAlign = "center";
      n.label.split("\n").forEach((l, i) => ctx.fillText(l, sx, sy - 2 + i * 13));

      ctx.fillStyle = (TC[n.type] || "#888") + (inT || !thread ? "60" : "10");
      ctx.font = "7px Inter"; ctx.fillText(n.type.toUpperCase(), sx, sy + h - 4);
      ctx.globalAlpha = 1;
    }
  }, [nodes, pan, zoom, sel, hov, pinned, thread, threadEdgeSet, routePaths, ts]);

  useEffect(() => { draw(); }, [draw]);
  useEffect(() => { const h = () => draw(); window.addEventListener("resize", h); return () => window.removeEventListener("resize", h); }, [draw]);

  const hit = useCallback((sx, sy) => {
    const { x, y } = tw(sx, sy);
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i]; const w = n.type === "equation" ? 82 : n.type === "axiom" ? 72 : 56;
      const h = n.label.includes("\n") ? 36 : 26;
      if (x >= n.x - w && x <= n.x + w && y >= n.y - h && y <= n.y + h) return n;
    }
    return null;
  }, [nodes, tw]);

  const onDown = (e) => {
    const r = cvs.current.getBoundingClientRect();
    const n = hit(e.clientX - r.left, e.clientY - r.top);
    setMoved(false);
    if (n) { setDrag(n.id); setSel(n.id); } else { setDrag("pan"); if (!e.shiftKey) { setSel(null); setPinned(new Set()); } }
    last.current = { x: e.clientX, y: e.clientY };
  };

  const onMove = (e) => {
    const r = cvs.current.getBoundingClientRect();
    if (!drag) { const n = hit(e.clientX - r.left, e.clientY - r.top); setHov(n ? n.id : null); return; }
    const dx = e.clientX - last.current.x, dy = e.clientY - last.current.y;
    if (Math.abs(dx) > 2 || Math.abs(dy) > 2) setMoved(true);
    last.current = { x: e.clientX, y: e.clientY };
    if (drag === "pan") setPan(p => ({ x: p.x + dx, y: p.y + dy }));
    else setNodes(prev => prev.map(n => n.id === drag ? { ...n, x: n.x + dx / zoom, y: n.y + dy / zoom } : n));
  };

  const onUp = (e) => {
    if (drag && drag !== "pan" && !moved) {
      const id = drag;
      const isShift = e.shiftKey;
      setPinned(prev => {
        const next = new Set(prev);
        if (isShift) {
          // Shift+click: add/remove from selection, or select whole row
          const node = nodes.find(n => n.id === id);
          if (node) {
            const sameRow = nodes.filter(n => n.row === node.row);
            const allRowPinned = sameRow.every(n => next.has(n.id));
            if (next.has(id) && !allRowPinned) {
              // Already pinned individually, shift = select entire row
              sameRow.forEach(n => next.add(n.id));
            } else if (allRowPinned) {
              // All row pinned, shift = deselect row
              sameRow.forEach(n => next.delete(n.id));
            } else {
              // Add to selection
              next.add(id);
            }
          }
        } else {
          // Regular click: toggle single node, clear others
          if (next.has(id) && next.size === 1) {
            next.clear();
          } else {
            next.clear();
            next.add(id);
          }
        }
        return next;
      });
    }
    setDrag(null);
  };

  const onWheel = (e) => { e.preventDefault(); setZoom(z => Math.max(0.2, Math.min(3, z * (e.deltaY > 0 ? 0.92 : 1.08)))); };

  const selNode = nodes.find(n => n.id === sel);
  const threadNodes = thread ? nodes.filter(n => thread.has(n.id)) : [];
  const pinnedList = [...pinned].map(id => nodes.find(n => n.id === id)).filter(Boolean);

  return (
    <div style={{ width: "100%", height: "100vh", background: "#0c0d12", display: "flex", fontFamily: "'Inter', sans-serif" }}>
      <canvas ref={cvs} style={{ flex: 1, cursor: drag === "pan" ? "grabbing" : drag ? "move" : "default" }}
        onMouseDown={onDown} onMouseMove={onMove} onMouseUp={onUp} onMouseLeave={() => setDrag(null)} onWheel={onWheel} />

      <div style={{ width: 290, background: "#14151e", borderLeft: "1px solid #1e2030", padding: 14, overflowY: "auto", flexShrink: 0, fontSize: 12 }}>
        <div style={{ fontSize: 15, fontWeight: 700, color: "#e8a838", marginBottom: 2 }}>Atom Map</div>
        <div style={{ fontSize: 10, color: "#4b5563", marginBottom: 10 }}>{nodes.length} atoms · {EDGES.length} edges</div>

        <div style={{ fontSize: 10, color: "#6b7280", background: "#0c0d12", borderRadius: 6, padding: "8px 10px", marginBottom: 10, lineHeight: 1.6 }}>
          <b style={{ color: "#c8ccd4" }}>Click</b> — pin node, show thread<br />
          <b style={{ color: "#c8ccd4" }}>Shift+Click</b> — add to selection<br />
          <b style={{ color: "#c8ccd4" }}>Shift+Click pinned</b> — select entire row<br />
          <b style={{ color: "#c8ccd4" }}>Click empty</b> — clear all<br />
          Drag nodes to rearrange. Scroll to zoom.
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "3px 8px", marginBottom: 10 }}>
          {Object.entries(TC).map(([t, c]) => (
            <div key={t} style={{ display: "flex", alignItems: "center", gap: 3, fontSize: 9, color: "#6b7280" }}>
              <span style={{ width: 6, height: 6, borderRadius: 2, background: c }} />{t}
            </div>
          ))}
        </div>

        <div style={{ height: 1, background: "#1e2030", margin: "6px 0 10px" }} />

        {/* Pinned nodes */}
        {pinnedList.length > 0 && (
          <div style={{ marginBottom: 10 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: "#ef4444", marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Pinned ({pinnedList.length})
            </div>
            {pinnedList.map(n => (
              <div key={n.id} style={{ display: "flex", alignItems: "center", gap: 5, padding: "3px 4px", borderRadius: 3, fontSize: 11, color: "#e2e8f0", cursor: "pointer", background: sel === n.id ? "#ffffff08" : "transparent" }}
                onClick={() => setSel(n.id)}>
                <span style={{ width: 5, height: 5, borderRadius: "50%", background: TC[n.type], flexShrink: 0 }} />
                <span style={{ flex: 1 }}>{n.label.replace("\n", " ")}</span>
                <span style={{ fontSize: 9, color: GB[n.grade] || "#555" }}>{n.grade}</span>
              </div>
            ))}
          </div>
        )}

        {/* Thread */}
        {thread && threadNodes.length > 0 && (
          <div style={{ marginBottom: 10 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: "#94a3af", marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Full Thread ({threadNodes.length} nodes)
            </div>
            <div style={{ maxHeight: 300, overflowY: "auto" }}>
              {[...new Set(threadNodes.map(n => n.row))].sort((a, b) => a - b).map(row => (
                <div key={row}>
                  <div style={{ fontSize: 8, color: "#3b4252", padding: "4px 0 1px", textTransform: "uppercase", letterSpacing: "0.08em" }}>{ROW_LABELS[row]}</div>
                  {threadNodes.filter(n => n.row === row).map(n => (
                    <div key={n.id} onClick={() => setSel(n.id)} style={{
                      display: "flex", alignItems: "center", gap: 5, padding: "2px 4px", fontSize: 11, cursor: "pointer",
                      color: pinned.has(n.id) ? "#ef4444" : "#9ca3af",
                      background: sel === n.id ? "#ffffff06" : "transparent", borderRadius: 3,
                    }}>
                      <span style={{ width: 5, height: 5, borderRadius: "50%", background: TC[n.type], flexShrink: 0 }} />
                      {n.label.replace("\n", " ")}
                      <span style={{ marginLeft: "auto", fontSize: 9, color: GB[n.grade] || "#444" }}>{n.grade}</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Selected detail */}
        {selNode && (
          <>
            <div style={{ height: 1, background: "#1e2030", margin: "6px 0 10px" }} />
            <div style={{ fontSize: 12, fontWeight: 600, color: "#e2e8f0", marginBottom: 3 }}>{selNode.label.replace("\n", " ")}</div>
            <div style={{ fontSize: 10, color: GB[selNode.grade] || "#6b7280", fontWeight: 700, marginBottom: 6 }}>
              Grade {selNode.grade} · {selNode.type} · Row {selNode.row}
            </div>
            <div style={{ fontSize: 11, color: "#94a3af", lineHeight: 1.5, marginBottom: 8 }}>{selNode.desc}</div>
            <div style={{ fontSize: 9, color: "#4b5563" }}>
              {EDGES.filter(e => e.from === sel || e.to === sel).map((e, i) => {
                const oid = e.from === sel ? e.to : e.from;
                const on = nodes.find(n => n.id === oid);
                return (
                  <div key={i} onClick={() => setSel(oid)} style={{ padding: "2px 0", cursor: "pointer", color: "#6b7280" }}>
                    {e.from === sel ? "↓" : "↑"} <span style={{ color: TC[on?.type] }}>{on?.label.replace("\n", " ")}</span> <span style={{ color: "#3b4252" }}>{e.type}</span>
                  </div>
                );
              })}
            </div>
          </>
        )}

        {!selNode && pinnedList.length === 0 && <div style={{ color: "#3b4252", fontSize: 11 }}>Click a node to trace its thread. Shift+click to build a multi-select.</div>}
      </div>
    </div>
  );
}
