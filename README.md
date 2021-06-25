```
   _____ _______   ____________        ___    ____
  / ___// ____/ | / / ____/ __ \      /   |  /  _/
  \__ \/ __/ /  |/ / /   / / / /_____/ /| |  / /  
 ___/ / /___/ /|  / /___/ /_/ /_____/ ___ |_/ /   
/____/_____/_/ |_/\____/\____/     /_/  |_/___/  
```

SENCO-AI is a BCI speller I'm currently developing as my B.Sc. thesis project. It allows users to spell sentences with their brain, via near-infrared spectroscopy (fNIRS). SENCO-AI will hopefully one day enable patients who are unable to move & speak (e.g., because of a stroke, brainstem injury, ALS or similar) to communicate faster than they can with other currently available fNIRS BCI spellers.

The procedure for selecting words is based on a binary search algorithm, which was first implemented for use as a BCI word selector by Snipes et al. (2017) and later adapted to fNIRS by Cleutjens (2018).
- We have a long, alphabetically sorted list of words (the dictionary)
- The user sees the middle word of the dictionary
- The user decides if the word they want to select (the target) comes BEFORE or AFTER the middle word alphabetically
- The program cycles through BEFORE and AFTER on a fixed timer
- To enter their decision, the user performs a mental motor imagery task (like imagining to play tennis) while the command element they want to select is highlighted
- If the user decides on BEFORE, the dictionary is chopped in half and the first half of it is kept. If they decide on AFTER, the latter half is kept
- This procedure repeats until there's only one more word remaining in the dictionary
- If there were no errors, the remaining word will be the target.

With this procedure, any given word in the dictionary can be selected in a given number of steps. By chaining word selections together, the user can encode sentences.

SENCO-AI has a number of features designed to make it easier and faster to use for patients:
- Audio feedback and text-to-speech through pyttsx3 allow SENCO-AI to be used by patients who have difficulty controlling their eyes, or who are blind
- Word predictions powered by GPT-3 are available, making the encoding process significantly faster.
- The dictionary can be custom-tailored to the user (smaller dictionaries mean the encoding process will be faster, larger dictionaries give the user more vocabulary)
- The AI can suggest words that aren't part of the dictionary, meaning the actual vocabulary is much, much larger than the dictionary
