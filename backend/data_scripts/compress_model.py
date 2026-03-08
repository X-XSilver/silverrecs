import compress_fasttext
from gensim.models.fasttext import load_facebook_model
import os

scripts_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(scripts_folder)
data_folder = os.path.join(root_folder, "data")

MODEL_PATH = os.path.join(data_folder, "cc.en.300.bin")

big_model = load_facebook_model(MODEL_PATH)

small_model = compress_fasttext.prune_ft_freq(big_model.wv, new_vocab_size=50000, pq=True)

small_model.save(f'{data_folder}/cc.en.300.compressed.bin')