import unittest
import pandas as pd

from src.processing.build_dataset import (
    prepare_shots,
    aggregate_shots,
)


def example_data():
    return pd.DataFrame([
        {
            "game_id": "001",
            "season": "2023-24",
            "season_type_id": 2,
            "period": 1,
            "clock": "PT11M30.00S",
            "team_tricode": " bos ",
            "player_name": "Jugador A",
            "shot_result": "Made",
            "shot_value": 3,
            "shot_distance": 25,
            "x_legacy": 20,
            "y_legacy": 50,
        },
        {
            "game_id": "001",
            "season": "2023-24",
            "season_type_id": 2,
            "period": 1,
            "clock": "PT10M30.00S",
            "team_tricode": "BOS",
            "player_name": "Jugador B",
            "shot_result": "Missed",
            "shot_value": 2,
            "shot_distance": 3,
            "x_legacy": 0,
            "y_legacy": 10,
        },
    ])


class TestProcessing(unittest.TestCase):

    def test_cleaning_and_points(self):
        clean, summary = prepare_shots(
            example_data(), 2024
        )

        self.assertEqual(len(clean), 2)
        self.assertEqual(int(clean["is_made"].sum()), 1)
        self.assertEqual(
            int(clean["points_scored"].sum()), 3
        )
        self.assertTrue(
            clean["team_tricode"].eq("BOS").all()
        )

    def test_exact_duplicates(self):
        df = example_data()
        df = pd.concat(
            [df, df.iloc[[0]]], ignore_index=True
        )

        clean, summary = prepare_shots(df, 2024)

        self.assertEqual(summary["exact_duplicates"], 1)
        self.assertEqual(len(clean), 2)

    def test_missing_columns(self):
        df = example_data().drop(
            columns=["shot_distance"]
        )

        with self.assertRaises(ValueError):
            prepare_shots(df, 2024)

    def test_unknown_result(self):
        df = example_data()
        df.loc[0, "shot_result"] = "Unknown"

        with self.assertRaises(ValueError):
            prepare_shots(df, 2024)

    def test_aggregation(self):
        clean, _ = prepare_shots(
            example_data(), 2024
        )

        result = aggregate_shots(
            clean, ["team_tricode"]
        )

        self.assertEqual(int(result["attempts"].iloc[0]), 2)
        self.assertEqual(int(result["makes"].iloc[0]), 1)
        self.assertEqual(
            float(result["points_per_attempt"].iloc[0]),
            1.5,
        )


if __name__ == "__main__":
    unittest.main()
