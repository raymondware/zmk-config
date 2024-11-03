# Custom ZMK Firmware Keymap for 36-Key 5-Column Keyboard

## Introduction

This repository contains a custom ZMK firmware keymap designed for my 36-key keyboard with a 5-column layout, created by Raymond Ware. The keymap is optimized for efficient typing and includes several layers and custom behaviors to enhance productivity.
I use this keymap daily as a software engineer who primarily works with Neovim. The layout is tailored to enhance coding efficiency and streamline workflows within Neovim.

## Features

- **Homerow Mods**: Modifier keys are integrated into the home row for efficient typing.
- **Multiple Layers**: Default, Symbol, Navigation, and Number layers.
- **Combos**: Key combinations for accessing modifiers, layer toggles, and special functions.
- **Macros**: Custom macros for specific tasks.

## Keymap Layers

### Default Layer

#### Key Layout
```
Left Hand                                        Right Hand
┌─────┬─────┬─────┬─────┬─────┐         ┌─────┬─────┬─────┬─────┬─────┐
│  Q  │  W  │  E  │  R  │  T  │         │  Y  │  U  │  I  │  O  │  P  │
├─────┼─────┼─────┼─────┼─────┤         ├─────┼─────┼─────┼─────┼─────┤
│A(GUI)|S(ALT)|D(CTRL)|F(SHIFT)|  G  │   │  H  │J(SHIFT)|K(CTRL)|L(ALT)|  ;  │
├─────┼─────┼─────┼─────┼─────┤         ├─────┼─────┼─────┼─────┼─────┤
│  Z  │  X  │  C  │  V  │  B  │         │  N  │  M  │  ,  │  .  │  /  │
└─────┴─────┴─────┴─────┴─────┘         └─────┴─────┴─────┴─────┴─────┘
           ┌─────┬─────────┬─────┐     ┌─────┬─────────┬─────┐
           │LCTRL│ MO(SYM) │Space│     │Enter│ MO(NUM) │Bksp │
           └─────┴─────────┴─────┘     └─────┴─────────┴─────┘
```

#### Notes

- **Homerow Mods**: The keys `A`, `S`, `D`, `F` on the left hand and `J`, `K`, `L` on the right hand are mod-tap keys:
  - When tapped, they produce the letter.
  - When held, they act as modifiers:
    - `A` - Left GUI
    - `S` - Left Alt
    - `D` - Left Ctrl
    - `F` - Left Shift
    - `J` - Right Shift
    - `K` - Right Ctrl
    - `L` - Right Alt
- **Thumb Keys**:
  - Left Thumb:
    - `LCTRL` - Left Control
    - `MO(SYM)` - Momentary Symbol Layer
    - `Space` - Spacebar
  - Right Thumb:
    - `Enter` - Enter key
    - `MO(NUM)` - Momentary Number Layer
    - `Bksp` - Backspace

### Symbol Layer
```
Left Hand                                        Right Hand
┌─────┬─────┬─────┬─────┬─────┐         ┌─────┬─────┬─────┬─────┬─────┐
│  !  │  @  │  #  │  $  │  %  │         │  ^  │  &  │  *  │  -  │  \  │
├─────┼─────┼─────┼─────┼─────┤         ├─────┼─────┼─────┼─────┼─────┤
│  `  │  ~  │  [  │  ]  │  -  │         │  +  │  {  │  }  │  (  │  )  │
├─────┼─────┼─────┼─────┼─────┤         ├─────┼─────┼─────┼─────┼─────┤
│  '  │  "  │  <  │  >  │  _  │         │  |  │  :  │  ;  │  ?  │  /  │
└─────┴─────┴─────┴─────┴─────┘         └─────┴─────┴─────┴─────┴─────┘
           ┌─────┬─────────┬─────┐     ┌─────┬─────────┬─────┐
           │LCTRL│ LSHIFT  │Space│     │Enter│ RSHIFT  │Bksp │
           └─────┴─────────┴─────┘     └─────┴─────────┴─────┘
