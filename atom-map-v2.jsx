import { useState, useRef, useEffect, useCallback } from "react";

const NODES = [
  { id: "GOD", label: "God (Axiom)", type: "axiom", x: 500, y: 30, grade: "—", desc: "The one axiom. Self-grounding ground." },
  { id: "G01", label: "Self-Grounding", type: "claim", x: 120, y: 120, grade: "C", desc: "G must ground itself" },
  { id: "G02", label: "Omniscience", type: "claim", x: 260, y: 120, grade: "C", desc: "G knows all that is knowable" },
  { id: "G03", label: "Omnipotence", type: "claim", x: 400, y: 120, grade: "C", desc: "G can actualize any consistent state" },
  { id: "G06", label: "Perfection", type: "claim", x: 600, y: 120, grade: "C", desc: "Maximal coherence = perfection" },
  { id: "G07", label: "Moral Nature", type: "claim", x: 740, y: 120, grade: "C", desc: "G is necessarily moral" },
  { id: "G08", label: "Divine Negation", type: "claim", x: 880, y: 120, grade: "C", desc: "What G cannot do" },
  { id: "F01", label: "Existence", type: "claim", x: 80, y: 230, grade: "B", desc: "Why something rather than nothing" },
  { id: "F02", label: "Information", type: "claim", x: 230, y: 230, grade: "C", desc: "Information is fundamental" },
  { id: "F03", label: "Coherence", type: "claim", x: 380, y: 230, grade: "C", desc: "The coherence imperative" },
  { id: "F04", label: "Actuality", type: "claim", x: 550, y: 230, grade: "C", desc: "Potentiality → actualization" },
  { id: "F05", label: "Agency", type: "claim", x: 720, y: 230, grade: "C", desc: "Agency is real" },
  { id: "ME", label: "Master Equation\nχ = C_W[∏ Xᵢ]", type: "equation", x: 400, y: 350, grade: "B", desc: "The full product form" },
  { id: "CHI", label: "χ Properties", type: "claim", x: 620, y: 350, grade: "—", desc: "Bounded, product, veto, dimensionless" },
  { id: "G_var", label: "G\nNegentropy", type: "variable", x: 40, y: 470, grade: "B", desc: "External negentropy influx" },
  { id: "M_var", label: "M\nAlignment", type: "variable", x: 140, y: 470, grade: "B", desc: "Alignment cosine" },
  { id: "E_var", label: "E\nFidelity", type: "variable", x: 240, y: 470, grade: "B", desc: "Signal propagation fidelity" },
  { id: "S_var", label: "S_eff\nEntropy", type: "variable", x: 340, y: 470, grade: "B", desc: "Effective entropy factor" },
  { id: "T_var", label: "T\nTime", type: "variable", x: 440, y: 470, grade: "B", desc: "Temporal integration" },
  { id: "K_var", label: "K\nCompression", type: "variable", x: 540, y: 470, grade: "B", desc: "Information compression ratio" },
  { id: "R_var", label: "R\nPhase", type: "variable", x: 640, y: 470, grade: "B", desc: "Phase transition indicator" },
  { id: "Q_var", label: "Q\nSuperposition", type: "variable", x: 740, y: 470, grade: "B", desc: "Unresolved possibility" },
  { id: "F_var", label: "F\nCorrelation", type: "variable", x: 840, y: 470, grade: "B", desc: "Non-local correlation" },
  { id: "C_var", label: "C\nIntegration", type: "variable", x: 940, y: 470, grade: "B", desc: "Total integration measure" },
  { id: "VETO", label: "Zero Collapse\n(Lean ✓)", type: "proof", x: 250, y: 590, grade: "A", desc: "Any factor = 0 → χ = 0. Lean-verified." },
  { id: "GRACE_CHAIN", label: "Grace Chain\n(Lean ✓)", type: "proof", x: 450, y: 590, grade: "A", desc: "Grace → Faith → Hope → Salvation ordering." },
  { id: "LAGRANGIAN", label: "Lowe Lagrangian\n(Python ✓)", type: "proof", x: 650, y: 590, grade: "B", desc: "Mass matrix + Hamiltonian verified" },
  { id: "FORMAL_SPEC", label: "Formal Spec", type: "proof", x: 100, y: 590, grade: "B", desc: "Lean guardrail supported" },
  { id: "H01", label: "Constitution", type: "claim", x: 40, y: 700, grade: "C", desc: "Body, Soul, Spirit" },
  { id: "H03", label: "Soul Field", type: "claim", x: 180, y: 700, grade: "C", desc: "S as enduring bearer" },
  { id: "H06", label: "Consciousness\n& Φ", type: "claim", x: 330, y: 700, grade: "C", desc: "Consciousness and integrated information" },
  { id: "FRUITS", label: "Fruits of Spirit\n(9 terms)", type: "claim", x: 530, y: 700, grade: "C", desc: "Lean conditional (has sorry)" },
  { id: "GRACE_OP", label: "Grace Operator\n(Lean sorry)", type: "claim", x: 730, y: 700, grade: "C", desc: "grace_injective incomplete" },
  { id: "L1", label: "Law 1\nNewton-Grace", type: "law", x: 40, y: 810, grade: "B", desc: "Near-isomorphic" },
  { id: "L4", label: "Law 4\nYukawa-Agape", type: "law", x: 200, y: 810, grade: "B", desc: "Derived (confinement)" },
  { id: "L5", label: "Law 5\nClausius-Judgment", type: "law", x: 360, y: 810, grade: "B", desc: "Derived (Cross uniqueness)" },
  { id: "L6", label: "Law 6\nShannon-Logos", type: "law", x: 520, y: 810, grade: "B", desc: "Split (Shannon + Kolmogorov)" },
  { id: "L9", label: "Law 9\nFermi-Conservation", type: "law", x: 680, y: 810, grade: "B", desc: "Derived (Noether + CP)" },
  { id: "L10", label: "Law 10\nCoherence-Christ", type: "law", x: 840, y: 810, grade: "B", desc: "Definitional (wrapper)" },
  { id: "ISO_LANG", label: "Langevin\nDynamics", type: "mirror", x: 150, y: 920, grade: "L6", desc: "Maps AND breaks. Grace ≠ noise." },
  { id: "ISO_BOLTZ", label: "Boltzmann\nFactor", type: "mirror", x: 310, y: 920, grade: "L6", desc: "S_eff = e^(-αS). Same form." },
  { id: "ISO_ISING", label: "Ising Model", type: "mirror", x: 470, y: 920, grade: "L6", desc: "Fruits critical behavior" },
  { id: "ISO_SHANNON", label: "Shannon\nCapacity", type: "mirror", x: 630, y: 920, grade: "L7", desc: "E IS this. Definitional." },
  { id: "ISO_AND", label: "AND Gate", type: "mirror", x: 790, y: 920, grade: "L7", desc: "Veto IS AND. Lean proved." },
  { id: "ISO_APOPTOSIS", label: "Apoptosis", type: "mirror", x: 940, y: 920, grade: "L5", desc: "Binary irreversible. Maps onto R." },
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
  { from: "VETO", to: "ISO_AND", type: "mirror" }, { from: "R_var", to: "ISO_APOPTOSIS", type: "mirror" },
];

