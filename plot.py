#!/usr/bin/python

import os
import matplotlib.pyplot as mplot
import itertools

from experiments import PATH_RESULTS, RESULT_SEP

PATH_PLOTS = 'plots'
PLOTS_EXTENSION = '.eps'
PLOT_COLORS = itertools.cycle('bgrcmyk')
# PLOT_STYLES = itertools.cycle('ov^<>1234sp*hH+xDd|_')
PLOT_STYLES = itertools.cycle('op^s+xd|<D1H_>2*45vh')

""" Set to 1 if you want to count only words that belong exclusively 
to ONE family. Set to 0 if you want to count words that simply belong to 
the family. """
exclusive = 0

""" Dear user, 
I really need to warn you before you make use of the following code. This code
is not really part of the Multiword Project, it was written to conduct several
(exhaustive and random) studies. Please, do not use this code on your own! 
You should better write your own code based on the other modules (certain.py, 
multiword.py, etc.). The code in this file is very specific to what we needed, 
I can not ensure that you will be fine with that... """


MACRO = {'fpp' : r'$\mathcal{F}_\mathregular{rep.3}$',
        'fpu' : r'$\mathcal{F}_\mathregular{p.unb.}$',
        'fa' : r'$\mathcal{F}_\mathregular{anch.}$',
        'fu' : r'$\mathcal{F}_\mathregular{unr.}$'}

def load_results_from_files(filenames):
    """ Aggregate the results that are in the files whose names or in
    given sequence of filenames. 
    filenames -- a list of filenames """
    
    def load_results_from_file(filename):
        f = open(os.path.join(PATH_RESULTS, filename))
        results = []
        for line in f:
            word, size, nplus, diff = line.split(RESULT_SEP)
            results.append((word, int(size)))
        return results
    
    results = []
    for filename in filenames:
        results += load_results_from_file(filename)
    return results

    
def prepare_results(results):
    """ Prepare a given set of results and return a dict structure that
    contains, for each size of words, a dict structure that contains, 
    for each number of states, a list of words that have this size and
    this number of states. """
    words = dict()
    
    for word, size in results:
        length = len(word)
        number_of_states = words.setdefault(length, dict())
        list_of_words = number_of_states.setdefault(size, [])
        if word not in list_of_words:
            list_of_words.append(word)
    
    return words
    

def plot_length(chart, prepared_results, length, label = ''):
    """ Plot onto chart the given results on one chart with:
    x-axis = number of states of the DFA
    y-axis = number of DFA having this number of states. 
    Only the data of results that concern given word length are considered. 
    
    chart -- A matplotlib.pyplot object.
    prepared_results -- A dict structure returned by prepare_results.
    length -- The words length to consider. 
    label -- The label to use. Default is length.
    """
    
    x_values = prepared_results[length].keys()
    x_values.sort()
    
    y_values = []
    for x_value in x_values:
        number = len(prepared_results[length][x_value])
        # VERY IMPORTANT, PLEASE READ!!!
        # When we first ran experiments, the number of DFA we computed for each
        # size n of word and each size s of alphabet was NOT s**n, but (s**n)/2.
        # We considered that, for instance, "aab" is equal to "bba" (there is 
        # just an isomorphism). The "2" in the following line of code is there 
        # to display the right number of DFA... Please note that the code 
        # actually present in experiments.py generates exactly (s**n). Thus, 
        # if you need to plot something using this function, be careful!!
        y_values.append(2 * number) 
    
    label_to_use = label if label != '' else str(length)
    
    # print 'Drawing for length %d : \n%s\n%s' % (length, '\t'.join([str(x) for x in x_values]), '\t'.join([str(x) for x in y_values]))
    chart.plot(x_values, y_values, 
                '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), 
                label = label_to_use)
    
    
