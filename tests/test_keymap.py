"""Source-contract checks; firmware compilation and on-device feel are separate gates."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def source():
    def expand(path):
        text = path.read_text()
        return re.sub(r'#include "([^"]+)"', lambda m: expand(path.parent / m[1]), text)
    text = expand(ROOT / 'config/corne.keymap')
    return re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)


def bindings(text):
    return [re.sub(r'\s+', ' ', value).strip() for value in re.findall(r'&\w+[^&]*', text)]


class KeymapTests(unittest.TestCase):
    def setUp(self):
        self.text = source()
        self.aliases = {name: int(value) for name, value in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*$', self.text, re.M)}
        self.layers = {name: bindings(body) for name, body in re.findall(r'(\w+_layer)\s*\{\s*bindings\s*=\s*<(.*?)>;', self.text, re.S)}
        self.combos = {name: body for name, body in re.findall(r'(combo_\w+)\s*\{([^}]+)\}', self.text)}

    def test_five_complete_layers_in_declared_priority_order(self):
        self.assertEqual(list(self.layers), ['default_layer', 'navigation_layer', 'symbol_layer', 'number_layer', 'system_layer'])
        self.assertEqual([self.aliases[k] for k in ('DEF', 'NAV', 'SYM', 'NUMB', 'SYS')], list(range(5)))
        self.assertTrue(all(len(layer) == 36 for layer in self.layers.values()))

    def test_every_physical_alias_has_a_unique_correct_position(self):
        expected = ['LT4 LT3 LT2 LT1 LT0 RT0 RT1 RT2 RT3 RT4', 'LM4 LM3 LM2 LM1 LM0 RM0 RM1 RM2 RM3 RM4', 'LB4 LB3 LB2 LB1 LB0 RB0 RB1 RB2 RB3 RB4', 'LH2 LH1 LH0 RH0 RH1 RH2']
        self.assertEqual([self.aliases[name] for row in expected for name in row.split()], list(range(36)))

    def test_base_letters_mods_and_six_thumb_actions_preserved(self):
        expected = ['&kp '+key for key in 'Q W E R T Y U I O P'.split()]
        expected += ['&hm LGUI A', '&hm LALT S', '&hm LCTRL D', '&hm LSHIFT F', '&kp G', '&kp H', '&kp J', '&kp K', '&kp L', '&mt LS(LC(LA(LGUI))) SEMICOLON']
        expected += ['&kp '+key for key in 'Z X C V B N M COMMA DOT SLASH'.split()]
        expected += ['&kp LCTRL', '&mo SYM', '&kp SPACE', '&kp ENTER', '&mo NUMB', '&kp BACKSPACE']
        self.assertEqual(self.layers['default_layer'], expected)
        self.assertRegex(self.text, r'tapping-term-ms\s*=\s*<400>')
        self.assertNotRegex(self.text, r'tapping-term\s*=')

    def test_combos_have_one_behavior_valid_positions_and_explicit_noncolliding_scopes(self):
        seen = []
        for name, body in self.combos.items():
            positions = tuple(sorted(self.aliases[token] for token in re.search(r'key-positions\s*=\s*<([^>]+)>', body)[1].split()))
            self.assertEqual(len(set(positions)), len(positions), name)
            self.assertTrue(all(0 <= p < 36 for p in positions), name)
            scope = set(re.search(r'layers\s*=\s*<([^>]+)>', body)[1].split())
            self.assertTrue(scope <= {'DEF', 'SYM', 'NAV', 'NUMB', 'SYS'}, name)
            self.assertEqual(len(bindings(re.search(r'bindings\s*=\s*<([^>]+)>', body)[1])), 1, name)
            for other_positions, other_scope in seen:
                self.assertFalse(positions == other_positions and scope & other_scope, name)
            seen.append((positions, scope))

    def test_added_letter_chords_are_guarded_against_typing_rolls(self):
        for name in ('combo_enter', 'combo_delete', 'combo_caps_word', 'combo_sys'):
            body = self.combos[name]
            self.assertRegex(body, r'layers\s*=\s*<DEF>')
            self.assertRegex(body, r'require-prior-idle-ms\s*=\s*<150>')
            self.assertRegex(body, r'timeout-ms\s*=\s*<35>')
        self.assertIn('&kp ENTER', self.combos['combo_enter'])
        self.assertIn('&kp DELETE', self.combos['combo_delete'])
        self.assertIn('&caps_word', self.combos['combo_caps_word'])

    def test_all_latched_layers_have_a_dedicated_base_escape(self):
        for name, layer in self.layers.items():
            if name != 'default_layer':
                self.assertEqual(layer[20], '&to DEF', name)
        self.assertIn('&to NAV', self.combos['combo_nav'])
        self.assertIn('&to SYS', self.combos['combo_sys'])

    def test_opposite_hand_symbols_and_numpad(self):
        sym = self.layers['symbol_layer']
        self.assertEqual([sym[i] for i in (6, 7, 16, 17, 26, 27)], ['&kp LBRC', '&kp RBRC', '&kp LPAR', '&kp RPAR', '&kp LBKT', '&kp RBKT'])
        num = self.layers['number_layer']
        self.assertEqual([num[i] for i in (1, 2, 3, 11, 12, 13, 21, 22, 23, 14)], ['&kp N'+n for n in '7894561230'])
        self.assertEqual(self.layers['navigation_layer'][15:19], ['&kp '+k for k in ('LEFT', 'DOWN', 'UP', 'RIGHT')])

    def test_gui_thumb_combo_survives_layer_activation_without_becoming_system(self):
        body = self.combos['combo_gui']
        self.assertIn('&kp LGUI', body)
        self.assertEqual(set(re.search(r'layers\s*=\s*<([^>]+)>', body)[1].split()), {'DEF', 'NAV', 'SYM', 'NUMB', 'SYS'})
        self.assertIn('LH1 RH1', body)

    def test_physical_layout_selects_the_actual_36_key_geometry(self):
        self.assertIn('zmk,physical-layout = &foostan_corne_5col_layout;', self.text)

    def test_build_targets_use_current_nice_nano_zmk_variant(self):
        matrix = (ROOT / 'build.yaml').read_text()
        self.assertEqual(re.findall(r'^\s+- board:\s*(\S+)', matrix, re.M), ['nice_nano//zmk', 'nice_nano//zmk'])

    def test_tmux_macros_use_individually_masked_prefix_and_command_taps(self):
        for name, key in (('tmux_previous', 'p'), ('tmux_next', 'n'), ('tmux_zoom', 'z')):
            match = re.search(name+r'\s*\{(.*?)\};', self.text, re.S)
            self.assertIsNotNone(match)
            body = match[1]
            self.assertIn('&macro_tap &tmux_prefix &tmux_'+key, body)
            self.assertNotIn('&macro_press', body)


if __name__ == '__main__':
    unittest.main()
