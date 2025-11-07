# Recommender System (Universitas Sanata Dharma)

Singkat:
1. Buat virtual environment:
   python -m venv venv
2. Aktifkan venv:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependensi:
   pip install -r requirements.txt

Membuat requirements.txt dari venv lokal Anda:
1. Aktifkan venv yang saat ini Anda pakai.
2. Jalankan:
   pip freeze > requirements.txt
3. Commit requirements.txt ke repo.

Menambahkan ke GitHub:
1. git init
2. git add .
3. git commit -m "Initial commit"
4. Buat repo di GitHub (web) atau gunakan `gh`:
   gh repo create <nama-repo> --public --source=. --remote=origin --push
atau:
   git remote add origin https://github.com/USERNAME/REPO.git
   git branch -M main
   git push -u origin main
