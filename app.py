import asyncio
# Ensure a clean asyncio event loop before importing libraries that use async
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

# Use a headless backend for Matplotlib (important for servers / Gradio)
import matplotlib
matplotlib.use("Agg")

from matplotlib.figure import Figure
import numpy as np
import gradio as gr
from typing import List, Tuple, Dict


class InsertionSortVisualizer:
    """
    Handles:
    - Running insertion sort
    - Recording every step
    - Rendering visualizations
    """

    def __init__(self):
        # Stores all steps: (array snapshot, description, highlighted index)
        self.steps: List[Tuple[List[int], str, int]] = []
        # Tracks current step in UI
        self.current_step: int = 0


    def insertion_sort(self, arr: List[int]) -> List[Tuple[List[int], str, int]]:
        """
        Runs insertion sort manually and records each important change.
        """
        steps = []
        arr = arr.copy()

        # Step 0 — show initial state
        steps.append((arr.copy(), "Initial array", -1))

        # Start insertion sort from index 1
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            steps.append((arr.copy(), f"Looking at element {key} at position {i}", i))

            # Shift elements to the right while they are greater than key
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                steps.append((arr.copy(), f"Shifted {arr[j+2]} right", j + 1))

            # Insert the key
            arr[j + 1] = key
            steps.append((arr.copy(), f"Inserted {key} at position {j+1}", j + 1))

        # Final sorted array
        steps.append((arr.copy(), "Array fully sorted!", -1))
        return steps


    def generate_sample_data(self, size: int = 10) -> List[int]:
        """Generate a random array."""
        return list(np.random.randint(1, 100, size))


    def create_visualization(self, arr: List[int], description: str, current_index: int) -> Figure:
        """
        Creates a bar chart for the current sorting step.
        Highlights the currently active index in red.
        """
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()

        # Default bar colors
        colors = ['lightblue'] * len(arr)

        # Highlight the current element being processed
        if 0 <= current_index < len(arr):
            colors[current_index] = 'red'

        # Draw bars
        bars = ax.bar(range(len(arr)), arr, color=colors, edgecolor='black')

        # Write the number above each bar
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
        """
        Shows a simple message-only figure (for errors or instructions).
        """
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
        """
        Called when user clicks "Next Step".
        Advances through insertion sort one step at a time.
        """
        try:
            # Parse user input, or auto-generate if empty
            if input_array.strip():
                arr = [int(x.strip()) for x in input_array.split(',')]
            else:
                arr = self.generate_sample_data(8)

            # Reinitialize steps if needed or finished
            if (not self.steps) or (self.current_step >= len(self.steps)):
                self.steps = self.insertion_sort(arr)
                self.current_step = 0

            if not self.steps:
                fig = self.create_error_visualization(
                    "Please initialize the array first!"
                )
                return fig, "Array not initialized.", {"current_step": 0, "total_steps": 0, "array": []}

            # Move forward to the next step
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1

            # Retrieve current step data
            current_arr, description, current_index = self.steps[self.current_step]

            # Draw the graph for this step
            fig = self.create_visualization(current_arr, description, current_index)

            # Report step info
            step_info = {
                "current_step": self.current_step + 1,
                "total_steps": len(self.steps),
                "array": current_arr
            }
            status = f"Step {self.current_step + 1}/{len(self.steps)}: {description}"

            return fig, status, step_info

        except Exception as e:
            # If user input is bad, show a friendly message
            fig = self.create_error_visualization(f"Error: {str(e)}")
            return fig, f"Error: {str(e)}", {"current_step": 0, "total_steps": 0, "array": []}


    def reset(self):
        """Clear recorded steps."""
        self.steps = []
        self.current_step = 0


    def has_initialized_steps(self) -> bool:
        """Return True if sorting steps are ready."""
        return len(self.steps) > 0



# Global instance used by Gradio buttons
visualizer = InsertionSortVisualizer()


def next_step(input_array):
    """Called when user clicks Next Step."""
    return visualizer.sort_with_visualization(input_array)


