from simulators.refined_simulator import CraftProject, Atelier, CraftGame, Crafter
from simulators.card_templates import *  # noqa: F403

from collections import Counter

import typing as T


def atelier():
    return Atelier(lane_size=7, reserve_size=3, damage_resistance=80)


def mid_craft_project():
    return CraftProject(
        products_tpls=[
            (product_card_template_40, 3),  # noqa: F405
        ],
        materias_tpls=[
            (materia_card_template_50, 6),  # noqa: F405
        ],
        defaults_tpls=[(default_card_template_50, 30), (default_card_template_70, 20), (default_card_template_90, 10), (default_card_template_100, 3)],  # noqa: F405
        tools_tpls=[],
    )


def iterate_game(count=200) -> T.Iterable:
    summaries = []
    project = mid_craft_project()
    crafter = Crafter(craft_skill=60, base_endurance=25, base_skill_modifier=0)
    craft_game = CraftGame(
        project=project,
        crafter=crafter,
        atelier=atelier(),
    )
    for _ in range(count):
        craft_game.start()
        craft_game.play_game()
        summaries.append(craft_game.summary())
    return summaries


def export_csv(summaries):
    raise NotImplementedError


if __name__ == "__main__":
    summaries = iterate_game()
    c = Counter(summary.success for summary in summaries)
    print(sorted([(i, round(c[i] / c.total() * 100.0, 2)) for i in c]))

