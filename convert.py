#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys, re
import fileinput

"""
`pygmentize -S friendly -f html` to get all pygments tokens

lib/coderay/token_classes.rb

    :annotation => 'at',
    :attribute_name => 'an',
    :attribute_name_fat => 'af',
    :attribute_value => 'av',
    :attribute_value_fat => 'aw',
    :bin => 'bi',
    :char => 'ch',
    :class => 'cl',
    :class_variable => 'cv',
    :color => 'cr',
    :comment => 'c',
    :complex => 'cm',
    :constant => 'co',
    :content => 'k',
    :decorator => 'de',
    :definition => 'df',
    :delimiter => 'dl',
    :directive => 'di',
    :doc => 'do',
    :doctype => 'dt',
    :doc_string => 'ds',
    :entity => 'en',
    :error => 'er',
    :escape => 'e',
    :exception => 'ex',
    :float => 'fl',
    :function => 'fu',
    :global_variable => 'gv',
    :hex => 'hx',
    :imaginary => 'cm',
    :important => 'im',
    :include => 'ic',
    :inline => 'il',
    :inline_delimiter => 'idl',
    :instance_variable => 'iv',
    :integer => 'i',
    :interpreted => 'in',
    :keyword => 'kw',
    :key => 'ke',
    :label => 'la',
    :local_variable => 'lv',
    :modifier => 'mod',
    :oct => 'oc',
    :operator_fat => 'of',
    :pre_constant => 'pc',
    :pre_type => 'pt',
    :predefined => 'pd',
    :preprocessor => 'pp',
    :pseudo_class => 'ps',
    :regexp => 'rx',
    :reserved => 'r',
    :shell => 'sh',
    :string => 's',
    :symbol => 'sy',
    :tag => 'ta',
    :tag_fat => 'tf',
    :tag_special => 'ts',
    :type => 'ty',
    :variable => 'v',
    :value => 'vl',
    :xml_text => 'xt',
    
    :insert => 'ins',
    :delete => 'del',
    :change => 'chg',
    :head => 'head',

    :ident => :NO_HIGHLIGHT, # 'id'
    #:operator => 'op',
    :operator => :NO_HIGHLIGHT,  # 'op'
    :space => :NO_HIGHLIGHT,  # 'sp'
    :plain => :NO_HIGHLIGHT,
"""

class UserDict(dict):
    '''access to mapping'''
    
    def __iter__(self):
        '''Yields every key, even it is a tuple. Then it returns its elements.'''
        
        for key in self.keys():
            if isinstance(key, tuple):
                for v in key:
                    yield v
            else:
                yield key
                
    def __contains__(self, key):
        '''returns True if key is in self (or a subelement), else False.'''
        
        for val in iter(self):
            if val == key:
                return True
        return False
        
    def __getitem__(self, item):
        '''first look up the default dict-way. If not found, assuming it
        might be a tuple'''
        
        try:
            return super(UserDict, self).__getitem__(item)
        except KeyError:
            for key in self.keys():
                if isinstance(key, tuple):
                    if item in key:
                        return super(UserDict, self).__getitem__(key)
        raise KeyError(item)


class Rule:
    '''a basic CSS-Rule constructor.  __hash__-able, to sort out duplicates.'''
    
    def __init__(self, identifier, code):
        self.identifier = identifier
        self.code = code
        
    def __str__(self):
        return '.' + self.identifier + ' {' + self.code + '}'
        
    def __hash__(self):
        return hash(self.identifier)
        
    def __eq__(self, other):
        return True if hash(other) == hash(self) else False


