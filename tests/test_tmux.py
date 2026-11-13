"""Config-driven HID modifier model, not Zephyr/BLE or on-device execution.

Models ZMK's reference-counted explicit mods, masked explicit mods and unmasked
implicit keycode mods. The macro and mod-morph definitions come from the keymap.
"""
import re
import unittest

from test_keymap import source, bindings


def node(name):
    match = re.search(re.escape(name) + r'\s*\{(.*?)\};', source(), re.S)
    if not match:
        raise AssertionError('missing behavior: ' + name)
    return match[1]


def macro_reports(name, held):
    counts = [int(bool(held & (1 << i))) for i in range(8)]
    reports = []

    def invoke(binding, pressed, masked=0):
        parts = binding.split()
        if parts[0] != '&kp':
            body = node(parts[0][1:])
            mask = int(re.search(r'mods\s*=\s*<([^>]+)>', body)[1], 0)
            pair = re.search(r'bindings\s*=\s*<(.*?)>\s*,\s*<(.*?)>', body, re.S)
            explicit = sum((count > 0) << i for i, count in enumerate(counts))
            return invoke(pair[2] if explicit & mask else pair[1], pressed, mask if explicit & mask else 0)
        key = parts[1]
        if key == 'LCTRL':
            counts[0] += 1 if pressed else -1
            assert counts[0] >= 0
            return
        implicit = 0
        if key.startswith('LC('):
            key = key[3:-1]
            implicit = 1
        explicit = sum((count > 0) << i for i, count in enumerate(counts))
        if pressed:
            reports.append((key, (explicit & ~masked) | implicit))

    body = node(name)
    sequence = bindings(re.search(r'bindings\s*=\s*(.*?);', body, re.S)[1].replace('<', '').replace('>', '').replace(',', ''))
    mode = 'tap'
    for binding in sequence:
        if binding.startswith('&macro_'):
            mode = binding[len('&macro_'):]
        else:
            if mode in ('tap', 'press'):
                invoke(binding, True)
            if mode in ('tap', 'release'):
                invoke(binding, False)
    return reports, sum((count > 0) << i for i, count in enumerate(counts))


class TmuxModifierTests(unittest.TestCase):
    def test_default_macros_send_prefix_then_unmodified_command(self):
        for name, key in [('tmux_previous', 'P'), ('tmux_next', 'N'), ('tmux_zoom', 'Z')]:
            self.assertEqual(macro_reports(name, 0), ([('B', 1), (key, 0)], 0))

    def test_held_ctrl_does_not_turn_zoom_into_suspend(self):
        self.assertEqual(macro_reports('tmux_zoom', 1), ([('B', 1), ('Z', 0)], 1))

    def test_all_held_modifier_masks_preserve_physical_state_and_exact_shortcuts(self):
        for held in range(256):
            for name, key in [('tmux_previous', 'P'), ('tmux_next', 'N'), ('tmux_zoom', 'Z')]:
                with self.subTest(held=held, macro=name):
                    self.assertEqual(macro_reports(name, held), ([('B', 1), (key, 0)], held))


if __name__ == '__main__':
    unittest.main()
