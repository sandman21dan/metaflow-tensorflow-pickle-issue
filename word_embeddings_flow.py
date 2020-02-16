from metaflow import FlowSpec, step


class EmbeddingFlow(FlowSpec):

    @step
    def start(self):
        '''
        Simply starts the flow
        '''
        self.next(self.get_dataset_batches)

    @step
    def get_dataset_batches(self):
        '''
        Pull the dataset from tensorflow_datasets
        and get the batches
        '''
        import tensorflow_datasets as tfds

        (self.train_data, self.test_data), info = tfds.load(
            'imdb_reviews/subwords8k',
            split=(tfds.Split.TRAIN, tfds.Split.TEST),
            with_info=True,
            as_supervised=True,
        )

        self.encoder = info.features['text'].encoder

        self.next(self.define_model)

    @step
    def define_model(self):
        '''
        Define de model with hyper parameters
        '''
        from tensorflow import keras
        from tensorflow.keras import layers

        embedding_dimensions = 16

        self.model = keras.Sequential([
            layers.Embedding(self.encoder.vocab_size, embedding_dimensions),
            layers.GlobalAveragePooling1D(),
            layers.Dense(1, activation='sigmoid'),
        ])
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy'],
        )

        self.next(self.train)

    @step
    def train(self):
        '''
        Train the embeddings model
        '''
        self.history = self.model.fit(
            self.train_batches,
            epochs=10,
            validation_data=self.test_batches,
            validation_steps=20,
        )

        self.next(self.plot_training)

    @step
    def plot_training(self):
        '''
        Save a plot of the training history
        '''
        import matplotlib.pyplot as plt

        history_dict = self.history.history
        acc = history_dict['accuracy']
        val_acc = history_dict['val_accuracy']
        epocs = range(1, len(acc) + 1)

        plt.figure(figsize=(12, 9))
        plt.plot(epocs, acc, 'bo', label='Training acc')
        plt.plot(epocs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend(loc='lower right')
        plt.ylim((.5, 1))
        plt.savefig("train_accuracy.png")

        self.next(self.retrieve_embeddings)

    @step
    def retrieve_embeddings(self):
        '''
        Retrieves and produces tsv files
        for viewing in the browser
        '''
        import csv

        weights = self.model.layers[0].get_weights()[0]

        with open('vectors.tsv', 'w') as vectors_file:
            vec_writer = csv.writer(vectors_file, delimiter='\t')
            with open('metadata.tsv', 'w') as metadata_file:
                meta_writer = csv.writer(metadata_file, delimiter='\t')

                for num, word in enumerate(self.encoder.subwords):
                    vec = weights[num + 1]
                    meta_writer.writerow([word])
                    vec_writer.writerow([str(x) for x in vec])

        self.next(self.end)

    @step
    def end(self):
        '''
        End
        '''
        pass


if __name__ == '__main__':
    EmbeddingFlow()
