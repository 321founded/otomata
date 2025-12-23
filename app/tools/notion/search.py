#!/usr/bin/env python3
"""
Search Notion workspace for pages and databases.

Usage:
    python3 search.py --query "project management"
    python3 search.py --query "tasks" --filter page
    python3 search.py --query "database" --filter database --sort last_edited_time
"""
import json
import sys
from pathlib import Path
from typing_extensions import Annotated
import typer

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from notion_client import NotionClient

app = typer.Typer(help="Search Notion workspace")


@app.command()
def main(
    query: Annotated[str, typer.Option(help="Search query")],
    filter: Annotated[str, typer.Option(help="Filter by type (page or database)")] = None,
    sort: Annotated[str, typer.Option(help="Sort results by (relevance or last_edited_time)")] = "relevance",
    output: Annotated[str, typer.Option(help="Output file path (JSON)")] = None,
):
    if filter and filter not in ['page', 'database']:
        print("Error: filter must be 'page' or 'database'", file=sys.stderr)
        raise typer.Exit(1)

    if sort not in ['relevance', 'last_edited_time']:
        print("Error: sort must be 'relevance' or 'last_edited_time'", file=sys.stderr)
        raise typer.Exit(1)

    try:
        client = NotionClient()
        print(f"Searching Notion for: '{query}'...")

        if filter:
            print(f"   Filter: {filter}")
        if sort != 'relevance':
            print(f"   Sort: {sort}")

        result = client.search(query=query, filter_type=filter, sort=sort)

        results = result.get('results', [])
        print(f"\n✓ Found {len(results)} result(s)\n")

        for i, item in enumerate(results, 1):
            obj_type = item['object']
            item_id = item['id']

            if obj_type == 'page':
                title_prop = item.get('properties', {}).get('title', {})
                title_array = title_prop.get('title', [])
                title = title_array[0]['plain_text'] if title_array else '(Untitled)'
            else:
                title_array = item.get('title', [])
                title = title_array[0]['plain_text'] if title_array else '(Untitled)'

            last_edited = item.get('last_edited_time', 'N/A')
            url = item.get('url', '')

            print(f"{i}. [{obj_type.upper()}] {title}")
            print(f"   ID: {item_id}")
            print(f"   Last edited: {last_edited}")
            print(f"   URL: {url}\n")

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Results saved to: {output}")

        print("\n" + "="*60)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise typer.Exit(1)


if __name__ == '__main__':
    app()
