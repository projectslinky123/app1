import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64

def create_figure(xtitle, ytitle, x, y):
    fig = plt.figure(figsize=(15, 5))
    axis = fig.add_subplot(1, 1, 1)
    axis.set_xlabel(xtitle)
    axis.set_ylabel(ytitle)
    axis.grid()
    axis.plot(list(map(int, y)))
    xlabels = [""]
    xticks = [0]
    spacing = len(x)//10
    for i in range(11):
        xticks.append(spacing*i)
        xlabels.append(x[spacing*i])

    axis.set_xticks(xticks)
    axis.set_xticklabels(xlabels, rotation=70)
    fig.tight_layout()

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String