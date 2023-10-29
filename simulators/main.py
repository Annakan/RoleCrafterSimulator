from math import trunc

from simulators.refined_simulator import (
    CraftProject,
    Atelier,
    CraftGame,
    Crafter,
    GameSummary,
)
from simulators.card_templates import *  # noqa: F403

from collections import Counter

import typing as T


def mid_craft_project():
    return CraftProject(
        products_tpls=[
            (product_card_template_60, 5),
            (product_card_template_50, 3),  # noqa: F405
        ],
        materias_tpls=[
            (materia_card_template_60, 6),
            (materia_card_template_50, 6),  # noqa: F405
        ],
        defaults_tpls=[
            (default_card_template_70, 20),
            (default_card_template_80, 15),
            # (default_card_template_90, 0),
            # (default_card_template_100, 0),
            # (default_card_template_120, 0),
        ],  # noqa: F405
        tools_tpls=[],
    )


def iterate_game(
    project: CraftProject,
    crafter: Crafter,
    atelier: Atelier,
    count=200,
) -> T.Iterable[GameSummary]:
    summaries = []
    craft_game = CraftGame(
        project=project,
        crafter=crafter,
        atelier=atelier,
        generous_rolls=False,
    )
    for _ in range(count):
        craft_game.start()
        craft_game.play_game()
        summaries.append(craft_game.summary())
    return summaries


def export_csv(summaries):
    raise NotImplementedError


def mean_of(summaries, field):
    return trunc(sum(getattr(s, field) for s in summaries) / len(summaries))


def evaluate_parameters(count=300) -> T.Iterable:
    project = mid_craft_project()
    crafter = Crafter(craft_skill=95, base_endurance=20, base_skill_modifier=0)
    atelier = Atelier(lane_size=7, reserve_size=3, damage_resistance=80)
    full_summaries: list[GameSummary] = []
    for lane_size in range(3, 8):
        for endurance in range(15, 26):
            atelier.lane_size = lane_size
            crafter.base_endurance = endurance
            print(f"lane_size: {atelier.lane_size} Endurance: {endurance} : ", end="")
            summaries = iterate_game(
                project=project,
                crafter=crafter,
                atelier=atelier,
                count=count,
            )
            c = Counter(summary.success for summary in summaries)
            mean_defauts = mean_of(summaries, "product_default_value")
            mean_defauts_count = mean_of(summaries, "product_default_count")
            mean_overflowed_count = (summaries, "overflowed_count")
            print(
                sorted([(i, round(c[i] / c.total() * 100.0, 0)) for i in c]),
                mean_defauts,
                mean_defauts_count,
                mean_overflowed_count
            )
            full_summaries.extend(summaries)
    return full_summaries


if __name__ == "__main__":
    evaluate_parameters()
