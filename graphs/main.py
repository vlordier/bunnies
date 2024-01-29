"""
    This is the main file for the graph.
"""

from src.graph import WorkFlow

# Create the graph
app = WorkFlow().app

# Run the graph
app.invoke({})
