import os
import sys
import time
import json
import requests
try:
    from settings import config
except Exception as E:
    print("\nCannot open config.py, did you create it from config.py.sample?\n")
    print("\t Exception:\n\t {}\n".format(E))
    sys.exit(0)
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

headers = {
    "Authorization": "token {}".format(config['token'])
}
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('index.html')


def get_user(user):
    """
        Get main user data.
    """
    r = requests.get(config['apiurl'] + '/users/{}'.format(user), headers=headers) # noqa : 501
    if r.status_code == 200:
        res = r.json()
        data = {
            'user': {
                'user_data': {
                    'login': res['login'],
                    'name': res['name'],
                    'desc': res['bio'],
                    'location': res['location'],
                    'url': res['html_url'],
                    'avatar': res['avatar_url'],
                    'blog_url': res['blog'],
                    'joined': res['created_at']
                },
                'numbers': {
                    'repos': res['public_repos'],
                    'gists': res['public_gists'],
                    'followers': res['followers'],
                    'following': res['following'],
                },
                'user_urls': {
                    'followers': res['followers_url'],
                    'following': res['following_url'],
                    'gists': res['gists_url'],
                    'starred': res['starred_url'],
                    'subs': res['subscriptions_url'],
                    'org': res['organizations_url'],
                    'repos': res['repos_url']
                }
            }
        }
        json_object = json.dumps(data, sort_keys=False)
        return(json_object)
    else:
        print(
            "Something went wrong..",
            r.status_code,
            r.content
        )
        sys.exit(0)


def get_repos(user):
    """
        Get user repo data.
    """
    r = requests.get(config['apiurl'] + '/users/{}/repos?per_page=1000&sort=created'.format(user), headers=headers) # noqa : 501
    if r.status_code == 200:
        result = r.json()
        c = 0
        data = {'repos': {}}
        for res in result:
            data['repos'][c] = {}
            data['repos'][c]['id'] = res['id']
            data['repos'][c]['name'] = res['full_name']
            data['repos'][c]['desc'] = res['description']
            data['repos'][c]['language'] = res['language']
            data['repos'][c]['forks'] = res['forks']
            data['repos'][c]['watchers'] = res['watchers']
            data['repos'][c]['stars'] = res['stargazers_count']
            data['repos'][c]['dates'] = {}
            data['repos'][c]['dates']['created_at'] = res['created_at'].split('T')[0] # noqa : 501
            data['repos'][c]['dates']['updated_at'] = res['updated_at'].split('T')[0] # noqa : 501
            data['repos'][c]['dates']['pushed_at'] = res['pushed_at'].split('T')[0] # noqa : 501
            c = c+1
        return(data)
    else:
        print(
            "Something went wrong..",
            r.status_code,
            r.content
        )
        sys.exit(0)


def get_events(user):
    """
        Get user event data.
    """
    r = requests.get(config['apiurl'] + '/users/{}/events'.format(user), headers=headers) # noqa : 501
    if r.status_code == 200:
        result = r.json()
        c = 0
        data = {'events': {}}
        for res in result:
            data['events'][c] = {}
            data['events'][c]['type'] = res['type']
            data['events'][c]['repo'] = res['repo']['name']
            data['events'][c]['repo_url'] = res['repo']['url']
            data['events'][c]['created_at'] = res['created_at'].split('T')[0] # noqa : 501
            c = c+1
        json_object = json.dumps(data, sort_keys=False)
        return(json_object)
    else:
        print(
            "Something went wrong..",
            r.status_code,
            r.content
        )
        sys.exit(0)


def create_html(data):
    """
        Create HTML data.
    """
    if data:
        fname_time = time.strftime("%Y_%m_%d")
        fname = data['user']['user_data']['login'] + '_' + fname_time + '.html'
        filename = os.path.join(root, '../{}'.format(fname))
        with open(filename, 'w') as fh:
            fh.write(template.render(
                data=data,
                json_data=json.dumps(data)
            ))
        return(fname)
    else:
        print("Seems to be no data to parse.")
        sys.exit(0)


def count_repostars(repos):
    """
        Count stars across users
        repositories and build json.
    """
    stars = []
    for repo in repos['repos'].items():
        stars.append(repo[1]['stars'])
    stars = (sum(stars))
    repos['repos_stars'] = stars
    reps = json.dumps(repos, sort_keys=False)
    return(reps)


def json_merge(user, repos, events):
    """
        Merge 'user', 'repos' and 'events'
        into one big beautiful json.
    """
    repos_json = count_repostars(repos)
    merge = {
        **json.loads(user),
        **json.loads(repos_json),
        **json.loads(events)
    }
    return(merge)
