import unittest

import numpy as np
import pandas as pd

from src.analysis.clutch import (
    add_clutch_flags, analysis_base, benjamini_hochberg, clock_to_seconds,
    distance_range, elapsed_seconds, two_proportion_ci,
)


def shot(game, period, clock, home="", away="", made=0, value=2, distance=10):
    return {
        "game_id": game, "season": 2025, "period": period, "clock": clock,
        "team_tricode": "AAA", "person_id": 1, "player_name": "Test",
        "sub_type": "Jump Shot", "shot_value": value, "shot_distance": distance,
        "score_home": home, "score_away": away, "is_made": made,
    }


class TestClutch(unittest.TestCase):

    def test_clock_to_seconds(self):
        s = clock_to_seconds(pd.Series(["PT04M59.00S", "PT00M03.50S", "PT12M00.00S"]))
        self.assertEqual(s.tolist(), [299.0, 3.5, 720.0])

    def test_elapsed_seconds(self):
        out = elapsed_seconds(np.array([1, 4, 5]), np.array([720.0, 0.0, 300.0]))
        self.assertEqual(out.tolist(), [0.0, 2880.0, 2880.0])

    def test_distance_range(self):
        r = distance_range(pd.Series([0, 4, 5, 14, 15, 24, 25, 40]))
        self.assertEqual(r.tolist(), ["0-4", "0-4", "5-14", "5-14",
                                      "15-24", "15-24", "25+", "25+"])

    def test_clutch_uses_previous_score(self):
        df = pd.DataFrame([
            shot("G1", 4, "PT06M00.00S", "90", "88", made=1),   # fuera de ventana
            shot("G1", 4, "PT04M00.00S"),                       # dif 2 -> clutch
            shot("G1", 4, "PT03M00.00S", "100", "88", made=1),  # usa marcador previo (dif 2)
            shot("G1", 4, "PT02M00.00S"),                       # dif 12 -> no clutch
        ])
        out = add_clutch_flags(df).sort_values("tiempo_transcurrido")
        self.assertEqual(out["clutch"].tolist(), [False, True, True, False])
        self.assertEqual(out["diferencia_estimada"].tolist()[1:], [2.0, 2.0, 12.0])

    def test_overtime_is_final_window(self):
        df = pd.DataFrame([
            shot("G2", 4, "PT00M10.00S", "100", "100", made=1),
            shot("G2", 5, "PT04M50.00S"),
        ])
        out = add_clutch_flags(df).sort_values("tiempo_transcurrido")
        self.assertTrue(out["ventana_final"].iloc[1])
        self.assertTrue(out["clutch"].iloc[1])

    def test_ambiguous_instants_and_unknown_score_excluded(self):
        df = pd.DataFrame([
            shot("G3", 1, "PT11M00.00S"),                      # sin marcador previo
            shot("G3", 1, "PT10M00.00S", "2", "0", made=1),    # tampoco tiene previo
            shot("G3", 1, "PT09M00.00S"),                      # mismo instante x2
            shot("G3", 1, "PT09M00.00S"),
            shot("G3", 1, "PT08M00.00S"),                      # unico valido
        ])
        base = analysis_base(add_clutch_flags(df))
        self.assertEqual(len(base), 1)
        self.assertEqual(base["clock"].iloc[0], "PT08M00.00S")

    def test_two_proportion_ci(self):
        diff, lo, hi = two_proportion_ci(40, 100, 50, 100)
        self.assertAlmostEqual(diff, -0.10)
        self.assertLess(lo, diff)
        self.assertGreater(hi, diff)

    def test_benjamini_hochberg(self):
        q = benjamini_hochberg([0.01, 0.04, 0.03, 0.20])
        np.testing.assert_allclose(q, [0.04, 0.0533333, 0.0533333, 0.20], rtol=1e-4)


if __name__ == "__main__":
    unittest.main()
