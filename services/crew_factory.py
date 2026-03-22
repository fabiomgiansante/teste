import importlib
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CrewSpec:
    key: str
    module_path: str
    class_name: str
    description: str = ""


class CrewRegistry:
    def __init__(self) -> None:
        self._specs: dict[str, CrewSpec] = {}

    def register(self, spec: CrewSpec) -> None:
        self._specs[spec.key] = spec

    def get(self, key: str) -> CrewSpec:
        if key not in self._specs:
            available = ", ".join(sorted(self._specs.keys()))
            raise KeyError(f"Crew '{key}' nao registrada. Disponiveis: {available}")
        return self._specs[key]

    def list(self) -> list[CrewSpec]:
        return sorted(self._specs.values(), key=lambda spec: spec.key)

    def create(self, key: str, **kwargs: Any) -> Any:
        spec = self.get(key)
        module = importlib.import_module(spec.module_path)
        crew_class = getattr(module, spec.class_name)
        return crew_class(**kwargs)


registry = CrewRegistry()


def register_default_crews() -> None:
    defaults = [
        CrewSpec(
            key="post_agent",
            module_path="crews.post_crew",
            class_name="CrewPostagem",
            description="Crew para pesquisa e escrita de postagem.",
        ),
        CrewSpec(
            key="pdf_summary",
            module_path="crews.pdf_resumo_crew",
            class_name="CrewPDFResumo",
            description="Crew para resumo de PDF.",
        ),
        CrewSpec(
            key="pdf_research",
            module_path="crews.pesquisador_crew",
            class_name="CrewPDFResumo",
            description="Crew para analise cientifica estruturada de PDF.",
        ),
    ]

    for spec in defaults:
        registry.register(spec)


register_default_crews()


def create_crew(key: str, **kwargs: Any) -> Any:
    return registry.create(key, **kwargs)

