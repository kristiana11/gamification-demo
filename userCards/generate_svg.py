from svgwrite import Drawing

def generate_svg(data):
    # Read SVG template
    with open("template.svg", "r") as f:
        svg_template = f.read()

    # Replace placeholders with actual data
    svg_content = svg_template.format(
        level=data.get("level", ""),
        quests_completed=data.get("quests_completed", ""),
        power_ups_used=data.get("power_ups_used", ""),
        community_rating=data.get("community_rating", "")
    )

    # Generate SVG drawing
    svg = Drawing(size=("450px", "195px"))
    svg.add(svg_content)

    # Save SVG file
    with open("output.svg", "w") as f:
        f.write(svg.tostring())

    print("SVG file generated successfully.")

def main():
    # Fetch data from MongoDB or any other source
    data = {
        "level": 2,
        "quests_completed": 3,
        "power_ups_used": 2,
        "community_rating": 115
    }

    # Generate SVG file using the fetched data
    generate_svg(data)

if __name__ == "__main__":
    main()
