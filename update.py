def test(a=''):
    print('test func:', a)


def prep_func():
    test('from prep_func')


def cleanup_func():
    test('from cleanup_func')


INSTRUCTIONS = {'VERSION': 'dev_2',
                'prep': 'prep func',
                'dl': (('$R$want.txt', 'want.txt'), ('$R$example_main.py', 'example_main.py')),
                'cleanup': 'cleanup func'
                }
