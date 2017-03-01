# Astral Loom
#### General idea
The goal of this library is to provide an easy, flexible and extensible way to alchemically add and blend together any kind of magical energy. It does so by storing instead of a direct energy only a generalized *link* to this energy, which can be moved around, stored and sent just like any other programming object. The link framework also provides built-in methods to join together two links, creating a composite energy link that can be further processed.

AstralLoom also has a system that converts any image given, whether it be of a face or of a sigil, to the internal link representation; sigil libraries and collections (eg. runes) can be used and mixed as well.

This allows large recipies to generate layered spells who can then be exported as a simple link or magical drawing [coming soon(tm)]. These recipies are reuseable for different targets, composable, shareable, etc.

#### How to use
Most of the library only requires python 3 ([Windows download](https://www.python.org/downloads/windows/), everything else generally has it installed by default under `python3`).

To use links, just import the Link class from link.py and instantiate it for whatever you need
```python
from link import Link
name = Link("Akem")
print(name)# Gives "Link[*Akem*]"
```
You can merge links simply by adding them together. Adding them will always push **the smaller link onto the larger link**. If you want to specify which link goes on top of which, use .mixwith().
```python
from link import Link
name = Link("Akem")
fertility = Link("nyljUzBnoZWmSwajLcALniDGfosDtiFKP")
print(name+fertility)# Gives "Link[*mwwfNrKplRDqVenfUgNXmiCOsktDoiUYE*]"
print(name.mixwith(fertility))# Gives Link[*Zgvq*]
```
The library folder contains factory files which already have a certain repository of energies. This will of course be updated as time goes on.
```python
from link import Link
import library.symboltable
name = Link("Akem")
table = library.symboltable.build()
percep = table["perception"] # See [the source file](https://github.com/Nydrath/AstralLoom/blob/master/library/symboltable.py) or use a for loop to see what is available
print(name+percep)# Gives "Link[*dalailPHYeJKTcDcRhmqdBNVciPzK*]"
print(name.mixwith(percep))# Gives Link[*Zulp*]
```

Using the ImageLink class to convert images requires [pyimgur](https://github.com/Damgaard/PyImgur) as well as a registered imgur bot account. Ask me nicely and I'll give you mine, but I can't put it on github for obvious reasons. If you have your own such account, make a file `client_data.json` with `"imgurid": <your id>` in the same folder as AstralLoom.
Once this is set up, you can create links from images simply by creating an ImageLink instance with as argument the path to the image file.
```python
from imagelink import ImageLink
im = ImageLink("pictures/bird.png")
print(im)# Gives Link[*..something depending on your image..*]
```
This naturally supports addition like normal links.

If you know how to use them, there is also a table of Ziruph helper class in `ziruph.py`.
Ziruph tables are initialized with a list of powers they should align themselves to, and you access elements using `[input word, (powers to sequentially pipe the input through)]`
Examples:
```python
from ziruph import Ziruphtable
from link import Link
# The .split() is to make a list containing each individual word. Try and print it.
planets = Ziruphtable("Sun Moon Mercury Venus Earth Mars Jupiter Saturn".split())
akem_in_mercury = planets["Akem", "Mercury"]
# Lets say we wanted to give Akem energy for an upcoming race, so we say Mars energy to fuel it,
# Mercury to make him faster and the Sun to stabilize and unify the other two
akem_race = planets["Akem", ("Mars", "Mercury", "Sun")]
# Ziruph tables return a string, but if we wanted to make a link out of it all we'd need to do is wrap it in a new instance
spell_link = Link(akem_race)
# Printing a ziruph table outputs the entire table in a human-readable form
print(planets)
```

There exists also a script `squares.py` that creates and renders magical squares, but I have yet to figure out a way to combine that with the text links. You're free to use it for generating squares but it lacks integration so far.