if __name__ == '__main__':
    choice = raw_input('0) mdfa for |w|=14\n' + 
                       '1) mdfa_ab_2_16\n' + 
                       '2) mdfa_rand_ab_17_28\n' + 
                       '3) mdfa relative to |sigma|\n' +
                       '4) Size of the families for ab\n' + 
                       '5) Size of the families for abc\n' +
                       '6) Size of the families relative to |sigma|\n')
    choice = int(choice)
    if choice == 0:
        mplot.xlabel('Number of states')
        mplot.ylabel('Number of words')
        #mplot.title('Number of DFA\'s for each number of states')

        in_filenames = ['mdfa_ab_2_16.txt']
        results = prepare_results(load_results_from_files(in_filenames))
        out_filename = 'mdfa_ab_14' + PLOTS_EXTENSION

        results = prepare_results(load_results_from_files(in_filenames))

        plot_length(mplot, results, 14, '14')

        mplot.savefig(os.path.join(PATH_PLOTS, out_filename))
        mplot.show()

    elif choice == 1 or choice == 2:
        mplot.xlabel('Number of states')
        mplot.ylabel('Number of words')
        #mplot.title('Number of DFA\'s for each number of states')
        
        mplot.yscale('log')
        
        if choice == 1:
            in_filenames = ['mdfa_ab_2_16.txt']
        else:
            in_filenames = ['mdfa_rand_ab_17_28.txt']
        
        out_filename = in_filenames[0][:-4] + PLOTS_EXTENSION
        
        results = prepare_results(load_results_from_files(in_filenames))
        for size in results.keys():
            plot_length(mplot, results, size)
        
        if choice == 1:
            mplot.legend(loc = 2)
        else:
            mplot.legend(loc = 1)
        mplot.savefig(os.path.join(PATH_PLOTS, out_filename))
        mplot.show()
    elif choice == 3: 
        alphabets = ['ab', 'abc', 'abcd', 'abcde']
        words_length = 8
        
        mplot.xlim(words_length, words_length + words_length / 2 + 1)
        
        mplot.xlabel('Number of states')
        mplot.ylabel('Number of words')
        #mplot.title('Different alphabet sizes, |w| = %d.' % words_length)
         
        mplot.yscale('log')
        
        for alphabet in alphabets:
            print 'Considering %s...' % alphabet
            results = load_results_from_files(['mdfa_%s_%d_%d.txt' % (alphabet, words_length, words_length)])
            print 'Preparing results...'
            results = prepare_results(results)
            print 'Plotting...\n'
            plot_length(mplot, results, words_length, 'Size %d' % len(alphabet))
        
        mplot.legend(loc = 1)
        mplot.savefig(os.path.join(PATH_PLOTS, ('mdfa_alphabets_%d'+PLOTS_EXTENSION) % words_length))
        mplot.show()
    elif choice == 4 or choice == 5:
        
        if choice == 4:
            sizes = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
            results = []
            results.append((2, [0, 0], [2, 0], [0, 0], [2, 0], 0))
            results.append((4, [0, 0], [4, 2], [2, 0], [2, 0], 0))
            results.append((8, [2, 0], [6, 0], [6, 0], [4, 0], 0))
            results.append((16, [2, 0], [10, 6], [4, 0], [4, 0], 4))
            results.append((32, [2, 0], [14, 4], [14, 4], [8, 4], 8))
            results.append((64, [4, 0], [28, 10], [26, 8], [8, 2], 22))
            results.append((128, [4, 0], [42, 8], [56, 20], [16, 8], 52))
            results.append((256, [4, 0], [84, 26], [100, 36], [24, 12], 114))
            results.append((512, [10, 0], [154, 44], [194, 76], [40, 20], 244))
            results.append((1024, [10, 4], [300, 118], [356, 148], [72, 38], 502))
            results.append((2048, [10, 4], [570, 252], [648, 292], [132, 86], 1052))
            results.append((4096, [22, 4], [1150, 590], [1170, 536], [252, 158], 2156))
            results.append((8192, [22, 12], [2234, 1276], [2130, 1024], [480, 320], 4444))
            results.append((16384, [22, 14], [4468, 2798], [3844, 1884], [940, 640], 9080))
            results.append((32768, [52, 20], [8866, 5924], [6916, 3476], [1824, 1292], 18584))
            results.append((65536, [52, 32], [17706, 12566], [12498, 6320], [3660, 2600], 37820))
            
        if choice == 5:
            sizes = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
            results = []
            results.append((3, [0, 0], [3, 0], [0, 0], [3, 0], 0))
            results.append((9, [0, 0], [9, 6], [3, 0], [3, 0], 0))
            results.append((27, [3, 0], [21, 6], [18, 0], [9, 0], 0))
            results.append((81, [3, 0], [57, 18], [48, 0], [15, 0], 12))
            results.append((243, [3, 0], [147, 30], [150, 12], [39, 12], 48))
            results.append((729, [9, 0], [441, 90], [474, 66], [93, 24], 132))
            results.append((2187, [9, 0], [1245, 144], [1578, 300], [243, 54], 402))
            results.append((6561, [9, 0], [3735, 378], [4950, 1062], [735, 192], 1032))
            results.append((19683, [33, 0], [11055, 804], [15666, 3840], [2037, 426], 2754))
            results.append((59049, [33, 12], [33111, 2214], [48720, 12738], [6291, 1182], 6900))
            results.append((177147, [33, 18], [98877, 5634], [150780, 42156], [18303, 2904], 17796))
            results.append((531441, [105, 12], [296697, 15564], [463590, 134778], [55689, 7914], 44268))
            results.append((1594323, [105, 54], [888627, 41700], [1420818, 428226], [165219, 19500], 112200))
            results.append((4782969,[105, 78],[2665881, 112806],[4338714, 1338828],[498975, 52134],279210))
        
        mplot.xlabel('|w|')
        mplot.ylabel('Percentage of words')
        #mplot.title('Coverages of the families, alphabet has %d symbols.' % (choice - 2))
        
        prim = [x[1][exclusive] * 100.0 / x[0] for x in results]
        unb = [x[2][exclusive] * 100.0 / x[0] for x in results]
        anc = [x[3][exclusive] * 100.0 / x[0] for x in results]
        ove = [x[4][exclusive] * 100.0 / x[0] for x in results]
        other = [x[5] * 100.0 / x[0] for x in results]
        
        # mplot.plot(sizes, words, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = '# words')
        mplot.plot(sizes, prim, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = MACRO['fpp'])
        mplot.plot(sizes, unb, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = MACRO['fpu'])
        mplot.plot(sizes, anc, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = MACRO['fa'])
        mplot.plot(sizes, ove, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = MACRO['fu'])
        mplot.plot(sizes, other, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = 'others')
        
        mplot.ylim(0, 100)
        
        if choice == 4:
            mplot.xlim(0, 17)
            mplot.legend(loc = 1)
            mplot.savefig(os.path.join(PATH_PLOTS, 'families_ab_1_16'+PLOTS_EXTENSION))
        elif choice == 5:
            mplot.xlim(1, 15)
            mplot.legend(loc = 2)
            mplot.savefig(os.path.join(PATH_PLOTS, 'families_abc_1_14'+PLOTS_EXTENSION))
        mplot.show()
    elif choice == 6:
        mplot.xlabel('$|\\Sigma|$')
        mplot.ylabel('Percentage of words')
        #mplot.title('Coverages of the families, |w| = 8.')
        
        sizes = (2, 3, 4, 5, 6)
        results = []
        results.append((256, [4, 0], [84, 26], [100, 36], [24, 12], 114))
        results.append((6561, [9, 0], [3735, 378], [4950, 1062], [735, 192], 1032))
        results.append((65536, [16, 0], [45328, 2460], [56640, 7176], [7864, 1248], 5172))
        results.append((390625, [25, 0], [297525, 11060], [354580, 28740], [45285, 5880], 19080))
        results.append((1679616, [36, 0], [1354356, 40950], [1557540, 85500], [181776, 23100], 57990))
        
        prim = [x[1][exclusive] * 100.0 / x[0] for x in results]
        unb = [x[2][exclusive] * 100.0 / x[0] for x in results]
        anc = [x[3][exclusive] * 100.0 / x[0] for x in results]
        ove = [x[4][exclusive] * 100.0 / x[0] for x in results]
        other = [x[5] * 100.0 / x[0] for x in results]
        
        mplot.xlim(sizes[0] - 1, sizes[-1] + 1)
        mplot.ylim(0, 100)
        # mplot.plot(sizes, words, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = '# words')
        mplot.plot(sizes, prim, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = MACRO['fpp'])
        mplot.plot(sizes, unb, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()),  label = MACRO['fpu'])
        mplot.plot(sizes, anc, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()),  label = MACRO['fa'])
        mplot.plot(sizes, ove, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()),  label = MACRO['fu'])
        mplot.plot(sizes, other, '%s-%s' % (PLOT_COLORS.next(), PLOT_STYLES.next()), label = 'others')
        
        mplot.legend(loc = 2)
        mplot.savefig(os.path.join(PATH_PLOTS, 'families_alphabets_8'+PLOTS_EXTENSION))
        mplot.show()
        
