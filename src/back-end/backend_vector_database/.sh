python -m venv .venv
.venv/Scripts/activate
pip install -r requirements_llms-offline_full.txt
cd src/back-end

python backend_vector_database/create_vector_database_QdantLocal.py --excel backend_vector_database/dataset/LegalRAG.xlsx


