# Component Generator Documentation

This document describes all components currently supported by the component generator, including their configuration options and usage examples.

## Table of Contents

- [arc](#arc)
- [arc_countdown_interval](#arc_countdown_interval)
- [arc_global](#arc_global)
- [arc_interval](#arc_interval)
- [arc_widget](#arc_widget)
- [bar_widget](#bar_widget)
- [label_widget](#label_widget)
- [arc_countdown (Custom Component)](#arc_countdown-custom-component)

---

## arc

**Type:** `arc`

**Description:**
A basic arc component.

**Configuration Options:**
- `id` (string, required): Unique identifier for the arc.
- `min` (number, optional): Minimum value (default: 0).
- `max` (number, optional): Maximum value (default: 100).
- `value` (number, optional): Initial value (default: 100).

**Example:**
```yaml
- id: my_arc
  type: arc
  min: 0
  max: 100
  value: 100
```

---

## arc_countdown_interval

**Type:** `arc_countdown_interval`

**Description:**
Controls the countdown behavior for an arc component.

**Configuration Options:**
- `id` (string, required): Unique identifier for the controller.
- `arc_id` (string, required): The id of the arc component to control.
- `duration` (number, required): Countdown duration in seconds.
- `on_done_callback` (string, optional): Action to perform when countdown is done.

**Example:**
```yaml
- id: my_controller
  type: arc_countdown_interval
  arc_id: my_arc
  duration: 60
  on_done_callback: do_something
```

---

## arc_global

**Type:** `arc_global`

**Description:**
Global configuration for arc components.

**Configuration Options:**
- `id` (string, required): Unique identifier.
- ... (other options as defined in the template)

**Example:**
```yaml
- id: global_arc
  type: arc_global
  # ...other options
```

---

## arc_interval

**Type:** `arc_interval`

**Description:**
Interval configuration for arc components.

**Configuration Options:**
- `id` (string, required): Unique identifier.
- ... (other options as defined in the template)

**Example:**
```yaml
- id: interval_arc
  type: arc_interval
  # ...other options
```

---

## arc_widget

**Type:** `arc_widget`

**Description:**
Widget configuration for arc components.

**Configuration Options:**
- `id` (string, required): Unique identifier.
- ... (other options as defined in the template)

**Example:**
```yaml
- id: widget_arc
  type: arc_widget
  # ...other options
```

---

## bar_widget

**Type:** `bar_widget`

**Description:**
Widget configuration for bar components.

**Configuration Options:**
- `id` (string, required): Unique identifier.
- ... (other options as defined in the template)

**Example:**
```yaml
- id: widget_bar
  type: bar_widget
  # ...other options
```

---

## label_widget

**Type:** `label_widget`

**Description:**
Widget configuration for label components.

**Configuration Options:**
- `id` (string, required): Unique identifier.
- ... (other options as defined in the template)

**Example:**
```yaml
- id: widget_label
  type: label_widget
  # ...other options
```

---

## arc_countdown (Custom Component)

**Type:** `arc_countdown`

**Description:**
A custom component that wraps an arc and a countdown controller, providing default configuration and an event callback for when the countdown is done.

**Configuration Options:**
- `id` (string, required): Unique identifier for the arc countdown group.
- `duration` (number, required): Countdown duration in seconds.
- `on_countdown_done_callback` (string, optional): Action to perform when countdown is done.

**Example:**
```yaml
- id: my_arc_countdown
  type: arc_countdown
  duration: 60
  on_countdown_done_callback: do_something
```

This will generate two components:
- An `arc` component with id `<id>_arc`
- An `arc_countdown_interval` controller with id `<id>_controller` linked to the arc

---

*For more details, see the templates in the `componentGenerator/templates` and `componentGenerator/custom_templates` folders.*
