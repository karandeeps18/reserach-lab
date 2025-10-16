import typer
from typing import List
from qsentia.bronze.load_aggregates import load as load_agg
from qsentia.bronze.load_news import load as load_news
from qsentia.silver.normalize_aggregates import normalize as norm_agg
from qsentia.silver.normalize_news import normalize as norm_news

app = typer.Typer(help="QSentia pipeline CLI")

def _split_syms(s: str | None) -> List[str]:
    return [x.strip().upper() for x in s.split(",")] if s else []

@app.command()
def load_aggregates(symbols: str, start: str, end: str, timespan: str = "day"):
    total = 0
    for s in _split_syms(symbols):
        total += load_agg(s, start, end, timespan=timespan)
    typer.echo(f"Loaded {total} rows to bronze/aggregates")

@app.command()
def normalize_aggregates(start: str, end: str, symbols: str):
    n = norm_agg(start, end, _split_syms(symbols))
    typer.echo(f"Wrote {n} rows to silver/aggregates")

@app.command()
def load_news_cmd(symbols: str, start: str, end: str):
    total = 0
    for s in _split_syms(symbols):
        total += load_news(s, start, end)
    typer.echo(f"Loaded {total} rows to bronze/news")

@app.command()
def normalize_news_cmd(start: str, end: str, symbols: str):
    n = norm_news(start, end, _split_syms(symbols))
    typer.echo(f"Wrote {n} rows to silver/news")

if __name__ == "__main__":
    app()