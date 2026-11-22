"""Gabarit HTML commun à toutes les pages du portail."""

from html import escape

STYLE = """
body { font-family: system-ui, sans-serif; margin: 0; background: #f7f5f2; color: #222; }
header { background: #2d3a4a; color: #fff; padding: 12px 24px; }
header a { color: #fff; text-decoration: none; font-weight: 600; }
main { padding: 24px; max-width: 1000px; margin: auto; }
table { border-collapse: collapse; width: 100%; background: #fff; }
th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: left; }
th { background: #ece8e1; }
td.nombre { text-align: right; font-variant-numeric: tabular-nums; }
.carte { background: #fff; border: 1px solid #ddd; padding: 12px 16px; margin-bottom: 12px; }
.statut { font-size: 0.85em; color: #666; }
form { margin-bottom: 16px; }
"""


def page(titre: str, contenu: str) -> str:
    return f"""<!doctype html>
<html lang="fr">
<head><meta charset="utf-8"><title>{escape(titre)} - Portail Maison Lumière</title>
<style>{STYLE}</style></head>
<body>
<header><a href="/">Portail Maison Lumière</a></header>
<main>
<h1>{escape(titre)}</h1>
{contenu}
</main>
</body>
</html>"""


def tableau(colonnes: list[str], lignes: list[list], numeriques: set[int] | None = None) -> str:
    numeriques = numeriques or set()
    entete = "".join(f"<th>{escape(c)}</th>" for c in colonnes)
    corps = []
    for ligne in lignes:
        cellules = "".join(
            f'<td class="nombre">{escape(str(v))}</td>' if i in numeriques else f"<td>{escape(str(v))}</td>"
            for i, v in enumerate(ligne)
        )
        corps.append(f"<tr>{cellules}</tr>")
    return f"<table><thead><tr>{entete}</tr></thead><tbody>{''.join(corps)}</tbody></table>"
