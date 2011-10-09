#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import fileinput

mapping = {
    # pygments -> coderay
    # TODO: declaration == definition?
    #       namespace nn ?
    #       operator non-bold o ?
    #       whitespace w ?
    
    'c': 'c', # comment
    'cl': 'c',
    'cm': 'c',
    'err': 'er', # error
    # TODO: generic
    'il': 'i',
    'k' : 'kw', # keyword
    'kd': 'kw',
    'kn': 'kw',
    'kr': 'r', # reserved
    'kt': 'ty', # type
    'kc': 'co', # constant
    'kp': 'ps', # pseudo-class
    'bp': 'pc', # pre-constant
    'm': 'i', # number -> integer
    'mf': 'fl', # float
    'mh': 'hx', # hex
    'mi': 'i', # integer
    'mo': 'oc', # octal
    'na': 'an', # Name.Attribute -> Attribute_Name
    'nb': 'pd', # builtin
    'nc': 'cl', # class
    'nd': 'de', # decorator
    'ne': 'ex', # exception
    'nf': 'fu', # function
    'ni': 'en', # entity
    'nl': 'la', # label
#    'nn': ''
    'no': 'co', # constant
    'nt': 'ta',
    'nv': 'v', # variable
#    'o' : 'of', # operator
    'ow': 'of', # operator(-word)
    's' : 's', # string
    's1': 's',
    's2': 's',
    'sh': 's',
    'si': 's',
    'sx': 's',
    'sb': 'sh', # string-backtick (TODO: shell?)
    'sc': 'ch', # char
    'sd': 'k',
    'se': 'ch', # character-escape
    'sr': 'rx', # regex
    'ss': 'sy', # symbol
    'vc': 'cl', # variable-class
    'vi': 'iv', # variable instance
#    'w' : ''
}
          

def convert(input, options):
    '''converts pygments css file to match coderay tokens'''
    
    newcss = []
    
    for line in input:
        line = line.strip()
        if not line:
            newcss.append('')
            continue
        
        for token in mapping:
            if line.find('.'+token+' ') > -1:
                line = line.replace('.'+token+' ', '.'+mapping[token]+' ')
                
                if token == 'sd':
                    newcss.append(options.cssclass + ' ' \
                                  + line.replace('.'+token+' ', '.dl '))
                break
        
        newcss.append(options.cssclass + ' ' + line)
    return newcss


if __name__ == '__main__':
    
    from optparse import OptionParser, make_option
    
    options = [
        make_option('--class', dest='cssclass', help='prepending css class',
                    default=''),
    ]
    
    parser = OptionParser(option_list=options, usage='%prog [options] INPUT')
    (options, args) = parser.parse_args()
    
    result = convert(fileinput.input(args), options)
    for line in result:
        print line
            