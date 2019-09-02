# TODO:
# 1, rewrite config_to_ini using collections.OrderedDict objects
# 2, optimize parameters in cprint

from __future__ import print_function
import sys, re, os, time
CJK_str = '[\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]'
CJK_RE = re.compile( r'[\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+' )
CJK_QUOTE_RE = re.compile( r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])(["\'])' )
QUOTE_CJK_RE = re.compile( r'(["\'])([\u3040-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])' )
FIX_QUOTE_RE = re.compile( r'(["\'\(\[\{<\u201c]+)(\s*)(.+?)(\s*)(["\'\)\]\}>\u201d]+)' )
FIX_SINGLE_QUOTE_RE = re.compile(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])( )(\')([A-Za-z])' )

CJK_HASH_RE = re.compile( r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])(#(\S+))' )
HASH_CJK_RE = re.compile( r'((\S+)#)([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])' )

CJK_OPERATOR_ANS_RE = re.compile( r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([\+\-\*\/=&\\|<>])([A-Za-z0-9])' )
ANS_OPERATOR_CJK_RE = re.compile( r'([A-Za-z0-9])([\+\-\*\/=&\\|<>])([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])' )

CJK_BRACKET_CJK_RE = re.compile( r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([\(\[\{<\u201c]+(.*?)[\)\]\}>\u201d]+)([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])' )
CJK_BRACKET_RE = re.compile( r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([\(\[\{<\u201c>])' )
BRACKET_CJK_RE = re.compile( r'([\)\]\}>\u201d<])([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])' )
FIX_BRACKET_RE = re.compile( r'([\(\[\{<\u201c]+)(\s*)(.+?)(\s*)([\)\]\}>\u201d]+)' )

FIX_SYMBOL_RE = re.compile( r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([~!;:,\.\?\u2026])([A-Za-z0-9])' )

CJK_ANS_RE = re.compile( r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([A-Za-z0-9`\$%\^&\*\-=\+\\\|/@\u00a1-\u00ff\u2022\u2027\u2150-\u218f])' )
ANS_CJK_RE = re.compile( r'([A-Za-z0-9`~\$%\^&\*\-=\+\\\|/!;:,\.\?\u00a1-\u00ff\u2022\u2026\u2027\u2150-\u218f])([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])' )


VERSION = "v20190902"
def __version__():


    return VERSION

def add_fix(filename, fix, suffix= True):
    '''
    This function will return a new file name by adding a prefix or suffix to the **filename**

    Paramaters:

    * **filename**: string. old file name
    * **fix**: string. The prefix or suffix you want to add.
    * **suffix**: boolean. Should we add a prefix or suffix ?

    Example:

    name = '~/human.fastq'

    fix = '_sorted'

    add_fix(name, fix, suffix= True) will return "~/human_sorted.fastq"
    '''
    import os.path as path

    if not isinstance( filename, str ):
        raise TypeError( 'add_fix expects a string for filename, instead a {} is given.'.format(type(filename)) )

    if not isinstance( fix, str ):
        raise TypeError( 'add_fix expects a string for fix, instead a {} is given.'.format(type(fix)) )

    if not isinstance( suffix, bool ):
        raise TypeError( 'add_fix expects a boolean for suffix, instead a {} is given.'.format(type(suffix)) )

    #=====================format check over========================

    #If filename is 'in_file.fastq' then new filename would be 'in_file_sorted.fastq'
    if suffix:

        newname = path.split( path.splitext(filename)[0] )[1] + fix + path.splitext(filename)[1]
        newname = path.join( path.dirname(filename), newname )

    else:
        newname = fix + path.split( path.splitext(filename)[0] )[1] + path.splitext(filename)[1]
        newname = path.join( path.dirname(filename), newname )

    return newname

def bi_index(a, x):
    '''
    Locate the leftmost item exactly equal to x in a

    Parameters:
        **a**: any
            an iterable object such as a list

        **x**: any
            same type as the item in a

    Returns:
        **location**: integer
            the index location of the leftmost item exactly equal to x in a, -1 means can't find.
    '''
    import bisect
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise -1

def divide_dict(dictionary, chunk_size):

    '''
    Divide one dictionary into several dictionaries

    Return a list, each item is a dictionary with items of chunk_size
    '''

    import numpy, collections

    count_ar = numpy.linspace(0, len(dictionary), chunk_size+1, dtype= int)
    group_lst = []
    temp_dict = collections.defaultdict(lambda : None)
    i = 1
    for key, value in dictionary.items():
        temp_dict[key] = value
        if i in count_ar:
            group_lst.append(temp_dict)
            temp_dict = collections.defaultdict(lambda : None)
        i += 1
    return group_lst

def checkFile(filename, check_readable=False, check_writable= False, check_creatable= False, raise_on_error=False):
    '''
    Check the file status
    when exception, raise FileNotFoundError or IsADirectoryError or PermissionError if raise_on_error
    if raise_on_error=False, then return False when exception

    Return True if successful
    Return False if fail and raise_on_error=False
    Raise FileNotFoundError or IsADirectoryError or PermissionError if fail and raise_on_error=True
    '''

    import os.path as path
    import os, sys

    if not isinstance(filename, str):
        print('checkFile needs a string as parameter "filename", but a {} is given.\n'.format( type(filename) ) )
        raise TypeError
    else:
        file_str = path.realpath( path.expanduser( filename ) )

    if not isinstance(check_readable, bool) or not isinstance(check_writable, bool) or not isinstance(check_creatable, bool):
        print('check must be a boolean.')
        raise TypeError
    #========================format check over========================

    if check_readable:  # check if readable
        if not path.exists(file_str):
            print("{} doesn't exist.\n".format(filename) )
            raise FileNotFoundError
        if not path.isfile(file_str):
            print("{} is not a file.\n".format( filename ) )
            raise IsADirectoryError
        if not os.access(file_str,os.R_OK):
            print("{} is not readable.\n".format( filename ) )
            raise PermissionError

    if check_writable:  # check if writable
        if not path.exists(file_str):
            print("{} doesn't exist.\n".format(filename) )
            raise FileNotFoundError
        if not path.isfile(file_str):
            print("{} is not a file.\n".format( filename ) )
            raise IsADirectoryError
        if not os.access(file_str,os.W_OK):
            print("{} is not readable.\n".format( filename ) )
            raise PermissionError

    if check_creatable:  # check if creatable
        dirName_str = path.dirname(file_str)
        if not path.exists(dirName_str) or not path.isdir(dirName_str): # the folder doesn't exist
            os.mkdir(dirName_str)
            os.removedirs(dirName_str)
        elif not os.access( dirName_str, os.W_OK and os.X_OK ) :  # the folder exists
            print("The folder {} doesn't have proper permission.\n".format(dirName_str) )
            raise PermissionError
        else:
            pass

    return file_str

def complement(nuc_str):
    '''
    Input a nucleotide base ("A","T","C","G","a","t","c","g")
    Return its complementary base
    '''
    upper_lst = ["A","T","C","G"]
    upperC_lst = ["T","A","G","C"]
    lower_lst = ["a","t","c","g"]
    lowerC_lst = ["t","a","g","c"]
    if not isinstance(nuc_str, str) or len(nuc_str) != 1:
        return ""
    elif nuc_str in upper_lst:
        return upperC_lst[ upper_lst.index(nuc_str) ]
    elif nuc_str in lower_lst:
        return lowerC_lst[ lower_lst.index(nuc_str) ]
    else:
        return ""

def config_to_ini(config, fileobject, sequence='sorted', hint=None ,space_around_delimiters=True, raise_on_exist=False):
    '''
    This function is meant to replace configparser.ConfigParser().write
    It can write an configparser.ConfigParser() object in sorted sequence or custom sequence.
    Dependency: checkFile

    Parameter:
        **config**: A configparser.ConfigParser() object
            The config object you want to write

        **fileobject**: string or a fileobject
            Where you want to write into

        **sequence**: either None, 'sorted' or a dictionary
            This represents the sequence you want to write.
            If None, sections and keys will be writen arbitrarily as if configparser.ConfigParser().write does.
            If a dictionary. The dictionary will be like:
            {'Sections':[section1_name, section2_name,.....], 'section1_name':[keyname1 in section1, keyname2 in section1......], 'section2_name':[keyname1 in section2, keyname2 in section2......], ......  }
            Sections and keys that are not in the sequence dictionary will be writen into the configuration file alphabetically.
            Section 'DEFAULT' will be always on the top of the configuration file (even if 'DEFAULT' section is not the first item in sequence['Sections'] )

        **Hint**: None or a dictionary containing comments.
            The hint dictionary is in the follwing format:
                { (section1, key1):'your_comments', (section2, key2):'your_comments'........  }

        **space_around_delimiters**: boolean
            If space_around_delimiters is true, delimiters between keys and values are surrounded by spaces.

        **raise_on_exist**: boolean
            If True and the file exists an exception will be raised. If a fileobject is given this parameter will be ignored.

    Returns:
        True if completely successful

    '''
    import configparser, io
    import os.path as path
    #====================format check=========================

    if not isinstance(config, configparser.ConfigParser ):
        print( 'config_to_ini need a configparser.ConfigParser object as parameter "config", instead a {} is given.\n'.format( type(config) ) )
        raise TypeError

    if not isinstance(fileobject, str) and not isinstance(fileobject, io.TextIOBase):
        print( 'config_to_ini need a filename string or io.TextIOBase object as parameter "fileobject", instead a {} is given.\n'.format( type(fileobject) ) )
        raise TypeError

    if sequence != None and sequence != "sorted" and not isinstance(sequence, dict):
        print( 'config_to_ini need None or "sorted" or a dictionary as parameter "sequence", instead a {} is given.\n'.format( type(sequence) ) )
        raise TypeError


    if isinstance(fileobject, str) and path.exists(fileobject):
        if raise_on_exist:
            print('{} has already existed.\n'.format(fileobject) )
            raise FileExistsError

    if isinstance(sequence, dict):
        SyntaxError_str = "The sequence dictionary is like:\n{'Sections':[section1_name, section2_name,.....], 'section1_name':[keyname1 in section1, keyname2 in section1......], 'section2_name':[keyname1 in section2, keyname2 in section2......], ......  }\nSections and keys that are not in the sequence dictionary will be writen into the configuration file alphabetically.\nSection 'DEFAULT' will be always on the top of the configuration file (even if 'DEFAULT' section is not the first item in sequence['Sections'] )"
        SyntaxWarning_str = "sequence['Sections'] contains the section names that doesn't exist in the configparser.ConfigParser object."

        try:
            for sectionName_str in sequence['Sections']:
                if sectionName_str not in list( sequence.keys() ):  #
                    raise SyntaxError
                if sectionName_str not in config.sections():
                    raise SyntaxWarning

        except SyntaxError:
            print(SyntaxError_str)
            print()
            raise SyntaxError

        except SyntaxWarning:
            print(SyntaxWarning_str)
            print()

    #=================format check over=======================
    def __c_to_i(config, fileobject, s):
        '''
        Write a configparser.ConfigParser() object in sorted order into a fileobject
        This is a private function and should not be used out of config_to_ini()
        The [DEFAULT] section will be ignored.
        '''
        import configparser
        hint_str = ''
        config_cp = configparser.ConfigParser()
        config_cp = config
        keys_lst = list( config_cp.defaults().keys() )
        for k in keys_lst:
            config_cp.remove_option('DEFAULT', k)

        isSpace_str=' ' if s else ''
        sectionName_lst = config.sections()
        sectionName_lst.sort()
        for s in sectionName_lst:
            fileobject.writelines('[{}]\n'.format( s ) )
            keys_lst = config.options(s)
            keys_lst.sort()
            for k in keys_lst:
                hint_str = '   # ' + hint[ (sectionName_str, key_str) ] if isinstance(hint, dict) and (sectionName_str, key_str) in hint.heys() else ''
                fileobject.writelines( '{0}{1}={1}{2}{3}\n'.format(k, isSpace_str, config.get(s, k), hint_str )  )

            fileobject.writelines('\n')
        return True


    #==================main body========================

    config_cp = configparser.ConfigParser()
    config_cp = config
    hint_str = ''
    isSpace_str = ' ' if space_around_delimiters else ''

    if isinstance(fileobject, str) and checkFile(filename=fileobject, check_creatable=True): # if fileobject is a file name string
        f = open( path.realpath( path.expanduser(fileobject) ), 'wt')
    elif isinstance(fileobject, io.TextIOBase):
        f = fileobject

    if isinstance(sequence, dict) and len(sequence) != 0: # if a sequence dictionary is given
        # write [DEFAULT] section
        f.writelines('[DEFAULT]\n')
        if 'DEFAULT' in list( sequence.keys() ):
            for key_str in sequence['DEFAULT']: # write some keys in priority
                hint_str = '   # ' + hint[ ('DEFAULT', key_str) ] if isinstance(hint, dict) and ('DEFAULT', key_str) in hint.heys() else ''
                try:
                    f.writelines( '{0}{2}={2}{1}{3}\n'.format( key_str , config_cp.defaults()[key_str], isSpace_str, hint_str  ) )
                    if config_cp.remove_option('DEFAULT', key_str):
                        print("Warning: NoOptionError. The [DEFAULT] section doesn't have key {}.".format(key_str) )
                except configparser.NoSectionError:
                    print("Warning: NoSectionError. The configParser object doesn't have DEFAULT section.")


        #write the rest of ['DEFAULT'] section in config_cp
        keys_lst = list( config_cp.defaults().keys() )
        keys_lst.sort()
        for key_str in keys_lst:
            hint_str = '   # ' + hint[ ('DEFAULT', key_str) ] if isinstance(hint, dict) and ('DEFAULT', key_str) in hint.heys() else ''
            try:
                f.writelines( '{0}{2}={2}{1}{3}\n'.format(key_str, config_cp.defaults()[key_str], isSpace_str, hint_str ) )
                if not config_cp.remove_option('DEFAULT', key_str):
                    print("Warning: NoOptionError. The [DEFAULT] section doesn't have key {}.".format(key_str) )
            except KeyError:
                print('"config" object does NOT have option "{}"\n'.format(key_str) )
                raise KeyError

        f.writelines('\n')

        #============================================================
        # write the non-default sections
        # write the customed key in priority
        for sectionName_str in sequence['Sections']:
            if sectionName_str == "DEFAULT": # section ["DEFAULT"] should always on the top in the file
                continue

            f.writelines( '[{}]\n'.format(sectionName_str) )
            for key_str in sequence[sectionName_str]:
                hint_str = '   # ' + hint[ (sectionName_str, key_str) ] if isinstance(hint, dict) and (sectionName_str, key_str) in hint.heys() else ''
                try:
                    f.writelines('{0}{2}={2}{1}{3}\n'.format( key_str, config_cp[sectionName_str][key_str], isSpace_str, hint_str  ) )
                    if not config_cp.remove_option( sectionName_str, key_str ):
                        print("Warning: NoOptionError. The [{}] section doesn't have key {}.".format( sectionName_str ,key_str) )
                except configparser.NoSectionError:
                    print("Warning: NoSectionError. The configParser object doesn't have {} section.".format(sectionName_str) )

            #write the rest of the section in config_cp
            keys_lst = list( config_cp[sectionName_str].keys() )
            keys_lst.sort()
            for key_str in keys_lst:
                hint_str = '   # ' + hint[ (sectionName_str, key_str) ] if isinstance(hint, dict) and (sectionName_str, key_str) in hint.heys() else ''
                try:
                    f.writelines( '{0}{2}={2}{1}{3}\n'.format( key_str, config_cp[sectionName_str][key_str], isSpace_str, hint_str ) )
                    if not config_cp.remove_option( sectionName_str, key_str ):
                        print("Warning: NoOptionError. The [{}] section doesn't have key {}.".format( sectionName_str ,key_str) )
                except configparser.NoSectionError:
                    print("Warning: NoSectionError. The configParser object doesn't have {} section.".format(sectionName_str) )

            f.writelines('\n')
            if config_cp.options(sectionName_str) == []:
                if not config_cp.remove_section(sectionName_str):
                    print( "Warning: NoSectionError. The configParser object doesn't have {} section.".format(sectionName_str) )
            else:
                print("Section [{}] can't be removed, because it still have option {}".format( sectionName_str , config_cp.options(sectionName_str)) )

        __c_to_i(config_cp, f, space_around_delimiters)

    elif sequence == 'sorted':   # only write sorted configuration, no custom sequences needed
        #write the ['DEFAULT'] section in config_cp
        f.writelines('[DEFAULT]\n')
        keys_lst = list( config_cp.defaults().keys() )
        keys_lst.sort()
        for key_str in keys_lst:
            hint_str = '   # ' + hint[ ('DEFAULT', key_str) ] if isinstance(hint, dict) and ('DEFAULT', key_str) in hint.heys() else ''
            f.writelines( '{0}{2}={2}{1}\n'.format(key_str, config_cp.defaults()[key_str], isSpace_str ) )
            config_cp.remove_option('DEFAULT', key_str)

        f.writelines('\n')
        __c_to_i(config_cp, f, space_around_delimiters)

    else: # just write as if configparser.ConfigParser().write does
        config_cp.write(f, space_around_delimiters)

    f.close()

    return

def cprint(string, pos=[], style=[ [1,31] ], end='\n'):
    '''
    This function will print a string in a given position using color and style with ANSI escape character 'ESC' (ASCII decimal 27 / hex 0x1B / octal 033)
    More detail on https://en.wikipedia.org/wiki/ANSI_escape_code fragment

    Parameters:
        **string**: string
            The string you want to print in colors and special styles

        **pos**: 2D list
            It contains several range lists such as [ [start_pos1, end_pos1], [start_pos2, end_pos2], .... ]. Empty list [] means whole string.

            For example if you want to print out a string, in which the first and second chars in a customed style, and 5th-7th chars in another style
            you should set pos as [ [0,2], [4,7] ]. Hereby [0,2] means the first and second chars and [4,7] means 5th-7th chars

        **style**:2D list
            It contains several integer lists. Each item represents a print style. More detail on https://en.wikipedia.org/wiki/ANSI_escape_code

            For example if you want to print first character segment in a string in bright red underline and second character segment in faint cyan cross-out
            you should set style as [ [1,4,31], [2,9,36] ]. Hereby [1,4,31] means bright red underline and [2, 9, 36] for faint cyan cross-out.

        *Obviously parameters 'pos' and 'style' must be in an equal length, unless pos is left empty as default*

    Returns:
        **value**: integer
            0 if successful, otherwise raise an exception

    Usage: cprint('Print bright red and dark blue', pos=[[6,16], [21,30]], style=[[1,31], [2,34]] )
    '''
    #================format check=================

    if not isinstance(string, str):
        message = 'cprint needs a string as "string" parameter, instead a {0} is given.'.format(type(string))
        raise TypeError(message)

    if isinstance(pos, list):
        for lst in pos:
            if not isinstance(lst, list):
                message = 'Parameter "pos" expects a 2-D list, but it looks like an 1-D list.'
                raise TypeError(message)
    else:
        message = 'cprint needs a List as "pos" parameter, instead a {0} is given.'.format(type(pos))
        raise TypeError(message)

    if isinstance(style, list):
        for lst in style:
            if not isinstance(lst, list):
                message = 'Parameter "style" expects a 2-D list, but it looks like a 1-D list.'
                raise TypeError(message)
    else:
        message = 'cprint needs a List as "style" parameter, instead a {0} is given.'.format(type(style))
        raise TypeError(message)

    if pos != [] and len(style) != len(pos):
        message = 'cprint: "style" (len:{})and "pos" (len:{}) parameter must be in an equal length.'.format(len(style), len(pos))
        raise ValueError(message)

    #================format check over================
    pos_lst = [ [-1, 0] ] # -1 is not important, any thing like [ [x, 0] ] is feasible
    if pos == []:  # you have to add an extra
        pos_lst.extend( [ [0, len(string)] ] )
    else:
        pos_lst.extend( pos )

    makestyle_str = lambda lst: '\033[' + ';'.join( [ str(x) for x in lst] ) + 'm'   # construct an escape sequence. makestyle_str([1,32]) will return '\x1b[1;32m'
    restore_str = '\033[0m'

    stylefreg_str = ''
    for i in range( 1, len(pos_lst) ):
        stylefreg_str += string[ pos_lst[i-1][1]:pos_lst[i][0] ] + makestyle_str(style[i-1]) + string[ pos_lst[i][0]:pos_lst[i][1] ] + restore_str

    stylefreg_str += string[ pos_lst[-1][1] : ]
    print(stylefreg_str, end=end)
    return

def ckprint(string, keyword, style=[1,31], case_sensitive=True, end='\n') :
    '''
    This function will print a string and highlight the given keyword in a given style
    The style is implemented by ANSI escape character 'ESC' (ASCII decimal 27 / hex 0x1B / octal 033), more detail on https://en.wikipedia.org/wiki/ANSI_escape_code

    Parameters:
        **string** : String
            The string you want to print out

        **keyword**: List
            The keywords that will be highlighted

        **style**: List
            The keywords that will be highlighted in this style

        **case_sensitive**: Boolean.
            Should be keywords be searches case sensitively ?

    Example:
        s = 'Python Type "help", "copyright", "credits" or "license" for more information.'

        ckprint(s, ['op','ts', 'or']).

        The keywords in string will be printed out in light red.
    '''
    import re
    #=========================check format==============================
    if not isinstance(string, str):
        raise TypeError('ckprint needs a string as parameter "string", instead a {0} is given.'.format( type(string) ) )

    if not isinstance(keyword, list):
        raise TypeError('ckprint needs a List as parameter "keyword", instead a {0} is given.'.format( type(keyword) ) )

    if not isinstance(style, list):
        raise TypeError('ckprint needs a List as parameter "style", instead a {0} is given.'.format( type(style) ) )

    if not isinstance(case_sensitive, bool):
        raise TypeError('ckprint needs a boolean as parameter "case_sensitive", instead a {0} is given.'.format( type(case_sensitive) ) )
    #=====================format check over==============================

    makepattern_str = lambda lst: '(' + ')|('.join(lst) + ')'  # pattern for re module, makepattern_str( ['a', 'be', 'op'] ) will return '(a)|(be)|(op)'
    keyPos_lst = [] # to store the postition of keywords, like [ [10,12], [35, 40] ....   ]
    if case_sensitive:
        for r in re.finditer( makepattern_str(keyword), string): # search all positions of keywords in one hit-item
            keyPos_lst.append( [ r.start(), r.end() ] )
    else:
        for r in re.finditer( makepattern_str(keyword), string, flags=re.IGNORECASE ): # search all positions of keywords in one hit-item
            keyPos_lst.append( [ r.start(), r.end() ] )

    if keyPos_lst != []: # if we found the keyword
        cprint(string, style= [style]*len(keyPos_lst), pos = keyPos_lst,end=end)
    else:
        print(string, end=end)

    return

def environment_check(packages=None, python=None, system=None, softwares=None):
    '''
    Do a simple routine environment check

    Parameters:
        packages: None or a List. The python packages you want to check if installed, such as ['pandas', 'numpy', .....]
        python: None or a string, such as '3.5.2'
        system: None or a string. 'Linux', 'Windows', or 'Java' etc.
        softwares: None or a List. The software you want to check, such as ['samtools', 'java'.....]

    If any error occured, it will exit, no return value
    '''
    import platform, sys, re, importlib, os

    #===================format check===========================
    if not isinstance(packages, list) and packages != None:
        print( 'environment_check method expects a list or None for parameter "packages", instead type {0} was given.'.format( type(packages) )  )
        raise TypeError

    if not isinstance(python, str) and python != None:
        print( 'environment_check method expects a string or None for parameter "python", instead type {0} was given.'.format( type(python) )  )
        raise TypeError
    elif python != None:
        if python.count('.') > 2 or re.search( r'[^0-9.]', python ) != None: # contain too many '.' or contain characters other than '.' and number
            print('Wrong format for parameter "python": {0} '.format(python) )
            raise AttributeError
    else:
        pass

    if not isinstance(system, str) and system != None:
        print( 'environment_check method expects a string or None for parameter "system", instead type {0} was given.'.format( type(system) )  )
        raise TypeError
    #====================format check over======================

    if packages != None:  # check the packages
        temp_lst = []
        for module_str in packages:
            try:
                importlib.import_module(module_str)
            except ImportError as ex:
                temp_lst.append( ex.args[0].split("'")[1] )
                continue

        if temp_lst != []:
            print('This program needs packages "{0}" to run.'.format( ' '.join(temp_lst) )  )
            print('Use "pip3 install {0}" to install required python packages.'.format( ' '.join(temp_lst) ) )
            os._exit(1)


    if python != None:
        if sys.version.split()[0] < python:
            print('This program needs python {0} or newer to run, but only python {1} is installed.'.format( python, sys.version.split()[0] )  )
            os._exit(1)

    if system != None:    # check system
        if platform.system() != system:
            print( 'This module is {0}-specific, it can not run in {1}'.format( system, platform.system() ) )
            os._exit(1)

    if softwares != None:
        temp_lst = []
        for software_str in softwares:
            try:
                r = run(software_str)
            except FileNotFoundError:
                if r[0] == 128:
                    temp_lst.append( software_str )
                    continue

        if temp_lst != []:
            print('This program needs softwares "{0}" to run.'.format( ' '.join(temp_lst) )  )
            print('Install necessary sotwares before run this program.')
            os._exit(1)

    return

def get_cpu_int(default= 2) -> int:

    command_str = 'cat /proc/cpuinfo | grep "processor"'
    try:
        r = run(command_str, False)
        if r[0] == 0:
            CPU_INT = int( len(r[1].split('\n')) )
            CPU_INT = max( [1, CPU_INT] )
        else:
            raise SystemError

    except:
        CPU_INT = default

    return CPU_INT

def get_free_mem():
    '''
    Return machine free memory in {integer} MB
    return -1 on failure
    '''
    command_str = 'cat /proc/meminfo | grep "MemAvailable:"'
    try:
        r = run(command_str, False)
        if r[0] == 0:
            free_mem = int(int(r[1].split()[1])/1000)
            return free_mem
        else:
            raise OSError(r[2])

    except:
        return -1

def ini_to_config(ini_file, comment_mark='#'):
    '''
    This function is meant to replace configparser.ConfigParser().read()
    The original configparser.ConfigParser().read() fuction can't recogonize the comments in the config file.
    This function can read a commented configuration file into a configparser.ConfigParser() object

    Parameter:
        ini_file: string. The config file you want to read
        comment_mark: a string , usually '#' or '//'. Every string after the comment_mark will be ignored.

    Return:
        config: a configparser.ConfigParser() object
    '''

    import configparser, tempfile
    import os.path as path

    file_str = path.realpath( path.expanduser(ini_file) )
    checkFile( filename=file_str, check_readable=True )

    ini_f = open(file_str)
    temp_f = tempfile.TemporaryFile('w+t')

    for s in ini_f.readlines():
        if comment_mark in s and s[ : len(comment_mark) ] == comment_mark: # if the line starts with the comment_mark
            continue
        else:
            temp_f.writelines( s.split( comment_mark )[0] + '\n'  )

    ini_f.close()
    temp_f.seek(0)
    config = configparser.ConfigParser()
    config.read_file(temp_f)
    temp_f.close()
    if len(config.sections()) == 0:
        print('Warning: Not section found in config object')
    return config

def HowManyLinesToSkip(inputfile_str, skipmark_str = "#"):

    """
    Figure out how many lines to skip the header lines, which are marked by $skipmark_str in front

    Return:
        an non-negative integar if successful

        otherwise return
            -1, input format error
            -2, can't open input file
    """
    skip_int = 0

    if not isinstance(inputfile_str, str) or not isinstance(skipmark_str, str):
        return -1

    try:
        f = open(inputfile_str, mode="rt")
    except:
        return -2

    for s in f.readlines():   # find out how many lines should skip when read the CSV file
        if s[0] == skipmark_str:
            skip_int += 1
            continue
        else:
            break
    f.close()

    return skip_int

def multi_run_backwards(ProcessList, simultaneous, print_name = True):
    '''
    Spawn multiple processes

    Parameter:
        ProcessList: a list of multiprocessing.Process objects

        simultaneous: an integer, how many process do you want to spawn simultaneously

    Return:
    '''

    from multiprocessing import Process
    #==========================
    if not isinstance(simultaneous, int):
        message = 'Paramater "simultaneous" expects an integer, istead a {} is given'.format(type(simultaneous))
        raise TypeError(message)
    elif simultaneous <= 0:
        message = 'Paramater "simultaneous" must be greater than 0, the current value is {}'.format(simultaneous)
        raise ValueError(message)

    if isinstance(ProcessList, list):
        if ProcessList == []:
            message = 'ProcessList is an empty list.'
            raise ValueError(message)
    else:
        message = 'Paramater "ProcessList" expects a list, istead a {} is given'.format(type(ProcessList))
        raise TypeError(message)
    #==========================

    run_lst = []
    for p in ProcessList:
        if not isinstance(p, Process):
            message = 'Paramater "ProcessList" expects a list of multiprocessing.Process objects, instead it contains a {} item.'.format(type(p))
            raise TypeError(message)

        run_lst.append(p)

        if len(run_lst) == simultaneous:
            for p_sub in run_lst:
                if print_name:
                    print(p_sub.name)
                p_sub.start()
            for p_sub in run_lst:
                p_sub.join()
            run_lst = []

    if run_lst != []:
        for p in run_lst:
            if print_name:
                print(p.name)
            p.start()
        for p in run_lst:
            p.join()

    return

def md5( file, base_convert= False ):
    '''
    A simple hashlib.md5 wrapper. Calculate md5 hash of a file.

    Do remember that the security of the MD5 has been severely compromised since 2012, so it should NOT be used for security purposes.

    Parameters:
        file: String. The file you want to do the hash

    Return:
        Return a 32 bytes MD5 hash string.
    '''

    import hashlib, os
    import os.path as path

    if not isinstance(file, str):
        raise TypeError( 'Parameter "file" needs to be a string, instead a {} is given.'.format( type(file) ) )
    #===================format check over==========================
    file_str = path.realpath( path.expanduser( file ) )

    if path.isdir(file_str):
        raise IsADirectoryError( 'Parameter "file" needs to be a file, but {} is folder.'.format( file_str ) )

    # b = base64.b64encode( s.encode('utf-8') ).decode('utf-8')
    if os.access( file_str, os.R_OK ):
        f = open(file_str, 'rb')
        return hashlib.md5( f.read() ).hexdigest()
    else:
        raise PermissionError( "File {} doesn't exists or is not readable.".format(file_str) )

def pileup_covert(pileup_str, ref_str):
    """
    Convert samtools mpileup string to a nucleobase sequence
    ".+3TTGGgg,+4ttgTT.-11atgacatctaTAAAAA......." ----> "GGCCCTGAAAAAGGGGGGG"

    Dependency:
        complement() is needed

    Paramters:

        str: pileup_str: Samtools pileup format string, see samtools mpileup command manual

        str: ref_str: captial genome sequence base, one of "A", "T", "C", "G"

    Returns:

        str: A coverted string, if successful

        otherwise returns an error code (integer)
         0, At least one of the inputs is not string
        -1, ref_str is not one of "A", "T", "C", "G"
        -2, "+" or "-" mark and number doesn't exist in pairs
        -3, A insertion or deletion length is longer than sequence it needs, for example ".,+11TGActtt.."

    """
    import re
    #============================format check ============================
    if str( type(pileup_str) ) != "<class 'str'>" or str( type(ref_str) ) != "<class 'str'>":
        return 0

    if ref_str not in ["A", "T", "C", "G"]:
        return -1
    #============================format check over============================

    pileupSym_str = pileup_str
    converted_str = ""


    # remove "^\S" quaility symbol
    temp = re.split( r"\^{1}\S{1}" ,pileupSym_str)
    pileupSym_str = "".join(temp)


    if "+" in pileupSym_str or "-" in pileupSym_str:

        cutLength_lst = re.findall(r"\+\d+|-\d+" ,pileupSym_str) # figure out the length of string to be phased out
        for i in range( 0, len(cutLength_lst) ):
            cutLength_lst[i] = len(cutLength_lst[i]) + int( cutLength_lst[i][1:] )

        start_lst = []
        for r in re.finditer ( r"\+|-{1}", pileupSym_str ):
            start_lst.append( r.start() )

        if len(cutLength_lst) != len(start_lst):  # They should be equal in length
            return -2

        for i in range( len(start_lst)-1, -1, -1 ):
            try:
                pileupSym_str = pileupSym_str[ : start_lst[i] ] + pileupSym_str[ start_lst[i] + cutLength_lst[i] : ]
            except:
                return -3
    #=============================== insertion and deletion removed=================================

    for s in pileupSym_str:
        if s == ".":
            converted_str = converted_str + ref_str
        elif s == ",":
            #converted_str = converted_str + complement(ref_str)
            converted_str = converted_str + ref_str
        elif s in "ATCG":
            converted_str = converted_str + s
        elif s in "atcg":
            #converted_str = converted_str + complement(s).upper()
            converted_str = converted_str + s.upper()
        else:
            continue

    return converted_str

def pileup_decode( pileup_se, ref_se, index="None", allowempty=False ):

    """
        v0.1
        Convert a pandas series of samtools mpileup string to series of a nucleobase sequence
        ".+3TTGGgg,+4ttgTT.-11atgacatctaTAAAAA......." ----> "GGCCCTGAAAAAGGGGGGG"

        Dependency:
            Pandas, _pileup_convert() is needed

        Paramters:

            pileup_se: A Pandas Series of samtools pileup format string, see samtools mpileup command manual for detail

            ref_se: A Pandas Series of captial genome sequence base, in which every item must be one of "A", "T", "C", "G"

            index: String, either "P" or "R" or "None"
                If "P", the resulting axis will be labeled as same as pileup_se
                If "R", the resulting axis will be labeled as same as ref_se
                If "None", the resulting axis will be labeled 0, ..., n - 1. This is useful if you are concatenating
                objects where the concatenation axis does not have meaningful indexing information.

            allowempty: boolean, default False
                If True, results (pandas series) can contain empty strings, otherwise it will be replaced by np.NaN

        Returns:

            A coverted Pandas Series, if successful
            every item in it is converted string or integer, see _pileup_convert for more detail

            otherwise returns an error code (integer)
             0, At least one of the inputs is not Pandas Series
             -1, pileup_se and ref_se don't have equal length
        """
    import pandas as pd

    decode_str = ""
    decode_se = pd.Series()

    if str( type(pileup_se) ) != "<class 'pandas.core.series.Series'>" or str( type(ref_se) ) != "<class 'pandas.core.series.Series'>":
        return 0

    if len(pileup_se) != len(ref_se):
        return -1

    if index not in ["P", "R", "None"]:
        return -2
    #===================format check over==========================

    p_se = pd.Series(); r_se = pd.Series()

    p_se = pd.Series.copy( pileup_se )
    r_se = pd.Series.copy( ref_se )

    if index == "P":
        r_se.index = p_se.index
        temp_pd = pd.DataFrame( dict(Ref=r_se, Pileup=p_se), index=p_se.index )

    elif index == "R":
        p_se.index = r_se.index
        temp_pd = pd.DataFrame( dict(Ref=r_se, Pileup=p_se), index=r_se.index )

    else:
        p_se.index = pd.Series( range(0, len( p_se ) ) )
        r_se.index = pd.Series( range(0, len( r_se ) ) )
        temp_pd = pd.DataFrame( dict(Ref=r_se, Pileup=p_se), index=r_se.index )

    for tu in temp_pd.iterrows():
        decode_str = _pileup_covert( str(tu[1][0]), str(tu[1][1]) )
        if decode_str == "" and not allowempty:
            decode_str = pd.np.NaN

        decode_se = pd.concat( [ decode_se, pd.Series( decode_str, index=[tu[0]] ) ], ignore_index = True if index == "None" else False )

    return decode_se


def spacing_text(text):
    """
    Perform paranoid text spacing on text.
    Input: text
    return: a new test with a space between every non-Chinese char and Chinese char
    """
    new_text = text

    if len(new_text) < 2:
        return new_text

    new_text = CJK_QUOTE_RE.sub(r'\1 \2', new_text)
    new_text = QUOTE_CJK_RE.sub(r'\1 \2', new_text)
    new_text = FIX_QUOTE_RE.sub(r'\1\3\5', new_text)
    new_text = FIX_SINGLE_QUOTE_RE.sub(r'\1\3\4', new_text)

    new_text = CJK_HASH_RE.sub(r'\1 \2', new_text)
    new_text = HASH_CJK_RE.sub(r'\1 \3', new_text)

    new_text = CJK_OPERATOR_ANS_RE.sub(r'\1 \2 \3', new_text)
    new_text = ANS_OPERATOR_CJK_RE.sub(r'\1 \2 \3', new_text)

    old_text = new_text
    tmp_text = CJK_BRACKET_CJK_RE.sub(r'\1 \2 \4', new_text)
    new_text = tmp_text
    if old_text == tmp_text:
        new_text = CJK_BRACKET_RE.sub(r'\1 \2', new_text)
        new_text = BRACKET_CJK_RE.sub(r'\1 \2', new_text)
    new_text = FIX_BRACKET_RE.sub(r'\1\3\5', new_text)

    new_text = FIX_SYMBOL_RE.sub(r'\1\2 \3', new_text)

    new_text = CJK_ANS_RE.sub(r'\1 \2', new_text)
    new_text = ANS_CJK_RE.sub(r'\1 \2', new_text)

    return new_text.strip()

def readable(file, check_zero_size = True):
    '''
    check if file can be read, file can contain '~' or '..' etc.

    Return file size (bytes in integer) if file exists, otherwise False
    '''
    import os
    import os.path as path
    real_file = path.realpath(path.expanduser(file))
    if os.access(real_file, os.R_OK):
        if check_zero_size and path.getsize(real_file) == 0:
            return False
        else:
            return True

    else:
        return False

def run(command_str:str, verbose= True, manager_dict= None, key= None, wait=None, dummy_mode= False):
    '''
    A simple subprocess wrapper, v0.2a

    Parameters:
        **command_str**: string
            The terminal command you want to run.

        **verbose**: boolean
            If true a real-time output will be printed out, otherwise output will be buffered and printed out after child process exits.

            When true, stdout and stderr will be printed out together ( not fully tested ) and parameter 'wait' will be ignored.

        **manager_dict**: multiprocessing.managers.DictProxy or None
            A multiprocessing.Manager().dict() instance, used for store the return list object [returncode, stdout, stderr] when function is called in multiprocessing.

            It can be set to None if the function is not called in multiprocessing.

        **key**: any or None
            If not None, when manager_dict is set, this parameter will be the key of manager_dict

            Otherwise parameter command_str will be used as key.

        **wait**: integer or None
            A wrapper of Popen.wait(timeout=None)

    Returns:
        **[returncode, stdout, stderr]**: list
            return list object [returncode, stdout, stderr]
    '''
    import multiprocessing, subprocess, shlex, os, sys

    #==============================================================================================
    if not isinstance(command_str, str):
        message = 'Parameter command_str expects a string, instead type {} was given.'.format(type(command_str))
        raise TypeError(message)

    if not isinstance(verbose, bool):
        message = 'Parameter verbose expects a boolean, instead type {} was given.'.format(type(verbose))
        raise TypeError(message)

    if not str( type( multiprocessing.Manager().dict() ) ) == "<class 'multiprocessing.managers.DictProxy'>" and manager_dict is not None:
        message = 'Parameter manager_dict expects a multiprocessing.managers.DictProxy or None, instead type {} was given.'.format(type(manager_dict))
        raise TypeError(message)

    if not isinstance(wait, int) and not isinstance(wait, float) and wait is not None:
        message = 'Parameter wait expects a numeric or None, instead type {} was given.'.format(type(wait))
        raise TypeError(message)

    if not isinstance(dummy_mode, bool):
        message = 'Parameter dummy_mode expects a boolean, instead type {} was given.'.format(type(dummy_mode))
        raise TypeError(message)
    #==============================================================================================
    if dummy_mode:
        print("[ATTENTION]Run in dummy mode: " + command_str)
        return [0, '', '']

    # if there's pipe in the command_str, then shell=TRUE must be used and it is recommended to pass args as a string rather than as a sequence.
    if '~' in command_str or '*' in command_str or '?' in command_str or "|" in command_str or ">" in command_str or "<" in command_str or "&" in command_str:
        useShell_bool = True
        command = command_str

    else:  # if there's no pipe in the command_str
        useShell_bool = False
        command = shlex.split(command_str)

    output_str = ""; error_str = ""
    if verbose:   # if we need real-time output
        r = subprocess.Popen( command, shell=useShell_bool, stdout=subprocess.PIPE, stderr= subprocess.STDOUT, universal_newlines=True )
        while True:  # Loop to print every line until process ends
            try:  # handle stdout
                line_str = r.stdout.readline()
            except UnicodeDecodeError as ex:
                print(ex)
            except Exception as ex:
                print('An error occured when read output from command "{}" '.format( command ) )
                raise ex

            if not line_str and r.poll() is not None:  # That r.poll() is None means the process hasn’t terminated yet.
                break

            if line_str != "":
                print( line_str.strip() )
                output_str += line_str

    else:  # if we don't need real-time output
        try:
            r = subprocess.Popen( command, shell=useShell_bool, stdout=subprocess.PIPE, stderr= subprocess.PIPE, universal_newlines=True )
            r.wait(wait)
        except Exception as ex:
            print('An error occured on subprocess.Popen, {} '.format( command ) )
            raise ex

        for s in r.stdout.readlines():
            output_str += str(s)

        for s in r.stderr.readlines():
            error_str += str(s)

    try:
        if isinstance(manager_dict, multiprocessing.managers.DictProxy):
            if key is None:
                manager_dict[command_str] = [r.returncode, output_str.strip() , error_str.strip() ]
            else:
                manager_dict[key] = [r.returncode, output_str.strip() , error_str.strip() ]
    except:
        message = 'The command "{command_str}......" was executed but fail to assign return list to multiprocessing.managers.DictProxy {manager_dict}'.format(command_str= command_str,
                                                                                                                                                              manager_dict= manager_dict)
        cprint(message)
        raise

    return [r.returncode, output_str.strip(), error_str.strip() ]



def remove_all(lst, value, inplace= True):
    """Remove all instances of value from lst"""
    if inplace:
        lst[:] = (x for x in lst if x != value) # that doesn't equal value
    else:
        temp = lst.copy()
        temp[:] = (x for x in temp if x != value)
        return temp


def warn(*args, **kwargs):
    '''
    Print messages to stderr
    '''
    print(*args, file=sys.stderr, **kwargs)



def multi_run(ProcessList:list, simultaneous:int, join = 300, verbose = True):
    '''
    Spawn multiple processes

    Parameter:
        **ProcessList**: List
            A list, in which each item is a multiprocessing.Process() objects

        **simultaneous**: int
            An integer, how many processes do you want to spawn simultaneously?

        **join**: int
            Make a memory collection after N processes finish.
            Lower it if you have 8GB or less RAM.

        **verbose**: bool
            Whether print process's name what a process starts ?

    Return:
        None on success
    '''
    from multiprocessing import Process
    import time
    #==========================
    if not isinstance(simultaneous, int):
        message = 'Paramater "simultaneous" expects an integer, istead a {} is given'.format(type(simultaneous))
        raise TypeError(message)
    elif simultaneous <= 0:
        message = 'Paramater "simultaneous" must be greater than 0, the current value is {}'.format(simultaneous)
        raise ValueError(message)

    if isinstance(ProcessList, list):
        if ProcessList == []:
            message = 'ProcessList is an empty list.'
            raise ValueError(message)
        else:
            for p in ProcessList:
                if not isinstance(p, Process):
                    message = 'Paramater "ProcessList" expects a list of multiprocessing.Process objects, instead it contains a {} item.'.format(type(p))
                    raise TypeError(message)
    else:
        message = 'Paramater "ProcessList" expects a list, instead a {} is given'.format(type(ProcessList))
        raise TypeError(message)
    #==========================

    running_process_int = 0  # how many processes are actually active. A process existing in memory but not carring any payload is not be considered as 'active'
    running_process_lst = []
    while len(ProcessList) > 0:
        try:
            if running_process_int < simultaneous:
                p = ProcessList.pop(0)
                if verbose:
                    local_time = time.localtime()
                    message = '[{year}-{month:>02}-{day:>02} {hour:>02}:{min:>02}:{sec:>02}] {process_name}'.format(process_name= p.name,
                                                                                                                    year= local_time.tm_year,
                                                                                                                    month= local_time.tm_mon,
                                                                                                                    day= local_time.tm_mday,
                                                                                                                    hour= local_time.tm_hour,
                                                                                                                    min= local_time.tm_min,
                                                                                                                    sec= local_time.tm_sec)
                    cprint(message, style= [[1,96]] )
                p.start()
                running_process_lst.append(p)
        except Exception as ex:
            message = '[{year}-{month:>02}-{day:>02} {hour:>02}:{min:>02}:{sec:>02}] {ex}'.format(ex= ex,
                                                                                                  year= local_time.tm_year,
                                                                                                  month= local_time.tm_mon,
                                                                                                  day= local_time.tm_mday,
                                                                                                  hour= local_time.tm_hour,
                                                                                                  min= local_time.tm_min,
                                                                                                  sec= local_time.tm_sec)
            cprint(message)

        running_process_int = 0  # how many processes are currently running ?
        for running_p in running_process_lst:
            if running_p.is_alive():
                running_process_int += 1

        if len(running_process_lst) == 500:
            for running_p in running_process_lst:
                try:
                    running_p.join()
                except Exception as ex:
                    message = '[{year}-{month:>02}-{day:>02} {hour:>02}:{min:>02}:{sec:>02}] {ex}'.format(ex= ex,
                                                                                                          year= local_time.tm_year,
                                                                                                          month= local_time.tm_mon,
                                                                                                          day= local_time.tm_mday,
                                                                                                          hour= local_time.tm_hour,
                                                                                                          min= local_time.tm_min,
                                                                                                          sec= local_time.tm_sec)
                    cprint(message)

            running_process_lst = []

        time.sleep(0.25)

    for running_p in running_process_lst:
        try:
            running_p.join()
        except Exception as ex:
            message = '[{year}-{month:>02}-{day:>02} {hour:>02}:{min:>02}:{sec:>02}] {ex}'.format(ex= ex,
                                                                                                  year= local_time.tm_year,
                                                                                                  month= local_time.tm_mon,
                                                                                                  day= local_time.tm_mday,
                                                                                                  hour= local_time.tm_hour,
                                                                                                  min= local_time.tm_min,
                                                                                                  sec= local_time.tm_sec)
            cprint(message)

    return None


#=======================class================================
