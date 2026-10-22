## AI acknowledgment

This demo was created with Claude Code (Anthropic, model
Claude Opus 5.5).

# Simple ChromaDB Demo: Food Search

A tiny command-line demo of a vector database. It stores 10 short food
descriptions in [ChromaDB](https://docs.trychroma.com/), then lets you type a
query and shows the 3 foods closest in *meaning*, along with their distances.

The whole demo is one short file, [food_search.py](food_search.py). Read the
comments. They explain what each step does.

## Install and run

You need Python 3.9 or newer. This demo was tested with Python 3.14 and
chromadb 1.5.9.

```
python -m pip install -r requirements.txt
python food_search.py
```

Depending on your system, you may need `python3` (macOS/Linux) or `py`
(Windows) instead of `python`.

The first run downloads Chroma's default embedding model (all-MiniLM-L6-v2,
about 80 MB), so it takes a little longer. The database is saved in a
`chroma_store/` folder next to where you ran the program. Delete that folder
to start over from scratch.

## Example session

```
The 'foods' collection holds 10 items.

What are you in the mood for? (press Enter to quit): food from Tokyo
  distance 1.003:  Sushi: Japanese rice rolls with raw fish and seaweed
  distance 1.272:  Apple pie: a baked pastry filled with sweet cinnamon apples
  distance 1.300:  Hamburger: a grilled beef patty on a bun, classic American fast food

What are you in the mood for? (press Enter to quit): a quick meal from a drive-through
  distance 1.040:  Hamburger: a grilled beef patty on a bun, classic American fast food
  distance 1.315:  Pizza: Italian flatbread baked with tomato sauce and melted cheese
  distance 1.325:  Caesar salad: crisp lettuce with croutons, parmesan, and a tangy dressing
```

Neither query shares an important word with the food it found. "Tokyo" never
appears in the sushi description, and "drive-through" never appears in the
hamburger description. The embedding model matched them by meaning.

## Things to try

- `I have the flu`, `street food from Mexico City`, `something sweet`
- `I want something hot and spicy`. Look at the top result and its distance.
  Why might the model have made that mistake?
- A query that has nothing to do with food. Notice that you still get 3
  results. How could a program tell "no good match"?
- Edit or add foods in the `FOODS` list and run it again. (If you *remove* a
  food, it stays in the database, because `upsert` adds and replaces items but
  never deletes them. Delete the `chroma_store/` folder to clear it out.)

## What this demo does *not* do

This is only a starting point. HW6 asks for much more, including:

- a real corpus of hundreds of items (not a hard-coded list)
- letting the user add new items while the program runs
- doing something useful with the results, not just printing them
