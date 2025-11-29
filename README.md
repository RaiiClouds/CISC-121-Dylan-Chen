# Algorithm Name:Insertion sort

Why is chose it: I decided to use this sorting algorithm because I wanted to recall and practice how different sorting algorithms are implemented. At the time, I had completely forgotten how to implement insertion sort, so I chose it as a way to refresh my understanding of how the algorithm works.


## Demo video/gif/screenshot of test
https://drive.google.com/file/d/1JGKhVdHCFBnQanviYKRwezbZkbgwzLLD/view?usp=sharing


## Problem Breakdown & Computational Thinking

Decomposition:
- Set current position to the second element (index 1)
- Pick the current element as the "key" to be inserted
- Store its value for comparison
- Comparison and Shifting Loop
- Place the key in its correct sorted position
- Move to the next unsorted element
- Repeat until all elements are processed

Pattern Recognition
- Repeatedly compares the current key with elements to its left
- Moves from right to left through the sorted portion
- Stops when it finds an element smaller than key or reaches the beginning
- Elements are shifted right to make space for the key

Abstraction: 

Details SHOWN to the user:

- Current Array State (Visualized with bars)
- Color coding: red for current element being processed, blue for others
- error handeling
- All possible steps:
"Looking at element X at position Y"
"Shifted element Z right"
"Inserted element X at position Y"
"Array fully sorted!"
Step Progress (Numerical tracking)

Details DISCARDED (not shown):

- No showing of loop counters (i, j variables)
- No display of temporary variable storage
- Low-level Operations


Algorithm Design: 

Input Flow: User Input → GUI Interface → Data Validation → Algorithm Initialization

User provides input through:
- Text box: "5, 2, 8, 1, 9"
- Generate button: creates random array
- Input change events: triggers reset

Input Processing:String parsing and validation

- Conversion to integer list
- Error handling for invalid formats like charcters.ex

Processing Flow: Initialized Array → Step Generation → State Tracking → Visualization Creation

Algorithm Execution:
- Generate all sorting steps upfront
- Store each step with (array_state, description, current_index)

Output Flow:Processed Data → Visualization → GUI Update → User Feedback

- Matplotlib bar chart with color coding
- Step description text

User Feedback:
- Real-time status updates
- Error messages with guidance


## Steps to Run
- Enter numbers separated by commas in the input box, or
- Click “Generate Random Array” to create a random list
- Click “Next Step” to advance through the algorithm
- Click “Previous Step” to go back and review prior steps
## Hugging Face Link
https://huggingface.co/spaces/Dylan10101/CISC121_PROJECT


## Author & Acknowledgment
