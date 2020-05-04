import furl
import re

import validators as validators

import tools

## Video is composed of
## ID
## Video Page
## thumbnail
## StoryBoard scrolling pictures
## Preview Video or image


vid_pattern = re.compile("^[a-zA-Z0-9\_\-]{11}$")

yt_domains_list = (
    "www.youtube.com",
    "youtube.com",
    'youtu.be',
    'm.youtube.com',
    "youtube-nocookie.com",
    "youtubeeducation.com",
    "yt.be",
    "googlevideo.com",
    "ytimg.com",
    "youtubekids.com"
)

yt_ignore_urls_regex_list = (
    r"(?:(?:[a-z0-9A-Z\-\_]+\.)?youtube\.com|youtu\.be|yt\.be|youtube\-nocookie\.com|ytimg\.com)(\/api\/stats\/)",
)

yt_img_thumbnail_regex_list = (
    r"(?:[a-z0-9A-Z\-\_]+\.)?ytimg\.com\/(?:vi|an_webp|vi_webp|sb|an)\/([a-zA-Z0-9\_\-]{11})\/",
)

yt_domain_regex_list = (
    r"(?:(?:[a-z0-9A-Z\-\_]+\.)?youtube\.com|youtu\.be|yt\.be|youtube\-nocookie\.com|ytimg\.com)$",
)

yt_path_regex_list = (
    "\/watch",
    "\/embed\/watch",
    "\/e\/watch",
    "\/e\/v\/watch",
    "\/user\/[a-zA-Z0-9\-\_]+\/watch?",
)

# yt_video_id_regex = re.compile(
#     r'(?:\?|\&|\/)(v\=|\/v\/)([a-zA-Z0-9\_\-]{6,11})',
# )

yt_video_id_regex = (
    r"(?:\?|\&|\/)(?:v\=|\/v\/)([a-zA-Z0-9\_\-]{11})",
    r"^(?:\/)([a-zA-Z0-9\_\-]{11})(\?|\/)?",
    r"^\/(?:an_webp|vi|sb|vi_webp)\/([a-zA-Z0-9\_\-]{11})(\?|\/)?",
)


# yt_list_id_regex = re.compile(
#     r'(?:\?|\&|\/)list\=([a-zA-Z0-9\_\-]+)',
# )


def get_yt_vid(test_url):
    oo = furl.furl(test_url)

    test_res = {"url": test_url}

    isYtDomainStr = oo.host in yt_domains_list
    isYtDomainRegex = tools.regex_list_match(oo.host, yt_domain_regex_list) is not None

    if isYtDomainStr or isYtDomainRegex:
        test_res["host-match"] = True

        if len(oo.pathstr) != 0:
            test_res["path-str"] = True
        else:
            test_res["path-str"] = False

        if len(oo.querystr) != 0:
            test_res["query-str"] = True
        else:
            test_res["query-str"] = False

        id_res = tools.regex_list_match(oo.pathstr + "?" + oo.querystr, yt_video_id_regex)
        if id_res is not None:
            test_res["id-match"] = id_res.group(1)

        res = tools.regex_list_match(oo.pathstr, yt_path_regex_list)
        if res is not None:
            test_res["path-match"] = True
        else:
            test_res["path-match"] = False

    else:
        test_res["host-match"] = False

    if test_res.get("id-match") is not None:
        return test_res["id-match"]

    return None
