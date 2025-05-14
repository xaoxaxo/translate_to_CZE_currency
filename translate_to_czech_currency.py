#!/usr/bin/python
# -*- coding: UTF-8 -*-
###############################################################################
# 
# Author        : xaoxaxo
# Description   : (CZECH) Vypiš hodnotu slovem, tak jako to dělá česká pošta :D
#
###############################################################################
import sys, codecs

def initialize_locale():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    if sys.platform == 'win32':
        try:
            import win32console 
        except:
            print ("Python Win32 Extensions module is required.\n You can download it from https://sourceforge.net/projects/pywin32 \n")
            exit(-1)
        # win32console implementation of SetConsoleCP does not return a value
        # CP_UTF8 = 65001
        win32console.SetConsoleCP(65001)
        if (win32console.GetConsoleCP() != 65001):
            raise Exception ("Cannot set console codepage to 65001 (UTF-8)")
        win32console.SetConsoleOutputCP(65001)
        if (win32console.GetConsoleOutputCP() != 65001):
            raise Exception ("Cannot set console output codepage to 65001 (UTF-8)")
    
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# do this for old python
if sys.version_info == (2,):
    initialize_locale()

def safeprint(s):
    try:
        print(s)        
    except UnicodeEncodeError:
        if sys.version_info >= (3,):
            print(s.encode('utf8').decode(sys.stdout.encoding))
        else:
            print(s.encode('utf8'))
    except:
        sys.stdout.write("Error\n")

#################################################
# replaces all whitespaces to one single space
def whitespaces_to_single_space (input):
    return ' '.join(input.split())


translatedict = {
1:  'jedna'     ,
2:  "dvě"       ,
3:  'tři'       ,
4:  'čtyři'     ,
5:  'pět'       ,
6:  'šest'      ,
7:  'sedm'      ,
8:  'osm'       ,
9:  'devět'     ,
10: 'deset'     ,
11: 'jedenáct'  ,
12: 'dvanáct'   ,
13: 'třináct'   ,
14: 'čtrnáct'   ,
15: 'patnáct'   ,
16: 'šestnáct'  ,
17: 'sedmnáct'  ,
18: 'osmnáct'   ,
19: 'devatenáct',
20: 'dvacet'    ,
30: 'třicet'    ,
40: 'čtyřicet'  ,
50: 'padesát'   ,
60: 'šedesát'   ,
70: 'sedmdesát' ,
80: 'osmdesát'  ,
90: 'devadesát' ,
100:'sto'      }

zenske = 1
muzske = 2

stotiny = lambda x: ['stě', 'sta', 'set'][((x in [3,4]) + (x in [5,6,7,8,9])*2)]
pluralcislonic =      lambda x: (zenske, '',       '')
pluralcislotisic =    lambda x: (muzske, 'tisíc',  ['', 'e', ''][((x in [2,3,4]) + (x in [5,6,7,8,9])*2)]  )
pluralcislomilion =   lambda x: (muzske, 'milion', ['ů', 'y', ''][((x in [2,3,4]) + (x in [1])*2)] )
pluralcislomiliarda = lambda x: (zenske, 'miliard',['', 'y', 'a'][((x in [2,3,4]) + (x in [1])*2)] )
pluralcislobilion =   lambda x: (muzske, 'bilion', ['ů', 'y', ''][((x in [2,3,4]) + (x in [1])*2)] )
tausendfunction = [pluralcislonic,pluralcislotisic,pluralcislomilion,pluralcislomiliarda,pluralcislobilion]


def correct_rod(x, y, rod):
    if x == 1 and rod == muzske:
        y = 'jeden'
    if x == 2 and rod == muzske:
        y = 'dva'
    return y

def translate(index, zbytek_po_deleni_tisic):
    thisnum = zbytek_po_deleni_tisic
    stovky = int(zbytek_po_deleni_tisic/100)
    finaltext = ''
    lastnum = 0

    if zbytek_po_deleni_tisic >= 200:
        finaltext += translatedict[stovky]
        finaltext += stotiny(stovky)
        finaltext += ' ' # mezerky
        thisnum -= stovky * 100


    try:
        postfixfn = tausendfunction[index]
    except:
        safeprint('Fakt moc velké číslo')
        sys.exit(0)

    #rod pro replacement jedna, dvě --- jeden, dva 
    rod, _, _ = postfixfn(lastnum)

    while thisnum:
        for x, y in reversed(sorted(translatedict.items(), key = lambda x: x[0])):
            if thisnum >= x:
                thisnum -= x
                lastnum = x
                y = correct_rod(x, y, rod)
                # v tabulce máme dvě, ale když je číslo npř dvacet dva, je to dva 
                if lastnum == 2 and index == 0 and zbytek_po_deleni_tisic != 2:
                    y = 'dva'
                finaltext += y + ' '

    # přípona množného čísla podle poslední nalezené číslice
    _, postfix, plural = postfixfn(lastnum) 

    #pokud neni nic ve finaltextu, nema ani smysl psat postfix (miliony, tisice)
    if finaltext == "": 
        postfix = ""
        plural = ""

    return finaltext + postfix + plural

def do_the_job(num):
    ori = num
    #safeprint( num )
    modnum = num % 1000
    currency = [" korun"," koruna"," koruny"][(modnum == 1) - (modnum in [2,3,4])]
    finaltext = ''
    index = 0
    while num:
        zbytek_po_deleni_tisic = num % 1000
        finaltext = translate(index, zbytek_po_deleni_tisic) + " " + finaltext 
        num -= zbytek_po_deleni_tisic
        if num:
            index += 1
            num /= 1000

    if finaltext == "":
        finaltext = "nula "
    safeprint(whitespaces_to_single_space(str(ori) + " -> " + finaltext.strip() + currency) )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            c = int(sys.argv[-1])
            do_the_job(c)
        except:
            print ("špatný vstup")
    else:
        testing_numbers = [0, 1, 2, 3, 4, 5, 6, 9, 23, 123, 199, 200, 222, 213, 333, 432, 444, 555, 666, 777, 888, 999, 
                        1000, 1001, 1002, 1111, 1577, 2222, 1999992, 13348821,
                        10000010, 16777216, 199199199, 1205055475, 9255355400, 10255355400,
                        100000000000, 1000000000000, 100000000100000, 999999999999999, 1000000000000000]
        for i in testing_numbers:
            do_the_job(i)
