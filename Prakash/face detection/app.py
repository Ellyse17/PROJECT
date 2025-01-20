import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from face_recognition import detect_faces, match_faces

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        file = request.files.get("image")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Detect faces
            faces, image_path = detect_faces(filepath)
            if len(faces) > 0:
                return render_template("result.html", image_path=image_path, faces=len(faces))
            else:
                flash("No faces detected. Try a different image.")
                return redirect(url_for("index"))
        else:
            flash("No file selected. Please upload an image.")
            return redirect(url_for("index"))
    return render_template("index.html")


@app.route("/match", methods=["POST"])
def match():
    # Handle face matching
    file1 = request.files.get("image1")
    file2 = request.files.get("image2")

    if file1 and file2:
        # Save files
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename))
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename))
        file1.save(filepath1)
        file2.save(filepath2)

        # Match faces
        match_percentage = match_faces(filepath1, filepath2)
        return render_template("result.html", match_percentage=match_percentage)
    else:
        flash("Both images must be uploaded.")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
