from flask import Flask, request, jsonify
import pandas as pd
from tabulate import tabulate
from app.converters.xml_converter import xml_to_dataframe
from app.converters.json_converter import json_to_dataframe
from app.converters.csv_converter import csv_to_dataframe

app = Flask(__name__)

# Global variable to store the DataFrame
stored_df = None

@app.route('/inlet', methods=['POST'])
def inlet():
    global stored_df
    
    # Check if file was uploaded
    if 'file' not in request.files and 'data' not in request.form:
        return jsonify({"error": "No file or data provided"}), 400
    
    try:
        # Determine the format (XML, JSON, or CSV)
        data_format = request.args.get('format', '').lower()
        
        if 'file' in request.files:
            file = request.files['file']
            if data_format == '':
                # Try to determine format from filename
                filename = file.filename
                if filename.endswith('.xml'):
                    data_format = 'xml'
                elif filename.endswith('.json'):
                    data_format = 'json'
                elif filename.endswith('.csv'):
                    data_format = 'csv'
                else:
                    return jsonify({"error": "Could not determine file format. Please specify format parameter."}), 400
            
            content = file.read()
        else:
            content = request.form['data']
            if data_format == '':
                return jsonify({"error": "Please specify format parameter when sending raw data."}), 400
        
        # Parse the data based on format
        if data_format == 'xml':
            stored_df = xml_to_dataframe(content)
        elif data_format == 'json':
            stored_df = json_to_dataframe(content)
        elif data_format == 'csv':
            stored_df = csv_to_dataframe(content)
        else:
            return jsonify({"error": f"Unsupported format: {data_format}"}), 400
        
        return jsonify({
            "message": "Data processed successfully",
            "rows": len(stored_df),
            "columns": list(stored_df.columns)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/outlet', methods=['GET'])
def outlet():
    global stored_df
    
    if stored_df is None:
        return jsonify({"error": "No data has been processed yet"}), 404
    
    output_format = request.args.get('format', 'json').lower()
    
    try:
        if output_format == 'text':
            # Return tabulated text
            table = tabulate(stored_df, headers='keys', tablefmt='grid')
            return table, 200, {'Content-Type': 'text/plain'}
        elif output_format == 'json':
            # Return JSON representation of the DataFrame
            return jsonify({
                "data": stored_df.to_dict(orient='records'),
                "columns": list(stored_df.columns),
                "index": list(stored_df.index)
            })
        elif output_format == 'html':
            # Return HTML table
            html_table = stored_df.to_html()
            return html_table, 200, {'Content-Type': 'text/html'}
        elif output_format == 'dataframe':
            # This is just for demonstration - in a real API you'd need to serialize this differently
            return jsonify({"message": "DataFrame is available in memory"}), 200
        else:
            return jsonify({"error": f"Unsupported output format: {output_format}"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
