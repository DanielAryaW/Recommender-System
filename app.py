from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

app = Flask(__name__)

# Load dataset
data = pd.read_excel(
    "C:/Users/Asus/Recommender System/project-folder/Dataset PBI.xlsx")


def calculate_similarity(input_data, dataset):
    dataset_matrix = dataset[['Nilai Tes/Rapor']].values
    input_vector = [[input_data['Nilai Tes/Rapor']]]
    distances = cdist(dataset_matrix, input_vector, metric='euclidean')
    return distances

# Function to predict admission


def predict_admission(input_data, dataset, k=5):
    results = {}
    for pilihan in ['Pilihan 1', 'Pilihan 2', 'Pilihan 3']:
        current_prodi = input_data[pilihan]
        filtered_dataset = dataset[
            (dataset['Prodi'] == current_prodi) & (
                dataset[pilihan] == current_prodi)
        ].copy()

        if filtered_dataset.empty:
            results[current_prodi] = "Data Tidak Cukup"
            continue

        distances = calculate_similarity(input_data, filtered_dataset)
        filtered_dataset['Distance'] = distances

        nearest_neighbors = filtered_dataset.nsmallest(k, 'Distance')
        prediction = nearest_neighbors['Keputusan Prodi'].mode()[0]
        results[current_prodi] = prediction

    return results


def recommend_program(input_candidate, dataset):
    # Calculate the average score for each program
    program_scores = dataset.groupby(
        'Pilihan 1')['Nilai Tes/Rapor'].mean().to_dict()

    # Find the program with the closest average score to the candidate's score
    candidate_score = input_candidate['Nilai Tes/Rapor']
    recommended_program = min(program_scores, key=lambda program: abs(
        program_scores[program] - candidate_score))

    return recommended_program

# Flask routes


@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    prediction = None

    if request.method == "POST":
        # Get form data

        pilihan1 = request.form.get("pilihan1")
        pilihan2 = request.form.get("pilihan2")
        pilihan3 = request.form.get("pilihan3")
        provinsi_calon = request.form.get("provinsi_calon")
        provinsi_sekolah = request.form.get("provinsi_sekolah")
        tipe_sekolah = request.form.get("tipe_sekolah")
        nilai = float(request.form.get("nilai"))

        # Validate inputs
        if not (0 <= float(nilai) <= 100):
            return jsonify({"error": "Nilai Tes/Rapor harus antara 0 sampai 100"})

        # if "Pendidikan Bahasa Inggris" not in [pilihan1, pilihan2, pilihan3]:
         #   return jsonify({"error": "Salah satu pilihan harus berisi Pendidikan Bahasa Inggris"})

        # Prepare input data
        input_candidate = {
            'Pilihan 1': pilihan1,
            'Pilihan 2': pilihan2,
            'Pilihan 3': pilihan3,
            'Propinsi Asal Calon Mahasiswa': provinsi_calon,
            'Propinsi Asal Sekolah Calon Mahasiswa': provinsi_sekolah,
            'Tipe Sekolah': tipe_sekolah,
            'Nilai Tes/Rapor': float(nilai)
        }

        # Predict
        dataset_for_prediction = data.copy()
        predicted_status = predict_admission(
            input_candidate, dataset_for_prediction)

        # Recommend a suitable program based on input data
        recommended_program = recommend_program(
            input_candidate, dataset_for_prediction)

        prediction = predicted_status
        recommendation = recommended_program

    # Dropdown options
    prodi_options = pd.concat(
        [data['Pilihan 1'], data['Pilihan 2'], data['Pilihan 3']]).unique().tolist()
    provinsi_options = data['Propinsi Asal Calon Mahasiswa'].unique().tolist()
    tipe_sekolah_options = data['Tipe Sekolah'].unique().tolist()

    return render_template("index.html",
                           prodi_options=prodi_options,
                           provinsi_options=provinsi_options,
                           tipe_sekolah_options=tipe_sekolah_options,
                           prediction=prediction,
                           recommendation=recommendation)


if __name__ == "__main__":
    app.run(debug=True)
