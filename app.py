
import tracemalloc
tracemalloc.start(25)

import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
from pathlib import Path
def dump_memory_snapshot():
    snapshot = tracemalloc.take_snapshot()
    snapshot.dump("/home/site/repository/memory_snapshot.dump")
app = Flask(__name__)
dump_memory_snapshot()

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route("/_diag/snapshot")
def snapshot_route():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")[:20]  # top 20 lines
    data = []
    for stat in top_stats:
        frame = stat.traceback[0]
        data.append({
            "file": frame.filename,
            "line": frame.lineno,
            "size_kib": round(stat.size / 1024, 2),
            "count": stat.count,
        })
    current, peak = tracemalloc.get_traced_memory()
    return jsonify({
        "current_bytes": current,
        "peak_bytes": peak,
        "top_allocations": data
    })

if __name__ == '__main__':
   app.run()
