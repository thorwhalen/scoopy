import os
from dol import JsonFiles


def current_time_str():
    from datetime import datetime

    now = datetime.now()
    return now.strftime("%Y-%m-%d--%H-%M-%S")


def search_and_save_news(query, store='~', country='us'):
    from scoopy import search_news

    if isinstance(store, str):
        import os
        from dol import JsonFiles

        rootdir = os.path.expanduser(store)
        # create the rootdir if it does not exist
        os.makedirs(rootdir, exist_ok=True)

        store = JsonFiles(rootdir)
    results = search_news(query)
    key = f'{current_time_str()}__{query}.json'
    store[key] = results
    return key


if __name__ == '__main__':
    import argh

    argh.dispatch_command(search_and_save_news)