```

### Navigation Layer
```
Left Hand                                        Right Hand
┌─────┬─────┬─────┬─────┬─────┐         ┌─────┬─────┬─────┬─────┬─────┐
│ F1  │ F2  │ F3  │ F4  │ F5  │         │ F6  │ F7  │ F8  │ F9  │ F10 │
├─────┼─────┼─────┼─────┼─────┤         ├─────┼─────┼─────┼─────┼─────┤
│ F11 │ F12 │     │     │     │         │Left │Down │ Up  │Right│     │
├─────┼─────┼─────┼─────┼─────┤         ├─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │         │     │     │     │     │     │
└─────┴─────┴─────┴─────┴─────┘         └─────┴─────┴─────┴─────┴─────┘
           ┌─────┬─────────┬─────┐     ┌─────┬─────────┬─────┐
           │LCTRL│ LSHIFT  │Space│     │Enter│ RSHIFT  │Bksp │
           └─────┴─────────┴─────┘     └─────┴─────────┴─────┘
```

### Number Layer
```
Left Hand                                        Right Hand
┌─────┬─────┬─────┬─────┬─────┐         ┌─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │         │  6  │  7  │  8  │  9  │  0  │
├─────┼─────┼─────┼─────┼─────┤         ├─────┼─────┼─────┼─────┼─────┤
│ Esc │ Tab │  -  │  +  │  /  │         │  *  │  %  │  =  │  .  │  ,  │
├─────┼─────┼─────┼─────┼─────┤         ├─────┼─────┼─────┼─────┼─────┤
│     │LAlt │     │     │     │         │Left │Down │ Up  │Right│     │
└─────┴─────┴─────┴─────┴─────┘         └─────┴─────┴─────┴─────┴─────┘
           ┌─────┬─────────┬─────┐     ┌─────┬─────────┬─────┐
           │LCTRL│ LSHIFT  │Space│     │Enter│ RSHIFT  │Bksp │
           └─────┴─────────┴─────┘     └─────┴─────────┴─────┘
```

## Combos

Combos are key combinations that perform specific actions when pressed together.

### Modifier Combos

- **Escape**: Press `Q` + `W` to produce `Esc`.
- **Left Shift Sticky**: Press `A` + `S` to activate a sticky `Left Shift`.
- **Right Shift Sticky**: Press `J` + `K` to activate a sticky `Right Shift`.
- **Tab**: Press `S` + `D` to produce `Tab`.
- **Left Control**: Press `Z` + `X` to produce `Left Control`.
- **Right Control**: Press `M` + `,` to produce `Right Control`.
- **Left Alt**: Press `X` + `C` to produce `Left Alt`.
- **Right Alt**: Press `,` + `.` to produce `Right Alt`.
- **Left GUI**: Press `A` + `Z` to produce `Left GUI`.
- **Backspace**: Press `O` + `P` to produce `Backspace`.

### Layer Toggles

- **Default Layer**: Press `N` + `M` to switch to the Default Layer.
- **Navigation Layer**: Press `.` + `/` to switch to the Navigation Layer.
- **Symbol Layer**: Press `B` + `N` to switch to the Symbol Layer.
- **Number Layer**: Press `,` + `.` to switch to the Number Layer.

### Vim Combos

- **First Non-Blank**: Press `Y` + `U` to produce `^` (beginning of line in Vim).
- **Last Non-Blank**: Press `U` + `I` to produce `$` (end of line in Vim).
- **Format Document**: Press `I` + `O` to execute a custom macro that formats the document.
- **Comment Toggle**: Press `O` + `P` to send the key sequence `gcc` (comment toggle in Vim).

## Macros

- **Vim Format Document**: A custom macro that sends `Ctrl+C`, then `F` to format the document in Vim.

## Installation

To use this keymap:

1. **Clone the Repository**:

2. **Build the ZMK Firmware**:

Follow the instructions provided in the ZMK Documentation to build the firmware using this keymap.

3. **Flash the Firmware**:

Flash the built firmware to your keyboard using the appropriate flashing tool for your microcontroller.

## Contributing
Contributions are welcome! If you have ideas to improve this configuration, please feel free to open an issue or submit a pull request. Your insights can help enhance the efficiency and usability of this layout for everyone.


