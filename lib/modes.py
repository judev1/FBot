import random
import spacy

nlp = spacy.load("en_core_web_sm")

def punctuate(text):

    for word in text:
        continue
        # gonna do some stuffs

def sanitise_text(text):
    
    text = text.lower()
    text = text.replace("*", "")
    text = text.replace("~", "")
    text = text.replace("`", "")
    text = text.replace("_", "")
    text = text.replace("|", "")
    
    return text

def santitise_word(word):

    start = ""
    for char in word:
        if not char.isalpha():
            start += char
            word = word[1:]
            continue
        break
    
    end = ""
    for char in word[::-1]:
        if not char.isalpha():
            end = char + end
            word = word[:-1]
            continue
        break

    return word, start, end

def uwu(text):

    text = sanitise_text(text)

    uwus = ["owo", "uwu", ">w<", "XD"]
    
    text = text.replace("er", "uw")
    text = text.replace("r", "w")
    text = text.replace("l", "w")
    
    text = text.replace("ith", "iv")
    text = text.replace("f", "v")
    text = text.replace("ove", "uv")
    text = text.replace("th", "d")
    text = text.replace("is", "iws")
    
    text = text.replace("na", "nya")
    text = text.replace("ne", "nye")
    text = text.replace("ni", "nyi")
    text = text.replace("no", "nyo")
    text = text.replace("nu", "nyu")

    return text + "~ " + random.choice(uwus)

def confused(text):

    text = sanitise_text(text)
    if text.endswith("?"):
        text += "??"
    else:
        text += "?"

    return text

def pirate(text):

    text = sanitise_text(text)
    text = text.replace("you", "ye")
    text = text.replace("ing", "in'")
    text = text.replace("and", "an'")

    temp = []
    for word in text.split():
        word, start, end = santitise_word(word)
        if word.startswith("h"):
            word = "'" + word[1:]
        elif word.startswith("th"):
            word = "'" + word[2:]
        elif word == "my":
            word = "me"
        elif word == "is":
            word = "be"
        temp.append(start + word + end)
    text = " ".join(temp)

    return text + " arr"


def triggered(text):

    text = sanitise_text(text)
    text = text.upper()

    return "**__" + text + "__**"

def italian(text):

    text = sanitise_text(text)

    temp = []
    for word in text.split():
        word, start, end = santitise_word(word)
        if not word.endswith("a"):
            word += "a"
        temp.append(start + word + end)
    text = " ".join(temp)

    return "*" + text + "*"

def fuck(text):

    text = sanitise_text(text)

    temp = []
    for word in text.split():
        word, start, end = santitise_word(word)
        if nlp(word)[0].pos_ in ["NOUN", "ADJ", "VERB"]:
            word = "fucking " + word
        temp.append(start + word + end)
    text = " ".join(temp)

    return text

def ironic(text):

    text = sanitise_text(text)

    temp = text
    text = ""
    for char in temp:
        text += random.choice([char.lower(), char.upper()])
    
    return text

def patronise(text):

    text = sanitise_text(text)
    text = " ".join(list(text))
    
    return text

def colonial(text):

    text = sanitise_text(text)

    temp = []
    for word in text.split():
        word, start, end = santitise_word(word)
        if word.startswith("h"):
            word = "'" + word[1:]
        elif word.startswith("th"):
            word = "'" + word[2:]
        temp.append(start + word + end)
    text = " ".join(temp)

    text = text.replace("t", "'")
    text = text.replace("ing", "in'")

    return text + " init fam"

def safe(text):

    words = {
        "fucking": "frickity lick sticks",
        "fucker": "fricker licker",
        "fuck": "frick",
        "dickhead": "poopoohed",
        "dick": "poopoo",
        "cock": "glock",
        "twat": "meanie",
        "prick": "cactus spike",
        "cock": "glock",
        "pussy": "kitty cat",
        "cunt": "cat",
        "shit": "shirt",
        "arse": "apple",
        "ass": "apple",
        "bloody": "blorpy",
        "bitch": "birch tree",
        "bastard": "brass tree",
        "wanker": "winker",
    }

    text = sanitise_text(text)

    for word in words:
        text = text.replace(word, words[word])

    return text

def biblical(text):

    text = sanitise_text(text)

    temp = []
    for word in text.split():

        word, start, end = santitise_word(word)
        
        if word == "are":
            word = "art"
        elif word == "am":
            word = "be"
        elif word.endswith(("d", "t", "k", "y", "m", "o")):
            word += "eth"
        elif word.endswith("e"):
            if word not in ["the", "be"]:
                word += "ith"
        elif word.endswith(("ave", "ome")):
            word += "th"
        elif word.endswith("as"):
            word += "t"
        elif word == "had":
            word = "hath"
        elif word in ["its", "it's"]:
            word = "it tis"
        elif word == "is":
            word = "tis"
        elif word == "you":
            word = "thou"
        elif word == "my":
            word = "mine"
        elif word == "the":
            word = random.choice(["thy", "thine"])
        temp.append(start + word + end)
    text = " ".join(temp)

    text = text.replace("ere", "'re")

    return text