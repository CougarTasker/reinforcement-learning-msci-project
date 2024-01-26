"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent

src = root / "src"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(root).with_suffix("")
    doc_path = Path("reference") / path.relative_to(src).with_suffix(".md")

    parts = tuple(module_path.parts)
    nav_parts = tuple(
        [
            part.replace("_", " ").title()
            for part in doc_path.with_suffix("").parts
        ]
    )

    if parts[-1] == "__init__":
        parts = parts[:-1]
        nav_parts = nav_parts[:-1]
        doc_path = doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[nav_parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(doc_path, path)

with mkdocs_gen_files.open("SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
