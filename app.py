import os
from flask import Flask, request, jsonify
from pypdf import PdfReader
from resumeparser import ats_extractor

# Set up the Flask app
UPLOAD_PATH = r"./uploads"  # Ensure this directory exists
app = Flask(__name__)

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)


@app.route("/")
def index():
    return jsonify({"message": "Resume Processing Backend is Running!"})


@app.route("/process", methods=["POST"])
def ats():
    try:
        # Check if a file is uploaded
        if "pdf_doc" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        # Save the uploaded file
        doc = request.files["pdf_doc"]
        if not doc.filename.endswith((".pdf", ".doc", ".docx")):
            return jsonify({"error": "Unsupported file format"}), 400

        file_path = os.path.join(UPLOAD_PATH, "uploaded_resume" + os.path.splitext(doc.filename)[1])
        doc.save(file_path)

        # Read the file content
        data = _read_file_from_path(file_path)

        # Extract ATS data
        extracted_data = ats_extractor(data)
        print("Extracted Data:", extracted_data)

        # Return extracted data as JSON
        return jsonify({"success": True, "data": extracted_data}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


def _read_file_from_path(path):
    """
    Read and extract text content from the provided file path.
    """
    try:
        reader = PdfReader(path)
        data = ""

        # Extract text from each page of the PDF
        for page_no in range(len(reader.pages)):
            page = reader.pages[page_no]
            data += page.extract_text()

        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        raise


if __name__ == "__main__":
    app.run(port=8000, debug=True)
