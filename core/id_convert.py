base = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def id_to_base62(num):
    if num == 0:
        return base[0]
    res = ""
    while num:
        num, remain = divmod(num, 62)
        res = base[remain] + res
    # output short string with base-62 decimal
    return res


def url_to_base10(short_url):
    url_len = len(short_url)
    res = 0
    for i in range(url_len):
        res = 62*res + base.find(short_url[i])
    return res
