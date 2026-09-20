/** TASK 036 — Hierarchy navigator (UI-only expansion; domain IDs preserved). */
import { useState, useMemo } from "react";
import { useSelection } from "../state/selectionStore";
import { useGardenState } from "../state/gardenStore";

type TreeItem = {
  id: string; type: string; parent_id?: string; meta?: Record<string, unknown>;
  domain_plant_id?: string; domain_organ_id?: string;
};

function getChildren(items: TreeItem[], parentId?: string): TreeItem[] {
  return items.filter((i) => i.parent_id === parentId);
}

function TreeRow({ item, items, depth = 0 }: { item: TreeItem; items: TreeItem[]; depth?: number }) {
  const [open, setOpen] = useState(true);
  const sel = useSelection((s) => s.selected);
  const selected = sel?.id === item.id;
  const children = getChildren(items, item.id);
  const hasChildren = children.length > 0;

  const handleClick = () => {
    useSelection.getState().select({
      id: item.id,
      type: item.type,
      parent_id: item.parent_id,
      local_pos: [0, 0, 0],
      world_pos: [0, 0, 0],
    });
  };

  return (
    <div style={{ marginLeft: depth * 12 }}>
      <button
        onClick={() => { if (hasChildren) setOpen((o) => !o); handleClick(); }}
        style={{
          display: "flex", alignItems: "center", gap: 6,
          width: "100%", textAlign: "left",
          padding: "3px 4px", border: "none", background: selected ? "rgba(88,166,255,0.18)" : "transparent",
          color: selected ? "#58a6ff" : "#c9d1d9",
          fontSize: 11, cursor: "pointer", borderRadius: 3,
        }}
        title={`${item.id} | parent=${item.parent_id || "none"}`}
      >
        <span style={{ width: 10, color: "#8b949e", fontSize: 10 }}>
          {hasChildren ? (open ? "▾" : "▸") : "·"}
        </span>
        <span style={{ fontWeight: selected ? 600 : 400 }}>{item.id}</span>
        <span style={{ color: "#484f58", fontSize: 9, marginLeft: 4 }}>{item.type}</span>
        {item.domain_plant_id && <span style={{ color: "#3fb950", fontSize: 9, marginLeft: 4 }}>plant:{item.domain_plant_id}</span>}
        {item.domain_organ_id && <span style={{ color: "#a371f7", fontSize: 9, marginLeft: 4 }}>organ:{item.domain_organ_id}</span>}
      </button>
      {open && hasChildren && (
        <div>
          {children.map((c) => (
            <TreeRow key={c.id} item={c} items={items} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function HierarchyNavigator() {
  const sceneNodes = useGardenState((s) => s.sceneNodes) || [];
  const selectedId = useSelection((s) => s.selected?.id);

  // Build tree items from scene nodes; preserve IDs/parent/child
  const items: TreeItem[] = useMemo(() => {
    return sceneNodes.map((n: any) => ({
      id: n.id,
      type: n.type || "other",
      parent_id: n.parent_id,
      meta: n.meta,
      domain_plant_id: n.domain_plant_id,
      domain_organ_id: n.domain_organ_id,
    }));
  }, [sceneNodes]);

  const roots = getChildren(items, undefined);

  return (
    <div style={{ padding: 8, fontSize: 11, lineHeight: 1.3, color: "#c9d1d9" }}>
      <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 1, color: "#8b949e", marginBottom: 6, fontWeight: 600 }}>
        Hierarchy — Garden
      </div>
      {items.length === 0 && (
        <div style={{ color: "#484f58", fontSize: 10, padding: "4px 0" }}>
          No hierarchy loaded. Use <b>Garden</b> mode with API data or <b>demoFixture</b> to populate.
        </div>
      )}
      {roots.map((r) => (
        <TreeRow key={r.id} item={r} items={items} />
      ))}
      <div style={{ marginTop: 6, paddingTop: 6, borderTop: "1px solid #30363d", color: "#484f58", fontSize: 10 }}>
        Selection: <b style={{ color: selectedId ? "#58a6ff" : "#8b949e" }}>{selectedId || "none"}</b>
        {" · "}Expansion: UI-only (no domain mutation)
      </div>
    </div>
  );
}
