import datasets
from transformers import AutoTokenizer, DataCollatorForTokenClassification, TFAutoModelForTokenClassification, create_optimizer
from transformers.keras_callbacks import KerasMetricCallback
import evaluate
import numpy as np
import tensorflow as tf
import pandas as pd
from bson.binary import Binary
from pymongo.mongo_client import MongoClient
from bson.binary import Binary
import gridfs
import pickle

uri = "mongodb://danielsz:ysDC3xbgKOj863d7@ac-noqw4xe-shard-00-00.qqrkswo.mongodb.net:27017,ac-noqw4xe-shard-00-01.qqrkswo.mongodb.net:27017,ac-noqw4xe-shard-00-02.qqrkswo.mongodb.net:27017/?ssl=true&replicaSet=atlas-3kz2n9-shard-0&authSource=admin&retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['dsp']
training_collection = db['reddit_training']


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



id2label = {
    0: "O",
    1: "B-drug"
}

label2id = {
    "O": 0,
    "B-drug": 1,
}


drugs_train = datasets.Dataset.from_pandas(pd.DataFrame(list(training_collection.find({'bert_training': 'train'},{'_id' : 0}))))
drugs_val = datasets.Dataset.from_pandas(pd.DataFrame(list(training_collection.find({'bert_training': 'validation'},{'_id' : 0}))))
drugs_test = datasets.Dataset.from_pandas(pd.DataFrame(list(training_collection.find({'bert_training': 'test'},{'_id' : 0}))))



drugs = datasets.DatasetDict({'train' : drugs_train, 'validation' : drugs_val, 'test' : drugs_test})


def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)

    labels = []
    for i, label in enumerate(examples[f"ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = seqeval.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }



label_list = list(label2id.keys())

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

tokenized_drugs = drugs.map(tokenize_and_align_labels, batched=True)

seqeval = evaluate.load("seqeval")
example = drugs["train"][0]
labels = [label_list[i] for i in example[f"ner_tags"]]
data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer, return_tensors="tf")


model = TFAutoModelForTokenClassification.from_pretrained("bert-base-uncased", num_labels=2, id2label=id2label, label2id=label2id)


tf_train_set = model.prepare_tf_dataset(
    tokenized_drugs["train"],
    shuffle=True,
    batch_size=32,
    collate_fn=data_collator,
    prefetch = False
)

tf_val_set = model.prepare_tf_dataset(
    tokenized_drugs["validation"],
    shuffle=False,
    batch_size=32,
    collate_fn=data_collator,
    prefetch = False
)

tf_test_set = model.prepare_tf_dataset(
    tokenized_drugs["test"],
    shuffle=False,
    batch_size=32,
    collate_fn=data_collator,
    prefetch = False
)


batch_size = 32
num_train_epochs = 5
num_train_steps = (len(tokenized_drugs["train"]) // batch_size) * num_train_epochs
optimizer, lr_schedule = create_optimizer(
    init_lr=2e-4,
    num_train_steps=num_train_steps,
    weight_decay_rate=0.1,
    num_warmup_steps=0,
)

model.compile(optimizer=optimizer)
metric_callback = KerasMetricCallback(metric_fn=compute_metrics, eval_dataset=tf_val_set)
callbacks = [metric_callback]
history = model.fit(x=tf_train_set, validation_data = tf_val_set, epochs=num_train_epochs, callbacks=callbacks)
eval = model.evaluate(tf_test_set)

# Save the weights and the evaluation metrics to the database
fs = gridfs.GridFS(db)

weight_files_db = client['client_weights']
fs = gridfs.GridFS(weight_files_db)
weights_info_collection = db['client_weights']


weights, data_size = model.get_weights(), drugs_train.num_rows
bin = pickle.dumps(weights)
mongo_binary = Binary(bin)

file_id = fs.put(mongo_binary, filename='training_result_client_2.pkl')

document = {'weights_file_id' : file_id, 'data_count' : data_size, 'result_metrics' : eval}
weights_info_collection.insert_one(document)