const TYPE_COLORS = { axiom:"#e8a838", claim:"#6d9cff", equation:"#c084fc", variable:"#34d399", proof:"#22c55e", law:"#f97316", mirror:"#ec4899" };
const GRADE_BORDER = { A:"#22c55e", B:"#6d9cff", C:"#f59e0b", D:"#ef4444" };
const EDGE_COLORS = { generates:"#e8a838", depends:"#6d9cff", grounds:"#c084fc", contains:"#34d399", proves:"#22c55e", derives:"#f97316", defines:"#c084fc", mirror:"#ec4899" };
const CLICK_STATES = ["none", "green", "yellow", "red"];
const CLICK_COLORS = { none: null, green: "#22c55e", yellow: "#facc15", red: "#ef4444" };

function getThread(nodeId) {
  const inThread = new Set();
  function walkUp(id) { if (inThread.has(id)) return; inThread.add(id); EDGES.filter(e => e.to === id).forEach(e => walkUp(e.from)); }
  function walkDown(id) { if (inThread.has(id)) return; inThread.add(id); EDGES.filter(e => e.from === id).forEach(e => walkDown(e.to)); }
  walkUp(nodeId);
  walkDown(nodeId);
  return inThread;
}

function getThreadEdges(thread) {
  return new Set(EDGES.filter(e => thread.has(e.from) && thread.has(e.to)).map((_, i) => i));
}

