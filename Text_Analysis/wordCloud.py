from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np


def wordcloud(filename,stopwords , show = False):
    with open(filename, "r") as f:
        text = str(f.readlines())

    #Setup Wordcloud
    liste_der_unerwuenschten_woerter = stopwords.split()
    STOPWORDS.update(liste_der_unerwuenschten_woerter)
    x, y = np.ogrid[:1000, :1000]
    mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 ** 2
    mask = 255 * mask.astype(int)
    wordcloud = WordCloud(background_color="white",width=1920, height=1080, mask=mask).generate(text)
    
    #Plot (if desired) and Save Wordcloud as PNG
    plt.imshow(wordcloud, interpolation="bilinear")
    if show == True: 
        plt.show()
    filename = filename.replace(".transcript", "") + 'WC.png'
    plt.savefig(filename)
    print("PNG saves as: " + filename)
    