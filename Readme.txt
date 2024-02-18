Coding assignment: Iterative-deepening-search
Author: Duc Tran
The program helps user solved 16-puzzle by using iterative-deepening-search. The program is written in Python.
To run the code, use latest version of Visual Studio Code, install Python 3.11.8 and install necessary library like time, psutil
System: Window 11
Python version: 3.11.8

Compare to Breadth-First-Search
			IDS-Expanded Node	BFS-Expanded Node	Memory IDS		Memory BFS  
Formation Move			
D			2			4			840				840
UUURRRDDD		100			1759			9032				148808
RRURDD			230			138			9032				10616
DRDRD			33			107			2888				10088
LDLDRR			162			174			9032				10616
RDLDDRR			353			359			33608				36776
DLLDRRDR		547			850			33608				41528
URDRURD			95			368			9032				37304
RULLDRDRD		2054			1999			131912				150392
LUUURDRDD		1635			1509			131912				146168

Result explain: The node expansion of IDS seems wasteful at first because we are generate and repeating node expansion many times. But for many states space, most of the nodes
are in bottom level, so it does not matter much that the upper levels are repeated. The memory of IDS is always smaller than the memory of BFS (O(bd) compared to O(b^d)).
If we dont get memory of explored set, the memory of IDS in the above tables can be further reduced