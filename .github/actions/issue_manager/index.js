// main code for managing Issues. Main functions are create and delete
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
            const response = await octokit.rest.issues.create({
                owner: github.context.repo.owner,
                repo: github.context.repo.repo,
                title: description,
                body: description
            });
            console.log('Issue created successfully:', response.data.html_url);
        break;

        case 'delete':
            // delete issue
        const issues = await octokit.rest.issues.listForRepo({
            owner: github.context.repo.owner,
            repo: github.context.repo.repo,
            state: 'open',
            creator: user
        });
        if (issues.data.length > 0) {
            await octokit.rest.issues.update({
                owner: github.context.repo.owner,
                repo: github.context.repo.repo,
                issue_number: issues.data[0].number,
                state: 'closed'
            });
            console.log('Issue deleted');
        } 
        else {
            console.log('No open issue found for the specified user');
        }
        break;

      default:
        console.log('Invalid action specified');
    }
}
catch (error) {
    console.log(error.message);
}
