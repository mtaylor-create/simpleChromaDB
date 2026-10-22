# food_search.py
# A tiny demo of a vector database using ChromaDB (tested with chromadb 1.5.9).
# It stores 10 food descriptions, then lets you search them by *meaning*.
#
# AI acknowledgment: This demo was created with the assistance of Claude Code
# (Anthropic, model Claude Opus 5.5) in October 2026.

import chromadb  # The ChromaDB library (install with: pip install chromadb)

# Our tiny hard-coded "dataset". Each string becomes one item in the database.
# (Chroma calls each piece of searchable text a "document".)
FOODS = [
    "Sushi: Japanese rice rolls with raw fish and seaweed",
    "Pizza: Italian flatbread baked with tomato sauce and melted cheese",
    "Tacos: Mexican corn tortillas filled with seasoned meat and salsa",
    "Ice cream: a frozen, creamy dessert that is perfect on a hot day",
    "Caesar salad: crisp lettuce with croutons, parmesan, and a tangy dressing",
    "Chicken noodle soup: a warm, comforting broth often eaten when you have a cold",
    "Pancakes: fluffy griddle cakes with maple syrup, a breakfast favorite",
    "Curry: meat or vegetables simmered in a spicy Indian sauce",
    "Hamburger: a grilled beef patty on a bun, classic American fast food",
    "Apple pie: a baked pastry filled with sweet cinnamon apples",
]

# --- Step 1: Build the database ---------------------------------------------

# Create a client that saves the database to disk in a folder named
# "chroma_store", so the data is still there after the program exits.
# This path is relative to the folder you run the program *from*, so running it
# from a different folder creates a separate, brand-new database there.
client = chromadb.PersistentClient(path="chroma_store")

# A "collection" is like a table in a regular database. This opens the "foods"
# collection, creating it the first time the program runs. Because we don't
# choose an embedding model, Chroma uses its default (all-MiniLM-L6-v2), which
# runs on your computer. It is downloaded (about 80 MB) the first time it's used.
collection = client.get_or_create_collection(name="foods")

# Store the foods. Chroma automatically turns each document into an embedding
# (a list of numbers that represents its meaning) using the embedding model.
# "upsert" means "update or insert": running this program again replaces these
# items instead of adding duplicate copies of them.  Note that for your project
# you probably don't want to re-embed your whole dataset each time the user 
# runs the program, so the next few lines aren't *necessarily* what you should 
# do.

print("Embedding the foods and adding them to the database...")  # first run also downloads the model
collection.upsert(
    ids=[f"food{i}" for i in range(len(FOODS))],  # unique IDs: "food0", "food1", ...
    documents=FOODS,  # the text that gets embedded and searched
)
print(f"The 'foods' collection holds {collection.count()} items.")

# --- Step 2: Search the database ---------------------------------------------

while True:
    query = input("\nWhat are you in the mood for? (press Enter to quit): ")
    if query.strip() == "":  # an empty line ends the program
        break

    # Chroma embeds the query with the same model, then returns the 3 stored
    # items whose embeddings are closest to the query's embedding.
    # Note: it always returns 3 items, even if none of them are a good match.
    results = collection.query(query_texts=[query], n_results=3)

    # query() can search for several queries at once, so each field in the
    # results holds one list per query. We sent just one query, so we use [0].
    documents = results["documents"][0]  # the 3 closest foods, closest first
    distances = results["distances"][0]  # how far each one is from the query

    # A smaller distance means a closer meaning. The numbers are mostly useful
    # for comparing results with each other, not as an absolute score.
    for document, distance in zip(documents, distances):
        print(f"  distance {distance:.3f}:  {document}")
