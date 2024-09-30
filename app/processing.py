import os
import pandas as pd
import pydot
import zipfile
from common import progress_data

def process_csv(filepath, uploadfolder):
    df = pd.read_csv(filepath)

    if 'from' not in df.columns or 'to' not in df.columns or 'group' not in df.columns:
        raise ValueError("CSV file must contain 'from', 'to', and 'group' columns.")

    # Create a directory for temporary PNG files
    temp_dir = os.path.join(uploadfolder, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    groups = df['group'].unique()
    graph_files = []
    total_groups = len(groups)
    current_progress = 0

    for group in groups:
        group_df = df[df['group'] == group]
        graph = pydot.Dot(graph_type='digraph')
        # note: _ indicates that the index is ignored
        for _, row in group_df.iterrows():
            edge = pydot.Edge(str(row['from']), str(row['to']))
            graph.add_edge(edge)
        graph_filename = f'{group}_network_graph.png'
        graph_output = os.path.join(temp_dir, graph_filename)
        graph.write_png(graph_output)
        graph_files.append(graph_output)

        # Update progress
        current_progress += 1
        progress_data['progress'] = int((current_progress / total_groups) * 100)

    # Create a ZIP file of the output PNG files
    zip_filename = 'network_graphs.zip'
    zip_path = os.path.join(uploadfolder, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in graph_files:
            zipf.write(file, os.path.basename(file))

    # Clean up temporary files
    for file in graph_files:
        os.remove(file)
    os.rmdir(temp_dir)

    # Set the filename for download once processing is complete
    progress_data['filename'] = zip_filename
    # Ensure progress reaches 100 after processing
    progress_data['progress'] = 100 

    return zip_filename