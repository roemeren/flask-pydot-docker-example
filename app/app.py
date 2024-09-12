from flask import Flask, render_template, request
import os
import pandas as pd
import pydot
import zipfile

app = Flask(__name__)

# Ensure the upload directory exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    zip_filename = None
    if request.method == "POST":
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file"

        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Process the CSV file to generate the graphs
            zip_filename = process_csv(filepath)
    
    return render_template("index.html", filename = zip_filename)

def process_csv(filepath):
    df = pd.read_csv(filepath)

    if 'from' not in df.columns or 'to' not in df.columns or 'group' not in df.columns:
        raise ValueError("CSV file must contain 'from', 'to', and 'group' columns.")

    # Create a directory for temporary PNG files
    temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    groups = df['group'].unique()
    graph_files = []
    
    for group in groups:
        group_df = df[df['group'] == group]
        graph = pydot.Dot(graph_type='digraph')
        for _, row in group_df.iterrows():
            edge = pydot.Edge(str(row['from']), str(row['to']))
            graph.add_edge(edge)
        graph_filename = f'{group}_network_graph.png'
        graph_output = os.path.join(temp_dir, graph_filename)
        graph.write_png(graph_output)
        graph_files.append(graph_output)
    
    # Create a ZIP file of the PNG files
    zip_filename = 'network_graphs.zip'
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in graph_files:
            zipf.write(file, os.path.basename(file))
    
    # Clean up temporary files
    for file in graph_files:
        os.remove(file)
    os.rmdir(temp_dir)
    
    return zip_filename

if __name__ == "__main__":
    app.run(debug=True)