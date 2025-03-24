import matplotlib.pyplot as plt

def setup_plotting():
    # set plotting parameters
    plt.rcParams.update({
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": False,
        "pgf.rcfonts": False,
    })
    
    # set plotting style
    plt.style.use("seaborn-v0_8-colorblind")

    # set format of saved figures
    plt.rcParams["savefig.format"] = "pgf"