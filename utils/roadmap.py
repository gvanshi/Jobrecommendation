import pandas as pd
from fuzzywuzzy import process
import graphviz

# Load roadmap data
roadmap_df = pd.read_csv("data/job_roadmap.csv")

def generate_roadmap(job_role, experience_level):
    """Finds closest job and returns roadmap steps."""
    closest_match = process.extractOne(job_role, roadmap_df['Job Role'])[0]
    row = roadmap_df[roadmap_df['Job Role'] == closest_match]
    
    if not row.empty:
        roadmap_steps = row.iloc[0]['Suggested Roadmap'].split(" → ")
        steps = roadmap_steps[:experience_level + 1]  # Trim steps by experience
        return steps
    return []

def draw_roadmap(steps):
    """Returns Graphviz object of the roadmap."""
    if not steps:
        return None
    graph = graphviz.Digraph(format='png')
    for i in range(len(steps) - 1):
        graph.edge(steps[i], steps[i + 1])
    return graph
