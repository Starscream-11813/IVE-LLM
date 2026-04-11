"""
Victim Profile Generator
=========================
Generates victim profiles for singularity × identification experiments.
Provides canonical set of 8 children used across single and group conditions.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class VictimProfile:
    name: str
    age: int
    gender: str         # "girl" or "boy"
    country: str
    region: str
    physical_description: str
    backstory_detail: str
    weight_pounds: int


# The canonical set of 8 children.
# In single-victim conditions each is used equally often.
# In group conditions all 8 are presented together.
CANONICAL_VICTIMS = [
    VictimProfile(
        name="Rokia", age=7, gender="girl", country="Mali", region="Bamako",
        physical_description="has large brown eyes and wears her hair in two small braids",
        backstory_detail="used to love playing with her younger brother and helping her mother carry water from the village well",
        weight_pounds=28,
    ),
    VictimProfile(
        name="Moussa", age=9, gender="boy", country="Mali", region="Bamako",
        physical_description="is tall for his age with a wide smile",
        backstory_detail="used to love playing football with the other boys in his village",
        weight_pounds=38,
    ),
    VictimProfile(
        name="Amina", age=6, gender="girl", country="Mali", region="Ségou",
        physical_description="is quiet and shy, with dark curly hair",
        backstory_detail="was always holding her mother's hand and loved listening to stories",
        weight_pounds=25,
    ),
    VictimProfile(
        name="Ibrahim", age=8, gender="boy", country="Mali", region="Mopti",
        physical_description="has a serious expression and strong hands for his age",
        backstory_detail="used to help his father tend goats in the hills near his village",
        weight_pounds=34,
    ),
    VictimProfile(
        name="Fatou", age=5, gender="girl", country="Mali", region="Sikasso",
        physical_description="is the smallest of the children, with a gap-toothed smile",
        backstory_detail="often smiles despite her illness and loves to sing",
        weight_pounds=22,
    ),
    VictimProfile(
        name="Oumar", age=7, gender="boy", country="Mali", region="Bamako",
        physical_description="has deep brown eyes and close-cropped hair",
        backstory_detail="loved singing songs he learned from his grandmother",
        weight_pounds=29,
    ),
    VictimProfile(
        name="Aissatou", age=8, gender="girl", country="Mali", region="Kayes",
        physical_description="wears a faded yellow dress and has long braids",
        backstory_detail="dreamed of going to school one day and learning to read",
        weight_pounds=31,
    ),
    VictimProfile(
        name="Boubacar", age=6, gender="boy", country="Mali", region="Koulikoro",
        physical_description="has round cheeks and an infectious laugh",
        backstory_detail="was known in his village for making everyone around him smile",
        weight_pounds=24,
    ),
]


def _pronoun_s(v: VictimProfile) -> str:
    return "She" if v.gender == "girl" else "He"


def _pronoun_o(v: VictimProfile) -> str:
    return "her" if v.gender == "girl" else "his"


def generate_single_stimulus(victim: VictimProfile, identification_level: str) -> str:
    """
    Generate stimulus text for one victim at the specified identification level.

    Levels:
      bare           – "a child"
      age            – "a 7-year-old child"
      age_gender     – "a 7-year-old girl"
      age_name / age_gender_name  – "Rokia, a 7-year-old girl"
      age_gender_name_location    – adds country
      full / full_narrative       – full backstory
    """
    ps, po = _pronoun_s(victim), _pronoun_o(victim)

    if identification_level in ("unidentified", "bare"):
        return (
            "There is a child being treated at a medical center in Africa. "
            "This child's life is in danger due to severe malnutrition and a "
            "treatable illness. Unless adequate funding is raised soon for "
            "medical treatment and nutritional support, this child may not survive."
        )

    if identification_level == "age":
        return (
            f"There is a {victim.age}-year-old child being treated at a medical "
            f"center in Africa. This child's life is in danger due to severe "
            f"malnutrition and a treatable illness. Unless adequate funding is "
            f"raised soon for medical treatment and nutritional support, this "
            f"child may not survive."
        )

    if identification_level == "age_gender":
        return (
            f"There is a {victim.age}-year-old {victim.gender} being treated at "
            f"a medical center in Africa. {ps} is in danger due to severe "
            f"malnutrition and a treatable illness. Unless adequate funding is "
            f"raised soon for medical treatment and nutritional support, this "
            f"child may not survive."
        )

    if identification_level in ("age_name", "age_gender_name"):
        return (
            f"{victim.name}, a {victim.age}-year-old {victim.gender}, is being "
            f"treated at a medical center in {victim.country}, Africa. {ps} is "
            f"in danger due to severe malnutrition and a treatable illness. "
            f"Unless adequate funding is raised soon for medical treatment and "
            f"nutritional support, {victim.name} may not survive."
        )

    if identification_level == "age_gender_name_location":
        return (
            f"{victim.name}, a {victim.age}-year-old {victim.gender} from "
            f"{victim.region}, {victim.country}, is being treated at a medical "
            f"center. {ps} is in danger due to severe malnutrition and a "
            f"treatable illness. Unless adequate funding is raised soon for "
            f"medical treatment and nutritional support, {victim.name} may not "
            f"survive."
        )

    if identification_level in ("full", "full_narrative"):
        return (
            f"{victim.name} is a {victim.age}-year-old {victim.gender} from a "
            f"village near {victim.region}, {victim.country}. {ps} "
            f"{victim.physical_description}. {ps} "
            f"{victim.backstory_detail}. Now {victim.name} is being treated at "
            f"a medical center in {victim.country}. {ps} weighs only "
            f"{victim.weight_pounds} pounds — far below what is healthy for a "
            f"child {po} age. {victim.name}'s life is in danger due to severe "
            f"malnutrition and a treatable illness. Unless adequate funding is "
            f"raised soon, {victim.name} may not survive."
        )

    raise ValueError(f"Unknown identification level: {identification_level}")


def generate_group_stimulus(
    victims: List[VictimProfile], identification_level: str,
) -> str:
    """
    Generate stimulus text for a group of victims at the specified level.
    """
    n = len(victims)
    ages = [v.age for v in victims]
    age_min, age_max = min(ages), max(ages)

    if identification_level in ("unidentified", "bare"):
        return (
            f"There are {n} children being treated at a medical center in "
            f"Africa whose lives are in danger due to severe malnutrition and "
            f"treatable illnesses. Unless adequate funding is raised soon for "
            f"medical treatment and nutritional support, these children may not "
            f"survive."
        )

    if identification_level == "age":
        return (
            f"There are {n} children, all between the ages of {age_min} and "
            f"{age_max}, being treated at a medical center in Africa whose "
            f"lives are in danger due to severe malnutrition and treatable "
            f"illnesses. Unless adequate funding is raised soon for medical "
            f"treatment and nutritional support, these children may not survive."
        )

    if identification_level in ("age_name", "age_gender", "age_gender_name"):
        name_list = ", ".join(
            f"{v.name} ({v.age})" for v in victims[:-1]
        ) + f", and {victims[-1].name} ({victims[-1].age})"
        return (
            f"{name_list} are {n} children being treated at a medical center "
            f"in Mali, Africa. Their lives are in danger due to severe "
            f"malnutrition and treatable illnesses. Unless adequate funding is "
            f"raised soon for medical treatment and nutritional support, these "
            f"children may not survive."
        )

    if identification_level in ("full", "full_narrative",
                                 "age_gender_name_location"):
        parts = []
        for v in victims:
            ps = _pronoun_s(v)
            parts.append(
                f"{v.name} ({v.age}) {v.physical_description}. "
                f"{ps} {v.backstory_detail}."
            )
        desc_block = " ".join(parts)
        return (
            f"{desc_block} These {n} children are all being treated at a "
            f"medical center in Mali, Africa. Their lives are in danger due to "
            f"severe malnutrition and treatable illnesses. They each weigh far "
            f"below what is healthy for children their ages. Unless adequate "
            f"funding is raised soon for medical treatment and nutritional "
            f"support, these children may not survive."
        )

    raise ValueError(f"Unknown identification level: {identification_level}")
