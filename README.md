For those of you not in the know, ChefSteps is a website the has delicious recipes and beautiful videos of people making them. It makes it really easy to get enthusiastic about something, and totally clear about the technique used.

I've been a huge fan ever since I made the [chocolate soufle](https://www.chefsteps.com/activities/molten-chocolate-souffle) about 2 years ago[^1].

They use a lot more specialist equipment than your average cook book, but there are lots of recipes that use each bit of kit. I'm wondering: 

* What new recipes each new bit of kit unlocks?
* What order of acquisition would unlock the most recipes?
* Are there a lot of recipes that require pieces of equipment that no other recipe uses?

The quick summary is that there are 300ish bits of unique kit, but you seem to be able to get by very nicely on 50 or so.

I did a little scrape to get the equipment from each recipe. The [python to do that is here](https://github.com/notionparallax/ChefstepsEquipment) and the results are below:
<figure>
<iframe src="https://docs.google.com/spreadsheets/d/1tf2GLSQexYe3346Gj7arfgbUxX9-3apWmRWRvjPzkYg/pubhtml?gid=1735103416&amp;single=true&amp;widget=true&amp;headers=false"></iframe>
<figcaption>
You can get the data from the repo, or [a slightly tidied version from here](https://docs.google.com/spreadsheets/d/1tf2GLSQexYe3346Gj7arfgbUxX9-3apWmRWRvjPzkYg/pub?output=xlsx). This table shows the recipes ordered by number of bits of kit needed to make them. For an easy life, start at the bottom!

There are some problems. There are lots of things that are optional; you could make the recipes without them. The biggest problem is in the raw data. In some recipes it calls for a _pan_ lots of recipes need a pan, but it only shows up in the requirements a few times (and in a few different guises). It's not a big issue, most equipment that gets left out is common in most kitchens, but it needs a bit of extra gardening to reach full pedantry.
</figcaption>
</figure>

With a preliminary look, I can do an easy count of what's used the most. It's all about the: Sous vide setup, Blender, Digital scale, Fine-mesh sieve, Whisk, Whipping siphon and Ziplock-style bag (1 gallon)

<figure>
<iframe src="https://docs.google.com/spreadsheets/d/1tf2GLSQexYe3346Gj7arfgbUxX9-3apWmRWRvjPzkYg/pubchart?oid=1921581789&amp;format=interactive"></iframe>
<figcaption>
This is a pretty clear indication that a blender and a sous vide setup are going to make a big difference!
</figcaption>
</figure>

Re-sorted with optionals included:

<figure>
<iframe src="https://docs.google.com/spreadsheets/d/1tf2GLSQexYe3346Gj7arfgbUxX9-3apWmRWRvjPzkYg/pubhtml?gid=602899321&amp;single=true&amp;widget=true&amp;headers=false"></iframe>
<figcaption>
In a naive way, if you got things from this list, starting at the top, you'd probably be OK! No guarantees though.

If you folded things that were the same into each other then things like _Fine-mesh sieve_ getting another few hits. 
</figcaption>
</figure>

What I haven't worked out yet is how to figure out the productive combinations. There's still a lot of data tidying to do before any of this is _conclusive_(it's really late here).

I'll revisit this once I work out how to do the next step.

[^1]: Maybe it was even more than 2 years ago.