mapping = UserDict({
    # pygments -> coderay (neither injective nor surjective)
    
    # : 'at', # :annotation
    'na' : 'an', # :attribute_name
    'gs' : ('af', 'aw'), # :attribute_name_fat
    # : 'av', # :attribute_value
    # : 'aw', # :attribute_value_fat
    # : 'bi', # :bin
    'sc' : 'ch', # :char
    ('nc', 'vc') : 'cl', # :class
    # : 'cv', # :class_variable
    # : 'cr', # :color
    ('c', 'cl', 'cm') :  'c', # :comment
    # : 'cm', # :complex
    ('kc', 'no') : 'co', # :constant
    # :  'k', # :content
    'nd' : 'de', # :decorator
    # : 'df', # :definition
    # : 'dl', # :delimiter
    # : 'di', # :directive
    # : 'do', # :doc
    # : 'dt', # :doctype
    'sd' : ('ds', 'k', 'dl'), # :doc_string
    'ni' : 'en', # :entity
    'err': 'er', # :error
    'se' :  'e', # :escape
    'ne' : 'ex', # :exception
    'mf' : 'fl', # :float
    'nf' : 'fu', # :function
    'vg' : 'gv', # :global variable
    'mh' : 'hx', # :hex
    # : 'cm', # :imaginary
    # : 'im', # :important
    # : 'ic', # :include
    # : 'il', # :inline
    # : 'idl', # :inline_delimiter
    'vi' : 'iv', # :instance_variable
    ('m', 'il', 'mi') :  'i', # :integer
    # : 'in', # :interpreted
    ('k', 'kd', 'kn') : 'kw', # :keyword
     # : 'ke', # :key
     'nl' : 'la', # :label
    # : 'lv', # :local_variable
    # : 'mod', # :modifier
    'mo' : 'oc', # :oct
    'o' : 'op', # :operator
    'ow' : 'of', # :operator_fat
    'bp' : 'pc', # :pre_constant
    # : 'pt', # :pre_type
    'nb' : 'pd', # :predefined
    # : 'pp', # :preprocessor
    'kp' : 'ps', # :pseudo_class
    'kr' :  'r', # :reserved
    'sr' : 'rx', # :regexp
    'sb' : 'sh', # :shell
    ('s', 's1', 's2', 'sh', 'si', 'sx') :  ('s', 'xt'), # :string :xml_text
    'ss' : 'sy', # :symbol
    'nt' : 'ta', # :tag
    # : 'ts', # :tag_special
    'kt' : 'ty', # :type
    'nv' :  'v', # :variable
    # : 'vl', # :value
    
    'gi' : 'ins', # :insert
    'gd' : 'del', # :delete
    # : 'chg', # :change
    # : 'head', # :head
})

def parse(css):
    '''simple css parsing and comment stripping, assuming something like this:
    .oneidentifier { block };'''
    
    result = []
    css = re.sub('/\*[^*/]*\*/', '', css) # we strip pygment's css information
    
    for block in re.findall('\.([^{]+){([^}]*)}', css, re.MULTILINE):
        identifier, code = block[0].strip(), block[1]
        result.append((identifier, code))
        
    return result
    

def convert(input):
    '''converts pygments css file to match coderay tokens'''
    
    input = parse(''.join(line for line in input))
    newcss = set([])
    
    for (tag, code) in sorted(input): # TODO: does not select automatically the first item in tuples
        if not tag in mapping:
            # print >> sys.stderr, "'%s' not mapped" % tag
            continue
        
        v, w = tag, mapping[tag] # pygments identifier -> coderay identifier
        if isinstance(w, str) and isinstance(v, str):
            # bijektiv
            newcss.add(Rule(w, code))
        else:
            if isinstance(w, str):
                w = (w, )
            
            for token in w:
                # newcss is a set, pygments identifier returning the same token (surjective)
                # are skipped (returning the same hash for the same css class)
                newcss.add(Rule(token, code))
    
    return newcss


if __name__ == '__main__':
    
    from optparse import OptionParser, make_option
    
    options = [
        make_option('--class', dest='cssclass', help='prepending css class',
                    default=''),
    ]
    
    parser = OptionParser(option_list=options, usage='%prog [options] INPUT')
    (options, args) = parser.parse_args()
    
    result = convert(fileinput.input(args))
    for line in result:
        if options.cssclass:
            print options.cssclass,
        print line
            