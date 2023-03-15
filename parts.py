import pandas as pd
from flask import Flask, jsonify, request

# Start Flask

app = Flask(__name__)

# CSV data to memory

df = pd.read_csv('LE.txt', encoding='ISO-8859-1', delimiter='\t')
df.fillna('', inplace=True)

# Json format

@app.route('/spare-parts')
def spare_parts():

    # Pagination p1

    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=30, type=int)

    # Search parameters

    serial_number = request.args.get('serial_number')
    part_name = request.args.get('part_name')

    # Define name and serial number
    if serial_number:
        filtered_df = df.loc[df['00002356517'] == serial_number]
    elif part_name:
        filtered_df = df.loc[df['Valuveljed '].str.contains(
            part_name, case=False)]
    else:
        filtered_df = df

    # Pagination p2

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_df = filtered_df.iloc[start_index:end_index]
    return jsonify({
        'data': paginated_df.to_dict(orient='records'),
        'page': page,
        'page_size': page_size
    })

# Run Flask web server
if __name__ == '__main__':
    app.run(debug=True)