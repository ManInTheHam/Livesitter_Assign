import { Rnd } from "react-rnd";
import { useState } from "react";

export default function OverlayEditor({ items, setItems, readOnly = false }) {
  const [selectedItem, setSelectedItem] = useState(null);
  const containerSize = { width: 960, height: 540 };

  const update = (i, patch) => {
    const next = items.slice();
    next[i] = { ...next[i], ...patch };
    setItems(next);
  };

  const deleteItem = (index) => {
    const next = items.filter((_, i) => i !== index);
    setItems(next);
    setSelectedItem(null);
  };

  const addTextOverlay = () => {
    const newItem = {
      type: "text",
      content: "New Text",
      x: 0.1,
      y: 0.1,
      w: 0.2,
      h: 0.1,
      fontSize: 24,
      color: "#ffffff",
      z: items.length + 1
    };
    setItems([...items, newItem]);
  };

  // We position/size overlays in percentages (x,y,w,h ∈ [0..1]) so they stay responsive.
  return (
    <>
      <div style={{ 
        position: "absolute", 
        inset: 0, 
        pointerEvents: readOnly ? "none" : "auto",
        overflow: "hidden"
      }}>
        {items.map((it, i) => (
          <Rnd
            key={i}
            bounds="parent"
            size={{ width: `${it.w * 100}%`, height: `${it.h * 100}%` }}
            position={{ x: it.x * containerSize.width, y: it.y * containerSize.height }}
            onDragStop={(e, d) => update(i, { x: d.x / containerSize.width, y: d.y / containerSize.height })}
            onResizeStop={(e, dir, ref, delta, pos) =>
              update(i, {
                w: ref.offsetWidth / containerSize.width,
                h: ref.offsetHeight / containerSize.height,
                x: pos.x / containerSize.width,
                y: pos.y / containerSize.height,
              })
            }
            enableResizing={!readOnly}
            disableDragging={readOnly}
            onClick={() => setSelectedItem(i)}
            style={{ 
              border: readOnly ? "none" : selectedItem === i ? "2px solid #667eea" : "1px dashed rgba(255,255,255,0.5)", 
              zIndex: it.z ?? 1,
              cursor: readOnly ? "default" : "move",
              borderRadius: "4px",
              background: selectedItem === i && !readOnly ? "rgba(102, 126, 234, 0.1)" : "transparent"
            }}
            resizeHandleStyles={{
              bottomRight: {
                background: "#667eea",
                border: "2px solid white",
                borderRadius: "50%",
                width: "12px",
                height: "12px",
                right: "-6px",
                bottom: "-6px"
              }
            }}
          >
            {it.type === "text" ? (
              <div style={{
                width: "100%", 
                height: "100%", 
                display: "flex", 
                alignItems: "center", 
                justifyContent: "center",
                color: it.color || "#fff", 
                fontSize: it.fontSize || 24, 
                opacity: it.opacity ?? 1,
                textShadow: "2px 2px 4px rgba(0,0,0,0.8)",
                fontWeight: "600",
                userSelect: "none",
                padding: "4px"
              }}>
                {it.content}
              </div>
            ) : (
              <img
                src={it.content}
                alt="overlay"
                style={{ 
                  width: "100%", 
                  height: "100%", 
                  objectFit: "contain", 
                  opacity: it.opacity ?? 1,
                  userSelect: "none",
                  pointerEvents: "none"
                }}
              />
            )}
            
            {selectedItem === i && !readOnly && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteItem(i);
                }}
                style={{
                  position: "absolute",
                  top: "-10px",
                  right: "-10px",
                  width: "20px",
                  height: "20px",
                  borderRadius: "50%",
                  background: "#ef4444",
                  color: "white",
                  border: "2px solid white",
                  cursor: "pointer",
                  fontSize: "12px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  zIndex: 1000
                }}
              >
                ×
              </button>
            )}
          </Rnd>
        ))}
      </div>

      {/* Overlay Controls */}
      {!readOnly && (
        <div style={{
          position: "absolute",
          top: "10px",
          left: "10px",
          zIndex: 1000,
          display: "flex",
          gap: "8px"
        }}>
          <button
            onClick={addTextOverlay}
            style={{
              background: "rgba(102, 126, 234, 0.9)",
              color: "white",
              border: "none",
              borderRadius: "6px",
              padding: "8px 12px",
              fontSize: "12px",
              cursor: "pointer",
              backdropFilter: "blur(10px)",
              fontWeight: "500"
            }}
          >
            + Add Text
          </button>
          
          {selectedItem !== null && (
            <div style={{
              background: "rgba(0, 0, 0, 0.8)",
              color: "white",
              borderRadius: "6px",
              padding: "8px 12px",
              fontSize: "12px",
              backdropFilter: "blur(10px)"
            }}>
              Selected: {items[selectedItem]?.type === "text" ? items[selectedItem]?.content : "Image"}
            </div>
          )}
        </div>
      )}

      {/* Click outside to deselect */}
      {!readOnly && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            zIndex: -1
          }}
          onClick={() => setSelectedItem(null)}
        />
      )}
    </>
  );
}
