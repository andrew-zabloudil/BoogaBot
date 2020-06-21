import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import discord
from discord.ext import commands


char2idx = {
    '\n': 0, '\r': 1, ' ': 2, '!': 3, '"': 4, '#': 5, '$': 6, '%': 7,
    '&': 8, "'": 9, '(': 10, ')': 11, '*': 12, ',': 13, '-': 14,
    '.': 15, '/': 16, '0': 17, '1': 18, '2': 19, '3': 20, '4': 21,
    '5': 22, '6': 23, '7': 24, '8': 25, '9': 26, ':': 27, ';': 28,
    '?': 29, 'A': 30, 'B': 31, 'C': 32, 'D': 33, 'E': 34, 'F': 35,
    'G': 36, 'H': 37, 'I': 38, 'J': 39, 'K': 40, 'L': 41, 'M': 42,
    'N': 43, 'O': 44, 'P': 45, 'Q': 46, 'R': 47, 'S': 48, 'T': 49,
    'U': 50, 'V': 51, 'W': 52, 'Y': 53, 'Z': 54, 'a': 55, 'b': 56,
    'c': 57, 'd': 58, 'e': 59, 'f': 60, 'g': 61, 'h': 62, 'i': 63,
    'j': 64, 'k': 65, 'l': 66, 'm': 67, 'n': 68, 'o': 69, 'p': 70,
    'q': 71, 'r': 72, 's': 73, 't': 74, 'u': 75, 'v': 76, 'w': 77,
    'x': 78, 'y': 79, 'z': 80, 'ñ': 81, '—': 82, '‘': 83, '’': 84,
    '“': 85, '”': 86, '…': 87, 'ﬁ': 88
}

idx2char = [
    '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', ',',
    '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';',
    '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z', 'a', 'b', 'c', 'd',
    'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z', 'ñ', '—', '‘', '’', '“', '”', '…', 'ﬁ'
]


class Dadbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        model_path = os.path.join(os.getcwd(), 'cogs/dad_joke_model')
        self.model = keras.models.load_model(model_path)
        self.model.compile(optimizer='adam', loss=loss)

    @commands.command(name="dad-joke", help="Generates a dad joke from a seed input")
    async def dad_joke(self, ctx, seed="how"):
        async with ctx.typing():
            await ctx.send(f'{ctx.author.mention} {generate_text(self.model, char2idx, idx2char, start_string=seed)}')


def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


def generate_text(model, char2idx, idx2char, start_string):
    # Number of characters to generate
    num_generate = 170

    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store results
    text_generated = []

    # Lower temperatures are more predictable, higher temperatures are more surprising
    temperature = 1.0

    model.reset_states()
    for _ in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(
            predictions, num_samples=1)[-1, 0].numpy()

        input_eval = tf.expand_dims([predicted_id], 0)
        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated).split('\n')[0])
