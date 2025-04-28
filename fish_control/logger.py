import csv, time, os, pathlib

class CSVLogger:
    def __init__(self, root="logs"):
        pathlib.Path(root).mkdir(exist_ok=True)
        fname = f"{root}/{time.strftime('%Y%m%d-%H%M%S')}.csv"
        self.f = open(fname, "w", newline="")
        self.w = csv.writer(self.f)
        self.w.writerow(
            "t,p_phi,p_theta,f_phi,f_theta,pos_deg,curr_mA,volt_V, MODE".split(",")
        )

    def row(self, *values):
        self.w.writerow(values)
        self.f.flush()