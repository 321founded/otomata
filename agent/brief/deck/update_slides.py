#!/usr/bin/env python3
"""
Update Google Slides presentation with Otomata deck content.
"""
import sys
from pathlib import Path

# Add tools to path
MEMENTO_ROOT = Path('/data/assistants/654-memento')
tools_path = MEMENTO_ROOT / 'app' / 'tools' / 'google' / 'slides'
sys.path.insert(0, str(tools_path))

from lib.slides_client import SlidesClient

PRESENTATION_ID = '1BU9LrNLjdHPOJZGGn8L61Ox3GPVxZ-gWxr6OUfK5t4g'
CREDENTIALS_PATH = str(tools_path / '.keys' / 'gdrive-key.json')

# Warm pastel color palette (Notion/Forge style)
COLORS = {
    'warm_yellow': '#FEF9E7',      # Soft warm yellow
    'warm_orange': '#FDF2E9',      # Soft peach/orange
    'warm_sky': '#EBF5FB',         # Soft sky blue
    'warm_cream': '#FDFEFE',       # Cream white
    'accent_orange': '#E67E22',    # Orange accent
    'accent_blue': '#3498DB',      # Blue accent
    'text_dark': '#2C3E50',        # Dark text
}

# Slide background color mapping
SLIDE_BACKGROUNDS = {
    'p1': 'warm_yellow',   # Title slide - warm
    'p2': 'warm_cream',    # Market - neutral
    'p3': 'warm_orange',   # Challenges - warm
    'p4': 'warm_sky',      # Data Enrichment - cool
    'p5': 'warm_orange',   # Cost problem - warm
    'p6': 'warm_cream',    # PhacetLabs - neutral
    'p7': 'warm_yellow',   # Opportunity - warm/highlight
    'p8': 'warm_sky',      # Approach - cool
    'p9': 'warm_cream',    # Business model - neutral
    'p10': 'warm_yellow',  # Next steps - warm
    'p11': 'warm_cream',   # Questions - neutral
    'p12': 'warm_cream',   # Sources - neutral
}


def hex_to_rgb(hex_color):
    """Convert hex color to RGB dict (0.0-1.0 range)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return {'red': r, 'green': g, 'blue': b}


def get_slides_info(client):
    """Get info about all slides and their text objects."""
    slide_ids = client.get_slide_ids(PRESENTATION_ID)
    print(f"\nFound {len(slide_ids)} slides:\n")

    slides_info = []
    for i, slide_id in enumerate(slide_ids, 1):
        text_objects = client.get_text_objects_in_slide(PRESENTATION_ID, slide_id)
        print(f"=== Slide {i} (ID: {slide_id}) ===")

        slide_data = {
            'index': i,
            'id': slide_id,
            'text_objects': []
        }

        for obj in text_objects:
            text = obj['text'].strip()
            if text:
                print(f"  [{obj['objectId']}] {text[:60]}...")
                slide_data['text_objects'].append({
                    'id': obj['objectId'],
                    'text': text,
                    'type': obj.get('shapeType')
                })
        print()
        slides_info.append(slide_data)

    return slides_info


def set_slide_backgrounds(client):
    """Set background colors for all slides."""
    print("Setting slide backgrounds to warm pastel palette...")

    requests = []
    for slide_id, color_name in SLIDE_BACKGROUNDS.items():
        hex_color = COLORS.get(color_name, COLORS['warm_cream'])
        rgb = hex_to_rgb(hex_color)

        requests.append({
            'updatePageProperties': {
                'objectId': slide_id,
                'pageProperties': {
                    'pageBackgroundFill': {
                        'solidFill': {
                            'color': {
                                'rgbColor': rgb
                            }
                        }
                    }
                },
                'fields': 'pageBackgroundFill.solidFill.color'
            }
        })
        print(f"  {slide_id} → {color_name} ({hex_color})")

    # Execute batch update
    result = client.slides_service.presentations().batchUpdate(
        presentationId=PRESENTATION_ID,
        body={'requests': requests}
    ).execute()

    print(f"\nUpdated {len(requests)} slide backgrounds")
    return result


def set_title_colors(client):
    """Set title text colors to accent colors."""
    print("\nUpdating title text colors...")

    # Title objects to update with accent color
    title_updates = [
        ('p2_i18', 'accent_orange'),  # Le marché des AI Sales Agents
        ('p3_i15', 'accent_orange'),  # Pourquoi ça ne marche pas
        ('p4_i3', 'accent_blue'),     # Data Enrichment
        ('p5_i19', 'accent_orange'),  # Le problème du coût
        ('p6_i13', 'accent_blue'),    # Inspiration PhacetLabs
        ('p7_i19', 'accent_orange'),  # L'opportunité Otomata
        ('p8_i15', 'accent_blue'),    # Notre approche
        ('p9_i15', 'accent_orange'),  # Le modèle économique
        ('p10_i12', 'accent_blue'),   # Prochaines étapes
    ]

    requests = []
    for object_id, color_name in title_updates:
        hex_color = COLORS.get(color_name, COLORS['accent_orange'])
        rgb = hex_to_rgb(hex_color)

        requests.append({
            'updateTextStyle': {
                'objectId': object_id,
                'style': {
                    'foregroundColor': {
                        'opaqueColor': {
                            'rgbColor': rgb
                        }
                    }
                },
                'textRange': {'type': 'ALL'},
                'fields': 'foregroundColor'
            }
        })
        print(f"  {object_id} → {color_name}")

    if requests:
        result = client.slides_service.presentations().batchUpdate(
            presentationId=PRESENTATION_ID,
            body={'requests': requests}
        ).execute()
        print(f"\nUpdated {len(requests)} title colors")
        return result

    return None


def main():
    client = SlidesClient(CREDENTIALS_PATH)

    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == 'info':
            get_slides_info(client)

        elif action == 'backgrounds':
            set_slide_backgrounds(client)

        elif action == 'titles':
            set_title_colors(client)

        elif action == 'style':
            # Apply full style update
            set_slide_backgrounds(client)
            set_title_colors(client)
            print("\n✓ Style update complete!")
            print(f"  View: https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit")

        elif action == 'replace':
            if len(sys.argv) > 3:
                find_text = sys.argv[2]
                replace_text = sys.argv[3]
                print(f"Replacing '{find_text}' with '{replace_text}'...")
                result = client.replace_all_text(PRESENTATION_ID, find_text, replace_text)
                changes = result.get('replies', [{}])[0].get('replaceAllText', {}).get('occurrencesChanged', 0)
                print(f"Changed {changes} occurrences")

    else:
        print("Usage:")
        print("  python update_slides.py info        # Show slides info")
        print("  python update_slides.py backgrounds # Set background colors")
        print("  python update_slides.py titles      # Set title colors")
        print("  python update_slides.py style       # Apply full style update")


if __name__ == '__main__':
    main()
