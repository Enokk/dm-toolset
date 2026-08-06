from collections import defaultdict

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from dm_toolset_backend.core.db import DBSessionDep
from dm_toolset_backend.models import (
    ArmorCategory,
    Character,
    ClassProficiency,
    ProficienciesPublic,
    ProficiencyEntry,
    ProficiencyKind,
    ProficiencySource,
    RaceProficiency,
    SubclassProficiency,
    Weapon,
    WeaponCategory,
    WeaponType,
)

router = APIRouter(prefix="/characters/{character_id}/proficiencies", tags=["proficiencies"])

WEAPON_CATEGORY_LABELS: dict[WeaponCategory, str] = {
    WeaponCategory.SIMPLE: "Armi semplici",
    WeaponCategory.MARTIAL: "Armi da guerra",
}

ARMOR_CATEGORY_LABELS: dict[ArmorCategory, str] = {
    ArmorCategory.LIGHT: "Armature leggere",
    ArmorCategory.MEDIUM: "Armature medie",
    ArmorCategory.HEAVY: "Armature pesanti",
    ArmorCategory.SHIELD: "Scudi",
}

WEAPON_CATEGORY_ORDER: dict[WeaponCategory, int] = {
    WeaponCategory.SIMPLE: 0,
    WeaponCategory.MARTIAL: 1,
}

WEAPON_TYPE_ORDER: dict[WeaponType, int] = {
    WeaponType.MELEE: 0,
    WeaponType.RANGED: 1,
}

ARMOR_CATEGORY_ORDER: dict[ArmorCategory, int] = {
    ArmorCategory.LIGHT: 0,
    ArmorCategory.MEDIUM: 1,
    ArmorCategory.HEAVY: 2,
    ArmorCategory.SHIELD: 3,
}

# When the same grant (identical weapon/category) comes from more than one
# source, we show only one row, attributed to whichever source confers it
# latest in a character's build (race is fixed at creation, subclass is
# chosen last) — that's the most specific/interesting source to surface.
SOURCE_ORDER: dict[ProficiencySource, int] = {"race": 0, "class": 1, "subclass": 2}


# A grant row is either kind=WEAPON (weapon_id xor weapon_category set) or
# kind=ARMOR (armor_category set); weapon_names resolves weapon_id -> display name.
def _resolve_entry(
    row: RaceProficiency | ClassProficiency | SubclassProficiency,
    source: ProficiencySource,
    weapon_names: dict[int, str],
) -> tuple[ProficiencyKind, ProficiencyEntry]:
    if row.kind == ProficiencyKind.WEAPON:
        if row.weapon_id is not None:
            entry = ProficiencyEntry(name=weapon_names[row.weapon_id], is_category=False, source=source)
        else:
            assert row.weapon_category is not None
            entry = ProficiencyEntry(name=WEAPON_CATEGORY_LABELS[row.weapon_category], is_category=True, source=source)
    else:
        assert row.armor_category is not None
        entry = ProficiencyEntry(name=ARMOR_CATEGORY_LABELS[row.armor_category], is_category=True, source=source)
    return row.kind, entry


@router.get("/", response_model=ProficienciesPublic)
def get_character_proficiencies(character_id: int, session: DBSessionDep) -> ProficienciesPublic:
    character = session.get(Character, character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="character_not_found")

    race_rows = session.exec(
        select(RaceProficiency).where(RaceProficiency.character_race_id == character.character_race_id)
    ).all()
    class_rows = session.exec(
        select(ClassProficiency).where(
            ClassProficiency.character_class_id == character.character_class_id,
            ClassProficiency.min_level <= character.level,
        )
    ).all()
    subclass_rows = (
        session.exec(
            select(SubclassProficiency).where(
                SubclassProficiency.character_subclass_id == character.character_subclass_id,
                SubclassProficiency.min_level <= character.level,
            )
        ).all()
        if character.character_subclass_id is not None
        else []
    )

    rows_with_source: list[tuple[RaceProficiency | ClassProficiency | SubclassProficiency, ProficiencySource]] = (
        [(row, "race") for row in race_rows]
        + [(row, "class") for row in class_rows]
        + [(row, "subclass") for row in subclass_rows]
    )

    weapon_ids = {row.weapon_id for row, _ in rows_with_source if row.weapon_id is not None}
    weapon_rows = (
        session.exec(
            select(Weapon.id, Weapon.name, Weapon.category, Weapon.weapon_type).where(Weapon.id.in_(weapon_ids))
        ).all()
        if weapon_ids
        else []
    )
    weapon_names = {w.id: w.name for w in weapon_rows}
    weapon_categories = {w.id: w.category for w in weapon_rows}
    weapon_types = {w.id: w.weapon_type for w in weapon_rows}

    # Merge identical grants (same weapon/category) coming from multiple
    # sources into a single row, keeping only the latest source.
    representative: dict[tuple, RaceProficiency | ClassProficiency | SubclassProficiency] = {}
    sources_by_grant: dict[tuple, list[ProficiencySource]] = defaultdict(list)
    for row, source in rows_with_source:
        key = (row.kind, row.weapon_id, row.weapon_category, row.armor_category)
        representative[key] = row
        sources_by_grant[key].append(source)

    merged_rows = [
        (representative[key], max(sources, key=SOURCE_ORDER.__getitem__))
        for key, sources in sources_by_grant.items()
    ]

    # A blanket category grant (e.g. "Armi da guerra") makes any individually
    # named weapon of that same category redundant, regardless of which
    # source granted the named weapon — drop it rather than show both.
    granted_weapon_categories = {
        row.weapon_category
        for row, _ in merged_rows
        if row.kind == ProficiencyKind.WEAPON and row.weapon_category is not None
    }
    final_rows = [
        (row, source)
        for row, source in merged_rows
        if not (
            row.kind == ProficiencyKind.WEAPON
            and row.weapon_id is not None
            and weapon_categories[row.weapon_id] in granted_weapon_categories
        )
    ]

    weapon_rows_final = [(row, source) for row, source in final_rows if row.kind == ProficiencyKind.WEAPON]
    armor_rows_final = [(row, source) for row, source in final_rows if row.kind == ProficiencyKind.ARMOR]

    # Category grant first, then named weapons grouped by melee/ranged, alphabetically within each group.
    def _weapon_sort_key(row: RaceProficiency | ClassProficiency | SubclassProficiency) -> tuple:
        if row.weapon_id is None:
            assert row.weapon_category is not None
            return (WEAPON_CATEGORY_ORDER[row.weapon_category], 0, 0, "")
        category = weapon_categories[row.weapon_id]
        return (
            WEAPON_CATEGORY_ORDER[category],
            1,
            WEAPON_TYPE_ORDER[weapon_types[row.weapon_id]],
            weapon_names[row.weapon_id],
        )

    weapon_rows_final.sort(key=lambda item: _weapon_sort_key(item[0]))
    armor_rows_final.sort(key=lambda item: ARMOR_CATEGORY_ORDER[item[0].armor_category])

    return ProficienciesPublic(
        weapons=[_resolve_entry(row, source, weapon_names)[1] for row, source in weapon_rows_final],
        armor=[_resolve_entry(row, source, weapon_names)[1] for row, source in armor_rows_final],
    )
