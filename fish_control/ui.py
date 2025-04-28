# fish_control/ui.py
import os
import yaml
from flask import Flask, request, redirect, render_template_string

# Path to your YAML
CFG_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "cfg.yaml"
))

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Fish-Control GUI</title>
<style>
  body { font-size: 18px; font-family: sans-serif; margin: 20px; }
  .column { float: left; width: 48%; padding: 1%; box-sizing: border-box; }
  .clearfix::after { content: ""; clear: both; display: table; }
  label { display: block; margin-bottom: 8px; }
  button { margin-top: 10px; padding: 8px 16px; font-size: 1em; }
</style>
<h1>Fish-Control Parameters</h1>
<form method="post">
  <div class="clearfix">
    <div class="column">
      <label>Mode:
        <select name="mode">
          {% for m in ["standby","test","symmetric_sin"] %}
          <option value="{{m}}" {% if cfg.mode==m %}selected{% endif %}>{{m}}</option>
          {% endfor %}
        </select>
      </label>
      <label>Amplitude Tail: <input name="amplitude_tail" type="number" step="0.1" value="{{cfg.amplitude_tail}}"></label>
      <label>Amplitude Fin:  <input name="amplitude_fin"  type="number" step="0.1" value="{{cfg.amplitude_fin}}"></label>
      <label>Frequency:      <input name="frequency"      type="number" step="0.01" value="{{cfg.frequency}}"></label>
      <label>Phase:          <input name="phase"          type="number" step="0.01" value="{{cfg.phase}}"></label>
    </div>
    <div class="column">
      <label>Phi Tail (test):<input name="phi_tail" type="number" step="0.1" value="{{cfg.phi_tail}}"></label>
      <label>Phi Fin  (test):<input name="phi_fin"  type="number" step="0.1" value="{{cfg.phi_fin}}"></label>
      <button type="submit" name="save_cfg">Save Config</button>
      <button type="submit" name="toggle_logging">
        {% if cfg.logging %}Stop Logging{% else %}Start Logging{% endif %}
      </button>
    </div>
  </div>
</form>
"""

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        old_cfg = yaml.safe_load(open(CFG_PATH))
        # build updated config
        new_cfg = {
            "mode": request.form["mode"],
            "amplitude_tail": float(request.form["amplitude_tail"]),
            "amplitude_fin":  float(request.form["amplitude_fin"]),
            "frequency":      float(request.form["frequency"]),
            "phase":          float(request.form["phase"]),
        }
        new_cfg["phi_tail"] = float(request.form.get("phi_tail", 0.0))
        new_cfg["phi_fin"]  = float(request.form.get("phi_fin",  0.0))
        # toggle logging only if that button was pressed
        if "toggle_logging" in request.form:
            new_cfg["logging"] = not old_cfg.get("logging", False)
        else:
            new_cfg["logging"] = old_cfg.get("logging", False)
        with open(CFG_PATH, "w") as f:
            yaml.safe_dump(new_cfg, f)
        return redirect("/")

    # GET: load current cfg
    cfg = yaml.safe_load(open(CFG_PATH))
    # allow `.mode`, `.amplitude_tail` in template
    class Cfg: pass
    c = Cfg()
    for k,v in cfg.items():
        setattr(c, k, v)
    # fill defaults for missing keys
    for key, val in [("phi_tail", 0.0), ("phi_fin", 0.0)]:
        setattr(c, key, cfg.get(key, val))
    setattr(c, "logging", cfg.get("logging", False))
    return render_template_string(TEMPLATE, cfg=c)

if __name__ == "__main__":
    # only for local testing; 0.0.0.0 makes it reachable from your Mac
    app.run(host="0.0.0.0", port=5000, debug=True)