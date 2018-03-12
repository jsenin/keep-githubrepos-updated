#!/usr/bin/python

# This script clones all private repos from your github user or your organization

import os
import json
import base64
import urllib2 as requester
import argparse


def github_url_query_repos_from_organization(organization, visibility=None, page=1, per_page=100):
    ORG_REPOS_URL = 'https://api.github.com/orgs/{}/repos?type={}&page={}&per_page={}'
    return ORG_REPOS_URL.format(organization, visibility, page, per_page)

def github_url_query_repos_from_user(visibility=None, page=1, per_page=100):
    USER_REPOS_URL = 'https://api.github.com/user/repos?type={}&page={}&per_page={}'
    return USER_REPOS_URL.format(visibility, page, per_page)

def get_request_from(url, username=None, password=None):
    request = requester.Request(url=url)
    if username and password:
        print "> Authenticated Request as {}".format(username)
        request.add_header("Authorization", "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password)))
    request.add_header("Content-Type", "application/json")
    request.add_header("Accept", "application/json")
    f = requester.urlopen(request)
    content = f.read()
    headers= f.info()
    return content, headers

def find_next_request(headers):
    link = headers.get('Link')
    if not link:
        return None
    links = link.split(',')
    for link in links:
        link = link.strip()
        url, rel = link.split(';')
        if rel.strip().startswith('rel="next"'):
           next_request = url.replace('<','').replace('>', '')
           return next_request

def get_all_pages(next_request, username, password):
    content = []
    while next_request:
        response, headers = get_request_from(url=next_request, username=username, password=password)
        content = content + json.loads(response)
        next_request = find_next_request(headers)
    return content

def github_repos_from_organization(organization, username=None, password=None, visibility=None):
    page = 1
    next_request = github_url_query_repos_from_organization(organization=organization, page=page, visibility=visibility)
    return get_all_pages(next_request, username, password)

def github_repos_from_user(username=None, password=None, visibility=None):
    page = 1
    next_request = github_url_query_repos_from_user(page=page, visibility=visibility)
    return get_all_pages(next_request, username, password)

def clone(remote_repo):
    print ">>> Cloning {}".format(remote_repo)
    os.system("git clone {}".format(remote_repo))

def update(dirname):
    print ">>> Updating {}".format(dirname)
    os.system("cd {}; git remote update -p; git merge --ff-only;".format(dirname))

def clone_or_update(repos):
    print "> Found {} repos: ".format(len(repos))
    for repo in repos:
        repo_url = repo['ssh_url']
        dirname = repo['name']
        if os.path.isdir(dirname):
            update(dirname)
        else:
            clone(repo_url)

def command_line_arguments():
    parser = argparse.ArgumentParser(description='Clone all repositories from a github organization or account.')
    parser.add_argument('--organization', dest='organization', type=str, help='Clone or update the organization repos. Organization is the name e.j: \'github\' at https://github.com/github')
    parser.add_argument('--personal', dest='personal', action='store_true', help='Retrieve your personal repos. Require username and password. Default')
    parser.add_argument('--user', dest='username', default=os.environ.get('USERNAME', None), type=str, help='Your github username or USERNAME environment variable')
    parser.add_argument('--pass', dest='password', default=os.environ.get('PASSWORD', None), type=str, help='Your github password or PASSWORD environment variable')
    parser.add_argument('--visibility', dest='visibility', choices=['all', 'private', 'public'], type=str, help='Visiblity repos: all, private, public')
    return parser

parser = command_line_arguments()
args = parser.parse_args()
if args.organization:
    repos = github_repos_from_organization(args.organization, args.username, args.password, args.visibility)
    clone_or_update(repos)
elif args.username and args.password:
    repos = github_repos_from_user(args.username, args.password, args.visibility)
    clone_or_update(repos)
else:
    parser.print_help()
