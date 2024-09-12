from flask import Flask, render_template, request, send_from_directory
import os
import pandas as pd
import pydot

app = Flask(__name__)

# Ensure the upload directory exists (os.path ensures OS compatible path)
# note: serving files from static directory simplifies the code (no routing)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for file upload and graph generation
@app.route("/", methods=["GET", "POST"])
def index():
    # First call is a GET request
    file_name = None
    if request.method == "POST":
        # Check if a file has been uploaded
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file"

        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Process the CSV file to generate the graph
            file_name = process_csv(filepath)
    return render_template("index.html", filename=file_name)

def process_csv(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)

    # Check if 'from' and 'to' columns exist
    if 'from' not in df.columns or 'to' not in df.columns:
        raise ValueError("CSV file must contain 'from' and 'to' columns.")

    # Create a directed graph
    graph = pydot.Dot(graph_type='digraph')

    # Add edges from the CSV file
    for _, row in df.iterrows():
        edge = pydot.Edge(str(row['from']), str(row['to']))
        graph.add_edge(edge)

    # Save the graph as a PNG file
    graph_filename = 'network_graph.png'
    graph_output = os.path.join(app.config['UPLOAD_FOLDER'], graph_filename)
    graph.write_png(graph_output)

    return graph_filename

#@app.route('/static/uploads/<filename>')
#def uploaded_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)