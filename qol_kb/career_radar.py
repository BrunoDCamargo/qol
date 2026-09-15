from datetime import date
from pathlib import Path
from typing import Any

import yaml


ORGANIZATION_TYPES = frozenset(
    {
        "company",
        "ict",
        "research-institute",
        "university",
        "public-agency",
        "nonprofit",
        "foundation",
        "startup",
        "other",
    }
)
SOURCE_TYPES = frozenset(
    {
        "public-jobs",
        "research-funding",
        "academic-opportunities",
        "rd-network",
        "mixed-opportunities",
        "contract-research-opportunities",
        "other",
    }
)
WORK_MODES = frozenset({"onsite", "hybrid", "remote-brazil"})

# AMEP: https://www.amep.pr.gov.br/FAQ/Municipios-da-Regiao-Metropolitana-de-Curitiba
RMC_CITIES = frozenset(
    name.casefold()
    for name in {
        "Curitiba",
        "Adrianópolis",
        "Agudos do Sul",
        "Almirante Tamandaré",
        "Araucária",
        "Balsa Nova",
        "Bocaiúva do Sul",
        "Campina Grande do Sul",
        "Campo do Tenente",
        "Campo Largo",
        "Campo Magro",
        "Cerro Azul",
        "Colombo",
        "Contenda",
        "Doutor Ulysses",
        "Fazenda Rio Grande",
        "Itaperuçu",
        "Lapa",
        "Mandirituba",
        "Piên",
        "Pinhais",
        "Piraquara",
        "Quatro Barras",
        "Quitandinha",
        "Rio Branco do Sul",
        "Rio Negro",
        "São José dos Pinhais",
        "Tijucas do Sul",
        "Tunas do Paraná",
    }
)


def _load_list(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"{path}: required Career Radar file is missing")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"{path}: {error}") from error
    if data is None:
        return []
    if not isinstance(data, list):
        raise ValueError(f"{path}: top-level value must be a list")
    for index, record in enumerate(data):
        if not isinstance(record, dict):
            raise ValueError(f"{path}[{index}]: record must be a mapping")
    return data


def _text(record: dict[str, Any], key: str, label: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}.{key}: non-blank string is required")
    return value.strip()


def _validate_date(value: Any, label: str) -> None:
    if type(value) is date:
        return
    if isinstance(value, str):
        try:
            if date.fromisoformat(value).isoformat() == value:
                return
        except ValueError:
            pass
    raise ValueError(f"{label}.last_checked: YYYY-MM-DD date is required")


def _check_unique_ids(records: list[dict[str, Any]], kind: str) -> None:
    seen: set[str] = set()
    for index, record in enumerate(records):
        identifier = _text(record, "id", f"{kind}[{index}]")
        if identifier in seen:
            raise ValueError(f"duplicate {kind} id: {identifier}")
        seen.add(identifier)


def _validate_tags(record: dict[str, Any], label: str) -> None:
    if "tags" not in record:
        return
    tags = record["tags"]
    if not isinstance(tags, list):
        raise ValueError(f"{label}.tags: list is required")
    for index, tag in enumerate(tags):
        if not isinstance(tag, str) or not tag.strip():
            raise ValueError(f"{label}.tags[{index}]: non-blank string is required")


def _validate_organization(record: dict[str, Any], index: int) -> None:
    label = f"organization[{index}]"
    _text(record, "id", label)
    _text(record, "name", label)

    organization_type = _text(record, "organization_type", label)
    if organization_type not in ORGANIZATION_TYPES:
        raise ValueError(f"{label}.organization_type: invalid value {organization_type!r}")

    location = record.get("location")
    if not isinstance(location, dict):
        raise ValueError(f"{label}.location: mapping is required")
    _text(location, "country", f"{label}.location")

    modes = record.get("viable_from_curitiba")
    if not isinstance(modes, list) or not modes:
        raise ValueError(f"{label}.viable_from_curitiba: non-empty list is required")
    if any(mode not in WORK_MODES for mode in modes):
        raise ValueError(f"{label}.viable_from_curitiba: invalid work mode")

    local_mode = any(mode in {"onsite", "hybrid"} for mode in modes)
    if local_mode:
        city = _text(location, "city", f"{label}.location")
        state = _text(location, "state", f"{label}.location")
    else:
        city = location.get("city", "")
        state = location.get("state", "")
        if not isinstance(city, str) or not isinstance(state, str):
            raise ValueError(f"{label}.location: city and state must be strings when provided")
        city = city.strip()
        state = state.strip()

    in_rmc = state.casefold() == "pr" and city.casefold() in RMC_CITIES
    if not in_rmc and "remote-brazil" not in modes:
        raise ValueError(f"{label}.viable_from_curitiba: remote-brazil is required outside RMC")
    if not in_rmc and local_mode:
        raise ValueError(f"{label}.viable_from_curitiba: onsite or hybrid is only valid in RMC")

    rd_evidence = record.get("rd_evidence")
    if not isinstance(rd_evidence, dict):
        raise ValueError(f"{label}.rd_evidence: mapping is required")
    _text(rd_evidence, "url", f"{label}.rd_evidence")
    _text(rd_evidence, "note", f"{label}.rd_evidence")

    for key in ("careers_url", "jobs_url"):
        if key in record and record[key] is not None:
            _text(record, key, label)
    if not any(
        isinstance(record.get(key), str) and record[key].strip()
        for key in ("careers_url", "jobs_url")
    ):
        raise ValueError(f"{label}: careers_url or jobs_url is required")

    _validate_tags(record, label)
    _validate_date(record.get("last_checked"), label)


def _validate_source(record: dict[str, Any], index: int) -> None:
    label = f"source[{index}]"
    _text(record, "id", label)
    _text(record, "name", label)
    source_type = _text(record, "source_type", label)
    if source_type not in SOURCE_TYPES:
        raise ValueError(f"{label}.source_type: invalid value {source_type!r}")
    _text(record, "url", label)
    _text(record, "scope", label)
    _validate_date(record.get("last_checked"), label)


def validate_career_radar(root: str | Path = ".") -> None:
    root_path = Path(root)
    radar_path = root_path / "career-radar"
    organizations = _load_list(radar_path / "organizations.yaml")
    for expansion_path in sorted(radar_path.glob("organizations-expansion-*.yaml")):
        organizations.extend(_load_list(expansion_path))
    sources = _load_list(radar_path / "sources.yaml")

    _check_unique_ids(organizations, "organization")
    _check_unique_ids(sources, "source")

    for index, organization in enumerate(organizations):
        _validate_organization(organization, index)
    for index, source in enumerate(sources):
        _validate_source(source, index)
