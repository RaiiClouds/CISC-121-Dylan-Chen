# app.py (fixed)
import asyncio
# Set event loop policy early (important to do this before importing frameworks that create loops)
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

# Use headless backend before importing pyplot (we avoid pyplot but still set backend defensively)
import matplotlib
matplotlib.use("Agg")

from matplotlib.figure import Figure
import numpy as np
import gradio as gr
from typing import List, Tuple, Dict

class InsertionSortVisualizer:
    """
    A class to demonstrate insertion sort algorithm with step-by-step visualization.
    """

    def __init__(self):
        self.steps: List[Tuple[List[int], str, int]] = []
        self.current_step: int = 0

    def insertion_sort(self, arr: List[int]) -> List[Tuple[List[int], str, int]]:
        steps = []
        arr = arr.copy()
        steps.append((arr.copy(), "Initial array", -1))

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            steps.append((arr.copy(), f"Looking at element {key} at position {i}", i))

            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                steps.append((arr.copy(), f"Shifted {arr[j+2]} right", j + 1))

            arr[j + 1] = key
            steps.append((arr.copy(), f"Inserted {key} at position {j+1}", j + 1))

        steps.append((arr.copy(), "Array fully sorted!", -1))
        return steps

    def generate_sample_data(self, size: int = 10) -> List[int]:
        return list(np.random.randint(1, 100, size))

    def create_visualization(self, arr: List[int], description: str, current_index: int) -> Figure:
        """
        Build a Matplotlib Figure object directly (avoids pyplot global state).
        """
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()

        colors = ['lightblue'] * len(arr)
        if 0 <= current_index < len(arr):
            colors[current_index] = 'red'

        bars = ax.bar(range(len(arr)), arr, color=colors, edgecolor='black')

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}', ha='center', va='bottom')

        ax.set_xlabel('Array Index')
        ax.set_ylabel('Value')
        ax.set_title(f'Insertion Sort Visualization\n{description}')
        ax.set_xticks(range(len(arr)))
        fig.tight_layout()
        return fig

    def create_error_visualization(self, message: str) -> Figure:
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()
        ax.text(0.5, 0.5, message, ha='center', va='center',
                transform=ax.transAxes, fontsize=12, color='red', wrap=True)
        ax.set_title("Initialization / Error")
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        return fig

    def sort_with_visualization(self, input_array: str) -> Tuple[Figure, str, Dict]:
        try:
            if input_array.strip():
                arr = [int(x.strip()) for x in input_array.split(',')]
            else:
                arr = self.generate_sample_data(8)

            # Initialize steps if necessary
            if (not self.steps) or (self.current_step >= len(self.steps)) or (len(self.steps) == 0):
                self.steps = self.insertion_sort(arr)
                self.current_step = 0

            if not self.steps:
                fig = self.create_error_visualization(
                    "Please initialize the array first!\n\nClick 'Generate Random Array' or enter numbers above, then click 'Next Step'."
                )
                return fig, "Array not initialized. Please generate or enter an array first.", {"current_step": 0, "total_steps": 0, "array": []}

            # Auto-advance to next step
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1

            current_arr, description, current_index = self.steps[self.current_step]
            fig = self.create_visualization(current_arr, description, current_index)
            step_info = {
                "current_step": self.current_step + 1,
                "total_steps": len(self.steps),
                "array": current_arr
            }
            status = f"Step {self.current_step + 1}/{len(self.steps)}: {description}"
            return fig, status, step_info

        except Exception as e:
            fig = self.create_error_visualization(f"Error: {str(e)}\n\nPlease check your input format and try again.")
            return fig, f"Error: {str(e)}", {"current_step": 0, "total_steps": 0, "array": []}

    def reset(self):
        self.steps = []
        self.current_step = 0

    def has_initialized_steps(self) -> bool:
        return len(self.steps) > 0

# Global instance
visualizer = InsertionSortVisualizer()


def next_step(input_array):
    return visualizer.sort_with_visualization(input_array)

