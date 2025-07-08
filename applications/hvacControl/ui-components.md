# SVGL Air Conditioner Controller  
**Component-Based Design (High-Level UI Architecture)**

This document outlines the composable UI structure for the round LCD air conditioner controller, using reusable LVGL/SVGL components with hierarchical templating support.

---

## 🧩 High-Level Components

### `RoomScreen`
Represents one room’s interface view. Composed of reusable subcomponents.

**Children:**
- `RoomHeader`
- `TemperatureArc`
- `ACStatusLabel`
- `TouchControls`
- `RotaryControlHandler`
- `BackgroundSwipeHandler`

---

## 🔁 Reusable Components

### `RoomHeader`
Displays the room name and optional icon.

**Primitives:**
- `label` (room name)
- Optional `label` for icon

**Variables:**
- `text`, `icon`, `font`, `align`, `id`

---

### `TemperatureArc`
Circular arc around the screen showing the current target temperature.

**Primitives:**
- `arc`
- `label` (overlay value)

**Variables:**
- `min`, `max`, `value_source`, `id`, `color`

---

### `ACStatusLabel`
Displays whether the AC is ON or OFF.

**Primitives:**
- `label`

**Variables:**
- `text_source` (ON/OFF), `color`, `id`

---

### `TouchControls`
A container for interactive AC settings.

**Composed of:**
- `ModeButton`
- `FanSpeedButton`
- `SwingToggleButton`

---

### `TouchButton`
A generic button that toggles or cycles a value.

**Primitives:**
- `label` or `icon`
- `on_click`/`script`

**Variables:**
- `icon`, `action`, `position`, `id`, `font`, `feedback_color`

**Common Aliases:**
- `ModeButton`
- `FanSpeedButton`
- `SwingToggleButton`

---

### `RotaryControlHandler`
Handles rotary input and press detection.

**Function Only – No visual primitives**

**Events:**
- `on_clockwise`: increase temperature
- `on_anticlockwise`: decrease temperature
- `on_press`: toggle AC power

---

### `BackgroundSwipeHandler`
Captures swipe gestures for room navigation.

**Events:**
- `on_swipe_left`: go to next room
- `on_swipe_right`: go to previous room

---

## Optional Enhancements

### `AnimatedArc`
Advanced version of `TemperatureArc` with animation states.

---

### `RoomCardPreview`
Compact component to show room icon, current temp, and AC status for dashboards.

---

### `AlertIndicator`
Small visual flag (icon) for HVAC communication errors or warnings.

---

## 🧱 Component Hierarchy Example

RoomScreen
├── RoomHeader
├── TemperatureArc
├── ACStatusLabel
├── TouchControls
│ ├── ModeButton
│ ├── FanSpeedButton
│ └── SwingToggleButton
├── RotaryControlHandler
└── BackgroundSwipeHandler

---