def previous_step(input_array):
    """
    Moves backward one step.
    """
    try:
        if not visualizer.has_initialized_steps():
            fig = visualizer.create_error_visualization("Please initialize first.")
            return fig, "Array not initialized.", {"current_step": 0, "total_steps": 0, "array": []}

        # Move backward if possible
        if visualizer.current_step > 0:
            visualizer.current_step -= 1

        # Draw the previous step
        current_arr, description, current_index = visualizer.steps[visualizer.current_step]
        fig = visualizer.create_visualization(current_arr, description, current_index)

        step_info = {
            "current_step": visualizer.current_step + 1,
            "total_steps": len(visualizer.steps),
            "array": current_arr
        }
        status = f"Step {visualizer.current_step + 1}/{len(visualizer.steps)}: {description}"

        return fig, status, step_info

    except Exception as e:
        fig = visualizer.create_error_visualization(f"Error: {str(e)}")
        return fig, f"Error: {str(e)}", {"current_step": 0, "total_steps": 0, "array": []}



def generate_random_array():
    """
    Creates new random data and resets the visualizer.
    """
    visualizer.reset()
    sample_data = visualizer.generate_sample_data(8)
    sample_str = ', '.join(map(str, sample_data))

    fig = visualizer.create_error_visualization("Array generated! Click 'Next Step' to begin.")

    return sample_str, fig, "Array generated! Click 'Next Step' to start.", {"current_step": 0, "total_steps": 0, "array": []}



def input_changed(input_array):
    """
    Called when user edits the input array textbox.
    Resets sorting steps.
    """
    visualizer.reset()

    if input_array.strip():
        fig = visualizer.create_error_visualization("Input updated! Click Next Step to sort.")
        status = "Input changed! Click 'Next Step' to start sorting."
    else:
        fig = visualizer.create_error_visualization("Enter numbers or generate random array.")
        status = "Please enter an array or generate a random one."

    return fig, status, {"current_step": 0, "total_steps": 0, "array": []}



def create_gradio_interface():
    """
    Builds the full Gradio GUI.
    """
    try:
        demo = gr.Blocks(theme=gr.themes.Soft(), title="Insertion Sort Visualizer")
    except TypeError:
        demo = gr.Blocks(title="Insertion Sort Visualizer")

    with demo:
        # --- UI Layout + Instructions ---
        gr.Markdown("""
# 🔍 Insertion Sort Algorithm Visualizer
Follow each step of the insertion sort algorithm interactively.
        """)

        with gr.Row():
            # Left column: controls
            with gr.Column(scale=1):
                input_array = gr.Textbox(
                    label="Input Array (comma-separated numbers)",
                    placeholder="e.g., 5, 2, 8, 1, 9, 3",
                    value="",
                )

                generate_btn = gr.Button("🎲 Generate Random Array", variant="secondary")

                with gr.Row():
                    prev_btn = gr.Button("⏮️ Previous Step", variant="secondary")
                    next_btn = gr.Button("⏭️ Next Step", variant="primary")

                status = gr.Textbox(label="Status")
                step_info = gr.JSON(label="Step Information")

            # Right column: graph area
            with gr.Column(scale=2):
                plot = gr.Plot(
                    label="Insertion Sort Visualization",
                    value=visualizer.create_error_visualization(
                        "Welcome! Enter or generate an array to begin."
                    )
                )

        # Button wiring
        generate_btn.click(generate_random_array, outputs=[input_array, plot, status, step_info])
        next_btn.click(next_step, inputs=[input_array], outputs=[plot, status, step_info])
        prev_btn.click(previous_step, inputs=[input_array], outputs=[plot, status, step_info])
        input_array.change(input_changed, inputs=[input_array], outputs=[plot, status, step_info])

    return demo



def main():
    """Runs the Gradio interface."""
    print("\n🚀 Starting Gradio Interface...")
    demo = create_gradio_interface()
    demo.launch(share=False)



if __name__ == "__main__":
    main()