export default function AtomGraph() {
  const canvasRef = useRef(null);
  const [pan, setPan] = useState({ x: 20, y: 10 });
  const [zoom, setZoom] = useState(0.82);
  const [dragging, setDragging] = useState(null);
  const [dragMoved, setDragMoved] = useState(false);
  const [selected, setSelected] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [nodes, setNodes] = useState(NODES);
  const [clickStates, setClickStates] = useState({});
  const lastMouse = useRef({ x: 0, y: 0 });

  const redNode = Object.entries(clickStates).find(([, v]) => v === "red")?.[0] || null;
  const thread = redNode ? getThread(redNode) : null;
  const threadEdges = thread ? getThreadEdges(thread) : null;

  const toScreen = useCallback((x, y) => ({ sx: x * zoom + pan.x, sy: y * zoom + pan.y }), [zoom, pan]);
  const toWorld = useCallback((sx, sy) => ({ x: (sx - pan.x) / zoom, y: (sy - pan.y) / zoom }), [zoom, pan]);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const dpr = window.devicePixelRatio || 2;
    const W = canvas.offsetWidth; const H = canvas.offsetHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = "#0f1015"; ctx.fillRect(0, 0, W, H);

    // Grid
    ctx.strokeStyle = "#1a1b25"; ctx.lineWidth = 0.5;
    const gs = 50 * zoom;
    for (let x = pan.x % gs; x < W; x += gs) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
    for (let y = pan.y % gs; y < H; y += gs) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }

    // Edges
    EDGES.forEach((edge, ei) => {
      const fn = nodes.find(n => n.id === edge.from);
      const tn = nodes.find(n => n.id === edge.to);
      if (!fn || !tn) return;
      const f = toScreen(fn.x, fn.y); const t = toScreen(tn.x, tn.y);
      const inThread2 = thread ? threadEdges.has(ei) : true;
      const alpha = thread ? (inThread2 ? 1 : 0.06) : (selected && (edge.from === selected || edge.to === selected) ? 1 : 0.35);
      const col = EDGE_COLORS[edge.type] || "#888";

      ctx.globalAlpha = alpha;
      ctx.strokeStyle = col;
      ctx.lineWidth = inThread2 && thread ? 2.5 : 1;
      ctx.setLineDash(edge.type === "mirror" ? [5, 4] : []);
      ctx.beginPath(); ctx.moveTo(f.sx, f.sy); ctx.lineTo(t.sx, t.sy); ctx.stroke();

      // Arrow
      const a = Math.atan2(t.sy - f.sy, t.sx - f.sx);
      const hl = thread && inThread2 ? 10 : 7;
      const mx = t.sx - Math.cos(a) * 22 * zoom; const my = t.sy - Math.sin(a) * 22 * zoom;
      ctx.beginPath();
      ctx.moveTo(mx, my);
      ctx.lineTo(mx - hl * Math.cos(a - 0.35), my - hl * Math.sin(a - 0.35));
      ctx.moveTo(mx, my);
      ctx.lineTo(mx - hl * Math.cos(a + 0.35), my - hl * Math.sin(a + 0.35));
      ctx.stroke();
      ctx.globalAlpha = 1;
    });
    ctx.setLineDash([]);

    // Nodes
    for (const node of nodes) {
      const { sx, sy } = toScreen(node.x, node.y);
      const isSel = selected === node.id;
      const isHov = hoveredNode === node.id;
      const cs = clickStates[node.id] || "none";
      const inThread2 = thread ? thread.has(node.id) : true;
      const w = node.type === "equation" ? 80 : node.type === "axiom" ? 70 : 55;
      const h = node.label.includes("\n") ? 36 : 26;

      ctx.globalAlpha = thread ? (inThread2 ? 1 : 0.08) : 1;

      // Glow for thread nodes
      if (thread && inThread2) {
        ctx.shadowColor = cs === "red" ? "#ef4444" : TYPE_COLORS[node.type];
        ctx.shadowBlur = cs === "red" ? 20 : 10;
      } else if (isHov || isSel) {
        ctx.shadowColor = TYPE_COLORS[node.type]; ctx.shadowBlur = 10;
      }

      // Background
      ctx.fillStyle = cs !== "none" ? CLICK_COLORS[cs] + "20" : (isSel ? TYPE_COLORS[node.type] + "18" : "#181a22");
      ctx.strokeStyle = cs !== "none" ? CLICK_COLORS[cs] : (GRADE_BORDER[node.grade] || TYPE_COLORS[node.type] || "#333");
      ctx.lineWidth = cs === "red" ? 3 : (cs !== "none" ? 2 : 1);
      ctx.beginPath(); ctx.roundRect(sx - w, sy - h, w * 2, h * 2, 6); ctx.fill(); ctx.stroke();
      ctx.shadowBlur = 0;

      // Click state dot
      if (cs !== "none") {
        ctx.fillStyle = CLICK_COLORS[cs];
        ctx.beginPath(); ctx.arc(sx + w - 8, sy - h + 8, 4, 0, Math.PI * 2); ctx.fill();
      }

      // Grade
      if (node.grade && node.grade !== "—") {
        ctx.fillStyle = GRADE_BORDER[node.grade] || "#6b7280";
        ctx.font = "bold 8px Inter, sans-serif"; ctx.textAlign = "right";
        ctx.fillText(node.grade, sx + w - (cs !== "none" ? 16 : 4), sy - h + 12);
      }

      // Label
      ctx.fillStyle = inThread2 || !thread ? (isSel ? "#fff" : "#c8ccd4") : "#c8ccd420";
      ctx.font = `${isSel ? "bold " : ""}10px Inter, sans-serif`; ctx.textAlign = "center";
      node.label.split("\n").forEach((l, i) => ctx.fillText(l, sx, sy - 2 + i * 13));

      // Type
      ctx.fillStyle = (TYPE_COLORS[node.type] || "#888") + (inThread2 || !thread ? "80" : "15");
      ctx.font = "7px Inter, sans-serif"; ctx.fillText(node.type.toUpperCase(), sx, sy + h - 4);

      ctx.globalAlpha = 1;
    }
  }, [nodes, pan, zoom, selected, hoveredNode, clickStates, thread, threadEdges, toScreen]);

  useEffect(() => { draw(); }, [draw]);
  useEffect(() => { const h = () => draw(); window.addEventListener("resize", h); return () => window.removeEventListener("resize", h); }, [draw]);

  const findNode = useCallback((sx, sy) => {
    const { x, y } = toWorld(sx, sy);
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      const w = n.type === "equation" ? 80 : n.type === "axiom" ? 70 : 55;
      const h = n.label.includes("\n") ? 36 : 26;
      if (x >= n.x - w && x <= n.x + w && y >= n.y - h && y <= n.y + h) return n;
    }
    return null;
  }, [nodes, toWorld]);

  const onDown = (e) => {
    const r = canvasRef.current.getBoundingClientRect();
    const sx = e.clientX - r.left; const sy = e.clientY - r.top;
    const node = findNode(sx, sy);
    setDragMoved(false);
    if (node) { setDragging(node.id); setSelected(node.id); }
    else { setDragging("pan"); setSelected(null); }
    lastMouse.current = { x: e.clientX, y: e.clientY };
  };

  const onMove = (e) => {
    const r = canvasRef.current.getBoundingClientRect();
    if (!dragging) { const n = findNode(e.clientX - r.left, e.clientY - r.top); setHoveredNode(n ? n.id : null); return; }
    const dx = e.clientX - lastMouse.current.x; const dy = e.clientY - lastMouse.current.y;
    if (Math.abs(dx) > 2 || Math.abs(dy) > 2) setDragMoved(true);
    lastMouse.current = { x: e.clientX, y: e.clientY };
    if (dragging === "pan") setPan(p => ({ x: p.x + dx, y: p.y + dy }));
    else setNodes(prev => prev.map(n => n.id === dragging ? { ...n, x: n.x + dx / zoom, y: n.y + dy / zoom } : n));
  };

  const onUp = (e) => {
    if (dragging && dragging !== "pan" && !dragMoved) {
      const id = dragging;
      setClickStates(prev => {
        const cur = prev[id] || "none";
        const next = CLICK_STATES[(CLICK_STATES.indexOf(cur) + 1) % CLICK_STATES.length];
        const newState = { ...prev };
        // Clear any other red
        if (next === "red") { for (const k of Object.keys(newState)) { if (newState[k] === "red") newState[k] = "none"; } }
        newState[id] = next;
        return newState;
      });
    }
    setDragging(null);
  };

  const onWheel = (e) => { e.preventDefault(); setZoom(z => Math.max(0.25, Math.min(3, z * (e.deltaY > 0 ? 0.92 : 1.08)))); };

  const selectedNode = nodes.find(n => n.id === selected);
  const connEdges = selected ? EDGES.filter(e => e.from === selected || e.to === selected) : [];
  const threadNodes = thread ? nodes.filter(n => thread.has(n.id)) : [];

  return (
    <div style={{ width: "100%", height: "100vh", background: "#0f1015", display: "flex", fontFamily: "'Inter', sans-serif" }}>
      <canvas ref={canvasRef} style={{ flex: 1, cursor: dragging === "pan" ? "grabbing" : dragging ? "move" : "default" }}
        onMouseDown={onDown} onMouseMove={onMove} onMouseUp={onUp} onMouseLeave={() => setDragging(null)} onWheel={onWheel} />

      <div style={{ width: 280, background: "#181a22", borderLeft: "1px solid #1e2030", padding: 16, overflowY: "auto", flexShrink: 0, fontSize: 12 }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: "#e8a838", marginBottom: 2 }}>Atom Dependency Map</div>
        <div style={{ fontSize: 10, color: "#4b5563", marginBottom: 12 }}>{nodes.length} atoms · {EDGES.length} edges</div>

        {/* Instructions */}
        <div style={{ fontSize: 10, color: "#6b7280", background: "#0f1015", borderRadius: 6, padding: "8px 10px", marginBottom: 12, lineHeight: 1.5 }}>
          <b style={{ color: "#94a3af" }}>Click</b> a node to cycle:<br />
          <span style={{ color: "#22c55e" }}>● Green</span> = marked
          <span style={{ color: "#facc15", marginLeft: 8 }}>● Yellow</span> = watch
          <span style={{ color: "#ef4444", marginLeft: 8 }}>● Red</span> = <b>isolate thread</b><br />
          <span style={{ color: "#6b7280" }}>Click again to clear. Drag to move.</span>
        </div>

        {/* Legend */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px 10px", marginBottom: 12 }}>
          {Object.entries(TYPE_COLORS).map(([t, c]) => (
            <div key={t} style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 10, color: "#6b7280" }}>
              <span style={{ width: 7, height: 7, borderRadius: 2, background: c }} />{t}
            </div>
          ))}
        </div>

        <div style={{ height: 1, background: "#1e2030", margin: "8px 0" }} />

        {/* Thread view */}
        {redNode && thread && (
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: "#ef4444", marginBottom: 6 }}>
              Thread: {nodes.find(n => n.id === redNode)?.label.replace("\n", " ")}
            </div>
            <div style={{ fontSize: 10, color: "#6b7280", marginBottom: 4 }}>{threadNodes.length} nodes in chain</div>
            {threadNodes.map(n => (
              <div key={n.id} onClick={() => setSelected(n.id)} style={{
                padding: "4px 6px", cursor: "pointer", borderRadius: 4, marginBottom: 2,
                background: selected === n.id ? "#ffffff08" : "transparent",
                display: "flex", alignItems: "center", gap: 6,
              }}>
                <span style={{ width: 6, height: 6, borderRadius: "50%", background: TYPE_COLORS[n.type], flexShrink: 0 }} />
                <span style={{ color: n.id === redNode ? "#ef4444" : "#c8ccd4", fontSize: 11 }}>{n.label.replace("\n", " ")}</span>
                <span style={{ marginLeft: "auto", fontSize: 9, color: GRADE_BORDER[n.grade] || "#4b5563" }}>{n.grade}</span>
              </div>
            ))}
          </div>
        )}

        {/* Selected node detail */}
        {selectedNode && !redNode && (
          <>
            <div style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0", marginBottom: 4 }}>{selectedNode.label.replace("\n", " ")}</div>
            <div style={{ fontSize: 11, color: GRADE_BORDER[selectedNode.grade] || "#6b7280", fontWeight: 700, marginBottom: 6 }}>
              Grade {selectedNode.grade} · {selectedNode.type}
            </div>
            <div style={{ fontSize: 12, color: "#94a3af", lineHeight: 1.5, marginBottom: 10 }}>{selectedNode.desc}</div>
            {connEdges.length > 0 && (
              <>
                <div style={{ fontSize: 10, color: "#6b7280", fontWeight: 600, marginBottom: 4 }}>CONNECTIONS</div>
                {connEdges.map((e, i) => {
                  const oid = e.from === selected ? e.to : e.from;
                  const on = nodes.find(n => n.id === oid);
                  return (
                    <div key={i} onClick={() => setSelected(oid)} style={{ fontSize: 11, color: "#9ca3af", padding: "2px 0", cursor: "pointer" }}>
                      {e.from === selected ? "→" : "←"} <span style={{ color: TYPE_COLORS[on?.type] }}>{on?.label.replace("\n", " ")}</span>
                      <span style={{ color: "#4b5563", marginLeft: 6 }}>{e.type}</span>
                    </div>
                  );
                })}
              </>
            )}
          </>
        )}

        {!selectedNode && !redNode && <div style={{ color: "#4b5563" }}>Click any node. Three clicks to isolate its thread.</div>}
      </div>
    </div>
  );
}
