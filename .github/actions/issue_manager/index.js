const github = require('@actions/github');

try{
    const action = process.env.INPUT_ACTION;
    const user = process.env.INPUT_USER;
    const description = process.env.INPUT_DESCRIPTION;

    // look at how to use octokit to make API calls that will create an issue
    const octokit = github.getOctokit(process.env.GITHUB_TOKEN);


    switch (action) {
        case 'create':
            // create issue

        break;
        case 'delete':
            // delete issue
        break;
      default:
        console.log('Invalid action specified');
    }
}
catch (error) {
    console.log(error.message);
}
    }