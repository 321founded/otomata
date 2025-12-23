#!/usr/bin/env python3
"""
Append blocks to Notion page.

Usage:
    python3 append_blocks.py --page_id abc123 --text "New paragraph"
    python3 append_blocks.py --page_id abc123 --markdown "## Heading\nContent"
    python3 append_blocks.py --page_id abc123 --markdown-file file.md
"""
import json
import re
import sys
from pathlib import Path
from typing_extensions import Annotated
import typer

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from notion_client import NotionClient

app = typer.Typer(help="Append blocks to Notion page")


def parse_markdown_to_blocks(markdown_text):
    blocks = []
    lines = markdown_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:].strip()}}]
                }
            })
            i += 1
            continue

        if line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:].strip()}}]
                }
            })
            i += 1
            continue

        if line.startswith('- '):
            rich_text = parse_inline_formatting(line[2:].strip())
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": rich_text}
            })
            i += 1
            continue

        if re.match(r'^\d+\.\s', line):
            content = re.sub(r'^\d+\.\s', '', line)
            rich_text = parse_inline_formatting(content)
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": rich_text}
            })
            i += 1
            continue

        rich_text = parse_inline_formatting(line)
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": rich_text}
        })
        i += 1

    return blocks


def parse_inline_formatting(text):
    rich_text = []
    parts = re.split(r'(\*\*[^*]+\*\*)', text)

    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            content = part[2:-2]
            rich_text.append({
                "type": "text",
                "text": {"content": content},
                "annotations": {"bold": True}
            })
        else:
            rich_text.append({
                "type": "text",
                "text": {"content": part}
            })

    return rich_text if rich_text else [{"type": "text", "text": {"content": text}}]


@app.command()
def main(
    page_id: Annotated[str, typer.Option(help="Page ID")],
    text: Annotated[str, typer.Option(help="Text content to append as paragraph")] = None,
    markdown: Annotated[str, typer.Option(help="Markdown content to parse and append")] = None,
    markdown_file: Annotated[str, typer.Option(help="Path to markdown file to parse and append")] = None,
    replace: Annotated[bool, typer.Option(help="Replace existing content instead of appending")] = False,
    output: Annotated[str, typer.Option(help="Output file path (JSON)")] = None,
):
    try:
        client = NotionClient()
        page_id = page_id.replace('-', '')

        if replace:
            print("Replacing existing content...")
            blocks_data = client.get_page_blocks(page_id)
            existing_blocks = blocks_data.get('results', [])

            if existing_blocks:
                print(f"   Deleting {len(existing_blocks)} existing blocks...")
                import requests
                for block in existing_blocks:
                    block_id = block['id'].replace('-', '')
                    url = f"https://api.notion.com/v1/blocks/{block_id}"
                    response = requests.delete(url, headers=client.headers)

        blocks = []

        if markdown_file:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            blocks = parse_markdown_to_blocks(markdown_content)
        elif markdown:
            blocks = parse_markdown_to_blocks(markdown)
        elif text:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                }
            })

        if not blocks:
            print("No content to append. Use --text, --markdown, or --markdown-file.")
            raise typer.Exit(1)

        print(f"Appending {len(blocks)} block(s) to page: {page_id}...")

        result = client.append_blocks(page_id, blocks)

        print(f"\n✓ Block(s) appended successfully")

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\nResult saved to: {output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise typer.Exit(1)


if __name__ == '__main__':
    app()
