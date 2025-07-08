# 📐 Round LCD UI Layout Plan

## 📱 Screen Shape

- **Aspect Ratio**: 1:1 (perfect circle)
- **Safe zone**: Outer 5–10% margin reserved for gestures / rounded cutoff
- **Interactive ring**: Rotational arc usable for scroll/visual feedback
- **Primary touch area**: Central 60% of screen diameter

---

## 🧭 Layout Zones

+-------------------------+
| [ Room ] | ← Top label: Room name + icon
| |
| [ ❄️ 24° ] | ← Center: Icon + Target Temp
| |
| [ Temp Arc ] | ← Outer Arc (Target Temp Range)
| |
| Mode | Fan | Swing | ← Touch Controls (bottom/curve)
| |
| AC: ON / OFF | ← Status Indicator (small text)
+-------------------------+

---

## 📌 Element Breakdown

### 🏷️ 1. `RoomHeader`  
**Location:** Top-center (Y: ~10% of screen)  
**Size:** Small text label (room name)  
**Optional:** Inline icon (e.g., 🛏️, 🛋️, 🧒)

---

### 🌡️ 2. `TemperatureArc`  
**Location:** Perimeter of screen (radius ~80–95%)  
**Function:** Circular gauge showing target temperature  
**Interaction:** Rotary knob rotates through this scale

- Optional: Dual arc (target + current temp)
- Optional: Animate arc fill on update

---

### 🔘 3. `Center Display`  
**Location:** Center (X/Y midpoint)  
**Contents:**
- AC icon (snowflake, flame, fan)
- Large label with target temperature (`24°`, etc.)

**Font Size:** Large for visibility  
**Interaction:** None (read-only)

---

### 🎛️ 4. `TouchControls`  
**Location:** Bottom 25% of screen  
**Controls:**
- `ModeButton` (Cool, Heat, Dry, Auto)
- `FanSpeedButton` (Low, Med, High)
- `SwingToggleButton`

**Layout:**
- Horizontally aligned OR slight curve along arc
- Touch target radius: ≥ 40px

---

### 💡 5. `ACStatusLabel`  
**Location:** Bottom-center or slightly above controls  
**Text:** "AC: ON" / "AC: OFF"  
**Font:** Medium, subtle color  
**Color Feedback:** Green (on), gray/red (off)

---

### 🔁 6. `BackgroundSwipeHandler`  
**Gesture Zone:** Full screen  
**Purpose:** Swipe left/right to change rooms

---

### 🔘 7. `RotaryControlHandler`  
**Physical Control**  
- Rotate: Adjust target temperature (arc + label update)
- Press: Toggle AC ON/OFF

---

## 🎯 Touch & Interaction Planning

| Control           | Input Type | Area          | Action                    |
|-------------------|------------|---------------|----------------------------|
| Swipe             | Touch      | Entire screen | Change room (left/right)  |
| Rotary Turn       | Knob       | Physical      | Adjust temperature        |
| Rotary Press      | Knob Btn   | Physical      | Toggle power ON/OFF       |
| Mode Button       | Touch      | Bottom left   | Cycle mode                |
| Fan Speed Button  | Touch      | Bottom center | Cycle fan speed           |
| Swing Toggle      | Touch      | Bottom right  | Toggle swing              |

---

## 🔲 Sizing Suggestions (for 2.8" 480×480)

| Element             | Suggested Size |
|---------------------|----------------|
| Temperature label   | 80–120 px font |
| Arc thickness       | 20–30 px       |
| Touch buttons       | 80–100 px wide |
| Padding (safe area) | 24 px min      |

---

## 🧠 Design Guidelines

- Keep center clean and readable
- Use curved or radial alignment for buttons to match the screen shape
- Prefer icon + label combo for quick recognition
- Animate arc and icon transitions for better feedback
- Ensure touch areas are spaced to avoid mis-taps
