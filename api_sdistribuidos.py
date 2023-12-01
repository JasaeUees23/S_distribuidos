from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/distribution', methods=['POST'])
def distribute_process():
    task = request.json['distribution']

    # Distribuir la tarea a los seguidores

    m_results = []

    return jsonify({'Resultados': m_results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
