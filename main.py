import requests
import itertools

headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
base_url = "https://api.github.com/users"


def get_git_info(userid, number_of_events=100):
    url = f"{base_url}/{userid}/events/public?per_page={number_of_events}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        git_info = response.json()
        return git_info
    else:
        print(f"Returned Error Code: {response.status_code}")
        exit()


def get_top_event_types(github_events, number_of_events=3) -> {}:
    event_list = {}

    for event in github_events:
        if event['type'] in event_list:
            event_list[event['type']] = event_list[event['type']] + 1
        else:
            event_list[event['type']] = 1

    event_list = dict(itertools.islice(
        sorted(event_list.items(), key=lambda item: item[1], reverse=True), number_of_events))
    return event_list


def get_user_owned_repos(github_events, username) -> ():
    owned_urls = []
    for event in github_events:
        if username in event['repo']['url'] and event['repo']['url'] not in owned_urls:
            owned_urls.append(event['repo']['url'])

    return owned_urls


def main() -> None:
    username = input("Enter the GitHub username: ")
    github_events = get_git_info(username)

    print(f"Top event types for {username}: {get_top_event_types(github_events)}")
    print(f"Owned repos owned by {username}: {get_user_owned_repos(github_events, username)}")


if __name__ == "__main__":
    main()
