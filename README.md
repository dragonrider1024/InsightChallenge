# Solution to the problem
1. The running median algorithm was implemented using two heaps, with a minimum heap storing elements >= median
and the maximum heap storing elements < median. The size of the minimum heap was maintained to be equal to the size
of the maximum heap or the size of the maximum heap plus one.

2. Two dictionaries were created to store the heaps using combinations of recipient and zip code or recipient and date
as keys

(see function calculateMedianAndTotal(self, rowItem, byKey))

3. The input files were read into memory line by line. Every time a new line came in, it is parsed and the validity of
of the input was checked. The format of zip and date were also checked to decide whether to skip that entry or not.

(see function worker(self) and function readInput(self, fileInput))

4. Each time a valid new entry came in, the calculated running median and corresponding key were save in a txt file for
median by zip. For median by date, only the final median and corresponding keys were saved. The running medians are not
saved into txt.

(see function saveOutputByDate(self, fileOutput) and function saveOutput(self, key, medianAndTotal, fileOutput))

