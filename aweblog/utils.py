from flask import request, redirect, url_for


# from aweblog.extensions import cache


def redirect_back(default="post.index", **args):
    # cache.clear()
    for url in request.args.get('next'), request.referrer:
        if url:
            return redirect(url)
    return redirect(url_for(default), **args)
