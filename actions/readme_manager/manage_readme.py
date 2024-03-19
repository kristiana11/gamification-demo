import os

readme_path = os.path.join(os.environ['GITHUB_WORKSPACE'], 'README.md')

# get argument inputs, pass into script
action = os.environ['INPUT_ACTION']
content = os.environ['INPUT_CONTENT'] if 'INPUT_CONTENT' in os.environ else ''
replace_pattern = os.environ['INPUT_REPLACE_PATTERN'] if 'INPUT_REPLACE_PATTERN' in os.environ else ''

with open(readme_path, 'r') as file:
    readme_content = file.read()

# action based off requested action
if action == 'create':
    readme_content = content  # overwrite/create
elif action == 'append':
    readme_content += '\n' + content  # add to end
elif action == 'update':
    # look for specific to replace
    readme_content = readme_content.replace(replace_pattern, content)
elif action == 'delete':
    # delete specific
    readme_content = readme_content.replace(content, '')

with open(readme_path, 'w') as file:
    file.write(readme_content)

print('README managed successfully.')