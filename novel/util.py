
def prettytime(tick):
    if tick >= 24:
        return "@%dd%02dh" % (tick // 24, tick % 24)
    return "@%02dh" % (tick % 24)

def reltime(then, now):
    hours = now - then
    if hours == 0:
        return 'just now'
    if hours == 1:
        return 'an hour ago'
    if hours < 24:
        return "%s hours ago" % (int_to_word(hours),)
    return "%s days, %s hours ago" % (int_to_word(hours // 24), int_to_word(hours % 24))

def int_to_word(num):
    """Integer to English word converter,
    from https://stackoverflow.com/a/32640407"""
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'fourth', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + '-' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred and ' + int_to_word(num % 100)

    if (num < m):
        if num % k == 0: return int_to_word(num // k) + ' thousand'
        else: return int_to_word(num // k) + ' thousand, ' + int_to_word(num % k)

    if (num < b):
        if (num % m) == 0: return int_to_word(num // m) + ' million'
        else: return int_to_word(num // m) + ' million, ' + int_to_word(num % m)

    if (num < t):
        if (num % b) == 0: return int_to_word(num // b) + ' billion'
        else: return int_to_word(num // b) + ' billion, ' + int_to_word(num % b)

    if (num % t == 0): return int_to_word(num // t) + ' trillion'
    else: return int_to_word(num // t) + ' trillion, ' + int_to_word(num % t)

    raise AssertionError('num is too large: %s' % str(num))
