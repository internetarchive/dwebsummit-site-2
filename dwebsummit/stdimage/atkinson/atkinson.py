"""
Test dither() with a small 6x6 square
>>> input = '\x55\x66\x77\x88\x99\xaa' * 6
>>> output = dither(PIL.Image.fromstring('L', (6, 6), input))
>>> output.tostring()
'\\x00\\x00\\xff\\xff\\x00\\xff\\x00\\x00\\xff\\x00\\xff\\xff\\x00\\xff\\x00\\x00\\xff\\xff\\x00\\xff\\x00\\xff\\xff\\x00\\x00\\x00\\xff\\xff\\x00\\xff\\x00\\x00\\xff\\x00\\x00\\xff'
>>> input
'Ufw\\x88\\x99\\xaaUfw\\x88\\x99\\xaaUfw\\x88\\x99\\xaaUfw\\x88\\x99\\xaaUfw\\x88\\x99\\xaaUfw\\x88\\x99\\xaa'
"""

import atk
import PIL.Image

def dither(i, *args, **kwargs):
    """ Take an instance of single-channel PIL.Image, dither and return
    """
    if i.mode != 'L':
        i = i.convert('L')

    assert i.mode == 'L'
    thresh = 100
    s = atk.atk(i.size[0], i.size[1], i.tobytes(), 75)
    o = PIL.Image.frombytes('L', i.size, s)
    return o

if __name__ == '__main__':
    import doctest
    doctest.testmod()
