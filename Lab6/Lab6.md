# Todd Louison Lab 6
## Scientific Computation

#### Five Letter Pair Results

```
Shortest path between chaos and order is
chaos
choos
shoos
shoes
shoed
shred
sired
sided
aided
added
adder
odder
order
Shortest path between nodes and graph is
nodes
lodes
lores
lords
loads
goads
grads
grade
grape
graph
Shortest path between moron and smart is
moron
boron
baron
caron
capon
capos
capes
canes
banes
bands
bends
beads
bears
sears
stars
start
smart
Shortest path between pound and marks is
None
```

#### Four Letter Solution Code

```
def words_graph(filename, size):
    fh = gzip.open(filename, 'r')
    words = set()
    for line in fh.readlines():
        line = line.decode()
        if line.startswith('*'):
            continue
        w = str(line[0:size])
        words.add(w)
    return generate_graph(words)
```

I changed the 3rd to last line from `w = str(line[0:5])` to `w = str(line[0:size])` , where size is a command line argument that tells you how long the words will be. Filename is another command line argument that provides the name of the file to create the graph with, instead of having the name hardcoded. All other changes were to facilitate those two changes (e.g. adding arguments to the function and getting command line arguments from `sys.argv`.

#### Four Letter Solution

```
Shortest path between cold and warm is
cold
wold
word
ward
warm
Shortest path between love and hate is
love
hove
have
hate
```

#### Code Variation Code

This variation is all words that are 1 letter different from the original, regardless of location within the word.

``` 
def edit_distance_one(word):
        permutations = ["".join(att) for att in itertools.permutations(word, len(word))]
        for attempt in permutations:
            for i in range(len(attempt)):
                left, c, right = attempt[0:i], attempt[i], attempt[i + 1:]
                j = lookup[c]  # lowercase.index(c)
                for cc in lowercase[j + 1:]:
                    yield left + cc + right
```

This generates all permutations of the word with a single letter changed, and then checks all those possibilities.

#### Code Variation Results

```
Shortest path between chaos and order is
chaos
chose
chore
coder
order
Shortest path between nodes and graph is
nodes
anode
agone
anger
gaper
graph
Shortest path between moron and smart is
moron
manor
roams
smart
Shortest path between pound and marks is
pound
mound
monad
moans
roams
marks
```

