# keep-githubrepos-updated
A script to clone or update all repos from your github account or organization 

Note, it's supposed that you have git tools and your github ssh key account configured. See more info
https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/ 


```
usage: update-from-github.py [-h] [--organization ORGANIZATION] [--personal]
                             [--user USERNAME] [--pass PASSWORD]
                             [--visibility {all,private,public}]

Clone all repositories from a github organization or account.

optional arguments:
  -h, --help            show this help message and exit
  --organization ORGANIZATION
                        Clone or update the organization repos. Organization
                        is the name e.j: 'github' at https://github.com/github
  --personal            Retrieve your personal repos. Require username and
                        password. Default
  --user USERNAME       Your github username or USERNAME environment variable
  --pass PASSWORD       Your github password or PASSWORD environment variable
  --visibility {all,private,public}
                        Visiblity repos: all, private, public
```
