const fs = require('fs');
const readmePath = `${process.env.GITHUB_WORKSPACE}/README.md`;
let readmeContent = fs.readFileSync(readmePath, 'utf8');

// get argument inputs, pass into script
const action = process.env.INPUT_ACTION;
const user = process.env.INPUT_USER;
const content = process.env.INPUT_CONTENT || '';
const replacePattern = process.env.INPUT_REPLACE_PATTERN || '';

console.log(content)

// action based off requested action
switch (action) {
  case 'create':
    readmeContent = user
    readmeContent += '\n'
    readmeContent += content; // overwrite/create
    break;
  case 'append':
    readmeContent += '\n' + content; // add to end
    break;
  case 'update':
    // look for specific to replace 
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp
    readmeContent = readmeContent.replace(new RegExp(replacePattern, 'g'), content);
    break;
  case 'delete':
    // delete specific
    readmeContent = readmeContent.replace(new RegExp(content, 'g'), '');
    break;
  default:
    console.log('Invalid action!');
}

// write to file
// fs.writeFileSync(readmePath, readmeContent);

generateMarkdown({ username: user, show_icons: true })
  .then(statsMarkdown => {
    // Integrate GitHub Readme Stats into README content
    const githubStatsContent = `[![${user}'s GitHub stats](https://github-readme-stats.vercel.app/api?username=${user})](https://github.com/${user}/github-readme-stats)`;

    // Replace placeholder in README content with GitHub Readme Stats content
    readmeContent = readmeContent.replace('<!--PLACEHOLDER_STATS_CARD-->', githubStatsContent);

    // Write updated content back to README file
    fs.writeFileSync(readmePath, readmeContent);

    console.log('GitHub Readme Stats added to README successfully.');
  })
  .catch(error => {
    console.error('Error generating GitHub Readme Stats:', error);
  });

console.log('README managed successfully.');