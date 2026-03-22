import importlib
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class PageSpec:
    title: str
    icon: str
    module_path: str
    render_function: str


class PageRegistry:
    def __init__(self) -> None:
        self._pages: dict[str, PageSpec] = {}

    def register(self, page: PageSpec) -> None:
        self._pages[page.title] = page

    def list_titles(self) -> list[str]:
        return list(self._pages.keys())

    def list_icons(self) -> list[str]:
        return [page.icon for page in self._pages.values()]

    def get(self, title: str) -> PageSpec:
        if title not in self._pages:
            available = ", ".join(self.list_titles())
            raise KeyError(f"Pagina '{title}' nao encontrada. Disponiveis: {available}")
        return self._pages[title]

    def load_renderer(self, title: str) -> Callable[[], None]:
        page = self.get(title)
        module = importlib.import_module(page.module_path)
        return getattr(module, page.render_function)


registry = PageRegistry()

for page in (
    PageSpec("Home", "house", "paginas.welcome", "render_welcome"),
    PageSpec("Post Agent", "file-earmark-text", "paginas.post", "render_post_page"),
    PageSpec("Summary PDF", "cloud-upload", "paginas.upload_pdf", "render_upload_page"),
    PageSpec("Pesquisador PDF", "cloud-upload", "paginas.upload2_pdf", "render_upload_page2"),
    PageSpec("PubMed Agent", "search", "paginas.pubmed", "render_pubmed_page"),
):
    registry.register(page)


def list_page_titles() -> list[str]:
    return registry.list_titles()


def list_page_icons() -> list[str]:
    return registry.list_icons()


def load_page_renderer(title: str) -> Callable[[], None]:
    return registry.load_renderer(title)
