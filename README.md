# multiwords
A set of tools to handle multiwords and the languages certain(w) in Python.

Multiwords are words in which a single symbol can be replaced by a nonempty set of symbols. They extend the notion of partial words. A word w is certain in a multiword M if it occurs in every word that can be obtained by selecting one single symbol among the symbols provided in each position of M . This set of tools, written in Python, allow to handle multiwords and the language certain(w) which, given a word w, is the language of every multiword in which the word w is certain.

See the following papers:
 - A. Decan. Certain Query Answering in First-Order Languages - Ph.D Thesis, University of Mons, Belgium. 2013.
 - V. Bruyere, O. Carton, A. Decan, O. Gauwin, J. Wijsen. An Aperiodicity Problem for Multiwords. RAIRO - Theoretical Informatics and Applications, 46, 2012, pp 33-50.
 - V. Bruyere, A. Decan, J. Wijsen. On First-Order Query Rewriting for Inconsistent Database Histories. 16th International Symposium on Temporal Representation and Reasoning, 2009, IEEE Computer Society, pages 54-61.
 

**IMPORTANT**

(A) - The code included in this repository DOES NOT contain an aperiodicity test for certain(w). The aperiodicity of certain(w) can be checked using AMoRe (encode the DFA using AMoRe and test for a star-free expression for it). You can automatize this process by putting some code that emulates key strikes to encode the DFA.

(B) - The code in plot.py and experiments.py STRONGLY relies on assumption we did for OUR experiments with OUR raw results and for OUR purposes. If you want to plot something or to generate results, we suggest you to write your own code instead of using plot.py or experiments.py which are both very specific to our needs.
