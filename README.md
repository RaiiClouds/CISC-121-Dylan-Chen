# Algorithm Name:Insertion sort


## Demo video/gif/screenshot of test
https://drive.google.com/file/d/1JGKhVdHCFBnQanviYKRwezbZkbgwzLLD/view?usp=sharing


## Problem Breakdown & Computational Thinking (You can add a flowchart and write the

Decomposition: What smaller steps form your chosen algorithm?

The insertion sort algorithm is decomposed into these steps:

Initialization Step

Start with an array fo numbers
Set current position to the second element (index 1)

Element Selection Step

- Pick the current element as the "key" to be inserted
- Store its value for comparison
- Comparison and Shifting Loop

Compare the key with each element in the sorted portion (to its left)
If an element is larger than the key, shift it one position to the right
Continue moving left until finding the correct insertion position or reaching the beginning
Insertion Step

Place the key in its correct sorted position
The sorted portion grows by one element
Increment Step

Move to the next unsorted element
Repeat until all elements are processed
Completion Step

Entire array is sorted
Algorithm terminates
Pattern Recognition: How does it repeatedly reach, compare, or swap values?

The algorithm exhibits several repeating patterns:

Comparison Pattern:

python
while j >= 0 and arr[j] > key:
Repeatedly compares the current key with elements to its left
Moves from right to left through the sorted portion
Stops when it finds an element smaller than key or reaches the beginning
Shifting Pattern:

python
arr[j + 1] = arr[j]
j -= 1
Elements are shifted right to make space for the key
This creates a "hole" that moves leftward through the array
No actual swapping occurs - just sequential shifting
Insertion Pattern:

python
arr[j + 1] = key
The key is placed in the final vacated position
This happens exactly once per outer loop iteration
Iteration Pattern:

Outer loop: for i in range(1, len(arr)) - processes each unsorted element
Inner loop: while j >= 0 and arr[j] > key - finds insertion position for current element
The pattern repeats n-1 times (for n elements)
Abstraction: Which details of the process should be shown to the user and how to show it, and which details should be discarded?

Details SHOWN to the user:

Current Array State (Visualized with bars)

Complete array at each step
Color coding: red for current element being processed, blue for others
Current Operation (Text description)

"Looking at element X at position Y"
"Shifted element Z right"
"Inserted element X at position Y"
"Array fully sorted!"
Step Progress (Numerical tracking)

Current step number / total steps
JSON data with array state
Algorithm Progress (Visual highlighting)

Red bar indicates active element being placed
Implicitly shows growing sorted portion on the left
Details DISCARDED (not shown):

Technical Implementation Details

No showing of loop counters (i, j variables)
No display of temporary variable storage
No memory allocation details
Low-level Operations

Actual memory movements
Variable assignments
Index calculations
Performance Metrics (in main visualization)

Time complexity calculations
Space usage statistics
Comparison counts (though these could be added)
Error Handling Internals

Input validation processes
Exception handling mechanisms
How we show the important details:

Visual: Bar chart with color coding for immediate pattern recognition
Textual: Step descriptions for conceptual understanding
Numerical: Step counters for progress tracking
Structural: Array state preservation for verification
Algorithm Design: How will input → processing → output flow to and from the user?

Input Flow:

text
User Input → GUI Interface → Data Validation → Algorithm Initialization
User provides input through:

Text box: "5, 2, 8, 1, 9"
Generate button: creates random array
Input change events: triggers reset
Input Processing:

String parsing and validation
Conversion to integer list
Error handling for invalid formats
Processing Flow:

text
Initialized Array → Step Generation → State Tracking → Visualization Creation
Algorithm Execution:

Generate all sorting steps upfront
Store each step with (array_state, description, current_index)
Maintain current step pointer
User Interaction Processing:

"Next Step": increments pointer, returns visualization
"Previous Step": decrements pointer, returns visualization
State preservation between interactions
Output Flow:

text
Processed Data → Visualization → GUI Update → User Feedback
Visual Output:

Matplotlib bar chart with color coding
Step description text
Progress information in JSON format
User Feedback:

Real-time status updates
Error messages with guidance
Success confirmation
GUI Integration Flow:

text
[User Input Area] → [Control Buttons] → [Visualization Display] → [Status Feedback]
     ↓                    ↓                    ↓                     ↓
Text Input        Generate/Step Buttons   Matplotlib Plot      Text + JSON Info
The interface creates an interactive learning loop where users can:

Provide input or generate data
Step through the algorithm at their own pace
See visual and textual explanations
Go backwards to review steps
Modify input and restart the process

## Steps to Run
## Hugging Face Link
https://huggingface.co/spaces/Dylan10101/CISC121_PROJECT


## Author & Acknowledgment