def previous_step(input_array):
    try:
        if not visualizer.has_initialized_steps():
            fig = visualizer.create_error_visualization(
                "Please initialize the array first!\n\nClick 'Generate Random Array' or enter numbers above, then click 'Next Step'."
            )
            return fig, "Array not initialized. Please generate or enter an array first.", {"current_step": 0, "total_steps": 0, "array": []}

        if visualizer.current_step > 0:
            visualizer.current_step -= 1

        if 0 <= visualizer.current_step < len(visualizer.steps):
            current_arr, description, current_index = visualizer.steps[visualizer.current_step]
            fig = visualizer.create_visualization(current_arr, description, current_index)
            step_info = {
                "current_step": visualizer.current_step + 1,
                "total_steps": len(visualizer.steps),
                "array": current_arr
            }
            status = f"Step {visualizer.current_step + 1}/{len(visualizer.steps)}: {description}"
            return fig, status, step_info
        else:
            fig = visualizer.create_error_visualization("Invalid step index. Please reset and try again.")
            return fig, "Error: Invalid step index", {"current_step": 0, "total_steps": 0, "array": []}

    except IndexError:
        fig = visualizer.create_error_visualization(
            "Please initialize the array first!\n\nClick 'Generate Random Array' or enter numbers above, then click 'Next Step'."
        )
        return fig, "Array not initialized. Please generate or enter an array first.", {"current_step": 0, "total_steps": 0, "array": []}
    except Exception as e:
        fig = visualizer.create_error_visualization(f"Error: {str(e)}\n\nPlease try generating a new array.")
        return fig, f"Error: {str(e)}", {"current_step": 0, "total_steps": 0, "array": []}

def generate_random_array():
    visualizer.reset()
    sample_data = visualizer.generate_sample_data(8)
    sample_str = ', '.join(map(str, sample_data))
    fig = visualizer.create_error_visualization("Array generated! Click 'Next Step' to start the insertion sort visualization.")
    return sample_str, fig, "Array generated! Click 'Next Step' to start.", {"current_step": 0, "total_steps": 0, "array": []}

def input_changed(input_array):
    visualizer.reset()
    if input_array.strip():
        fig = visualizer.create_error_visualization("Input changed! Click 'Next Step' to start sorting with the new array.")
        status = "Input changed! Click 'Next Step' to start sorting."
    else:
        fig = visualizer.create_error_visualization("Please enter numbers separated by commas or click 'Generate Random Array'.")
        status = "Please enter an array or generate a random one."
    return fig, status, {"current_step": 0, "total_steps": 0, "array": []}

def create_gradio_interface():
    try:
        demo = gr.Blocks(theme=gr.themes.Soft(), title="Insertion Sort Visualizer")
    except TypeError:
        demo = gr.Blocks(title="Insertion Sort Visualizer")

    with demo:
        gr.Markdown("""
# 🔍 Insertion Sort Algorithm Visualizer
This interactive demo demonstrates how the **Insertion Sort** algorithm works by building a sorted array one element at a time.
---
## 📝 How to Use
- Enter numbers separated by commas in the input box, **or**
- Click **“Generate Random Array”** to create a random list  
- Click **“Next Step”** to advance through the algorithm  
- Click **“Previous Step”** to go back and review prior steps  
---
## 🔧 How Insertion Sort Works
1. Start at the second element (index 1)  
2. Compare it with elements to its left (the sorted portion)  
3. Shift larger elements one position to the right  
4. Insert the current element into its correct place  
5. Repeat for all elements  
---
## 📊 Complexity
- **Time Complexity:**  
  - Worst case: **O(n²)**  
  - Best case (already sorted): **O(n)**  
- **Space Complexity:**  
  - **O(1)** (in-place algorithm)
---
        """)

        with gr.Row():
            with gr.Column(scale=1):
                input_array = gr.Textbox(
                    label="Input Array (comma-separated numbers)",
                    placeholder="e.g., 5, 2, 8, 1, 9, 3",
                    value="",
                    info="Enter numbers separated by commas or generate a random array"
                )
                generate_btn = gr.Button("🎲 Generate Random Array", variant="secondary")
                with gr.Row():
                    prev_btn = gr.Button("⏮️ Previous Step", variant="secondary")
                    next_btn = gr.Button("⏭️ Next Step", variant="primary")
                status = gr.Textbox(
                    label="Status",
                    value="Please generate or enter an array to begin!",
                    info="Follow the instructions above to start the visualization"
                )
                step_info = gr.JSON(
                    label="Step Information",
                    value={"current_step": 0, "total_steps": 0, "array": []}
                )
            with gr.Column(scale=2):
                plot = gr.Plot(
                    label="Insertion Sort Visualization",
                    value=visualizer.create_error_visualization("Welcome! Please generate or enter an array to begin the insertion sort visualization.")
                )

        generate_btn.click(generate_random_array, outputs=[input_array, plot, status, step_info])
        next_btn.click(next_step, inputs=[input_array], outputs=[plot, status, step_info])
        prev_btn.click(previous_step, inputs=[input_array], outputs=[plot, status, step_info])
        input_array.change(input_changed, inputs=[input_array], outputs=[plot, status, step_info])

    return demo

def main():
    # Optional tests (will run locally when __main__); safe to keep but not required for Spaces

    print("\n🚀 Starting Gradio Interface...")
    demo = create_gradio_interface()
    demo.launch(share=False)

if __name__ == "__main__":
    main()
