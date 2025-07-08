# SVGL-Based Air Conditioner Controller  
**Design Document**

## Overview

This project aims to create a visually rich and intuitive user interface for controlling air conditioners across multiple rooms in a smart home environment. The interface is built using SVGL (LVGL for ESPHome) and designed specifically for a round LCD with touch capability and a rotary knob with press functionality.

It integrates with Home Assistant and provides fast, tactile access to essential AC controls in a visually engaging format.

---

## Goals

- Seamless room-based AC control through a hardware interface
- Minimal interaction required for common tasks (e.g., temp adjustment, power toggle)
- Visually clear and consistent user interface for all rooms
- Offline fallback functionality via ESPHome logic
- Full integration with Home Assistant entities

---

## Target Hardware

- **Round touchscreen LCD** (2.1"–2.8")
- **ESP32-S3 microcontroller**
- **Rotary encoder with push button**

---

## Key Interactions

| Action               | Description                              |
|----------------------|-------------------------------------------|
| Swipe left/right     | Switch between rooms                      |
| Turn rotary knob     | Adjust target temperature                 |
| Press rotary knob    | Toggle AC power (on/off)                  |
| Tap on-screen controls | Change fan speed, mode, or swing state   |

---

## User Interface Design

Each room has its own dedicated screen view.

### Common Elements Per Room

- **Center**: Room icon and name (e.g., "Bedroom", "Living Room")
- **Status Indicator**: Shows AC power state (ON/OFF)
- **Temperature Arc**: Circular visual arc around the screen indicating current target temperature
- **Touch Areas**: Discrete regions to modify fan speed, mode, and swing options

### Navigation

- Horizontal swipe to switch rooms
- On-screen gestures and touch targets for secondary settings

---

## Functional Scope

### Included Features

- Multi-room AC control
- Temperature adjustment
- Power toggle via knob press
- Visual feedback for current and target temperature
- Fan speed, mode, and swing toggle via touch

### Not Included (initial version)

- AC scheduling
- Occupancy sensing
- Weather-based automation
- Advanced configuration UI

---

## Integration with Home Assistant

- Room AC units are represented as `climate` entities
- State changes (temperature, mode, power) are reflected in Home Assistant
- Communication via native API or MQTT
- Optional: Presence and room temperature data can be displayed if available

---

## Design Principles

- **Glanceable UI**: Show the most important state info at a glance
- **Minimal input**: Avoid menu digging; one action per control
- **Immediate feedback**: UI should reflect changes instantly
- **Consistency**: All room screens follow the same layout and logic

---

## Future Considerations

- Theme customization (color schemes per room or mode)
- Animated transitions and visual effects
- Additional HVAC data (humidity, outdoor temp, etc.)
- Voice control triggers or assistant integration
- Modular version for wall-mounted or table-top variants

---

## Status

| Stage               | Progress     |
|---------------------|--------------|
| Concept & Planning  | ✅ Done       |
| UI Prototyping      | 🟡 Ongoing    |
| Hardware Testing    | ⬜ Not started |
| ESPHome Integration | ⬜ Not started |
| Home Assistant Sync | ⬜ Not started |
