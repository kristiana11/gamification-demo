from database import MongoDB

def generate_svg(user_data, template_path, output_path):
    with open(template_path, 'r') as f:
        svg_template = f.read()

    # Replace placeholders with actual data
    svg_template = svg_template.replace('{{ user_level }}', str(user_data['user_level']))
    svg_template = svg_template.replace('{{ total_quests }}', str(user_data['total_quests']))
    svg_template = svg_template.replace('{{ power_ups }}', str(user_data['power_ups']))
    svg_template = svg_template.replace('{{ community_rating }}', str(user_data['community_rating']))

    # Save the updated SVG to a new file
    with open(output_path, 'w') as f:
        f.write(svg_template)

if __name__ == "__main__":
    # Connect to the database
    db = MongoDB()

    # Test username
    username = "kristiana11"

    # Fetch user data from the database
    user_data = db.get_user_stats(username)

    # Provide the path to the template SVG file and the output SVG file
    template_path = '..\userCards\template.svg'
    output_path = '..\userCards\output.svg'

    # Generate the SVG file with dynamic data
    generate_svg(user_data, template_path, output_path)

    # Close the database connection
    db.close_connection()
