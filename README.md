# metaflow-tensorflow-pickle-issue

This is a repository created to reproduce an
issue with metaflow trying to checkpoint
tensorflow dataset objects and models

## How to reproduce

Run:

```sh
git clone git@github.com:sandman21dan/metaflow-tensorflow-pickle-issue.git
```

```sh
docker build . -t metaflow-tensorflow-issue
```

```sh
docker run metaflow-tensorflow-issue
```

## Issue

I'd like that the dataset transformations
get checkpointed/separated into a differnt step
so that I can resume it

Even if the dataset part is ignored, the model
produced by tensorflow.keras is also not pickable
due to Rlock objects

### Error on focus

The full run logs can be found in the [error.txt](./error.txt) file

```
2020-02-16 13:04:40.668 [1581858157185440/get_dataset_batches/2 (pid 21)] sha, size, encoding = self._save_object(obj, var, force_v4)
2020-02-16 13:04:40.668 [1581858157185440/get_dataset_batches/2 (pid 21)] File "/root/.local/share/virtualenvs/app-lp47FrbD/lib/python3.7/site-packages/metaflow/datastore/datastore.py", line 430, in _save_object
2020-02-16 13:04:40.668 [1581858157185440/get_dataset_batches/2 (pid 21)] transformable_obj.transform(lambda x: pickle.dumps(x, protocol=2))
2020-02-16 13:04:40.668 [1581858157185440/get_dataset_batches/2 (pid 21)] File "/root/.local/share/virtualenvs/app-lp47FrbD/lib/python3.7/site-packages/metaflow/datastore/datastore.py", line 67, in transform
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] temp = transformer(self._object)
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] File "/root/.local/share/virtualenvs/app-lp47FrbD/lib/python3.7/site-packages/metaflow/datastore/datastore.py", line 430, in <lambda>
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] transformable_obj.transform(lambda x: pickle.dumps(x, protocol=2))
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] File "/root/.local/share/virtualenvs/app-lp47FrbD/lib/python3.7/site-packages/tensorflow_core/python/framework/ops.py", line 873, in __reduce__
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] return convert_to_tensor, (self._numpy(),)
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] File "/root/.local/share/virtualenvs/app-lp47FrbD/lib/python3.7/site-packages/tensorflow_core/python/framework/ops.py", line 910, in _numpy
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] six.raise_from(core._status_to_exception(e.code, e.message), None)
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] File "<string>", line 3, in raise_from
2020-02-16 13:04:40.669 [1581858157185440/get_dataset_batches/2 (pid 21)] tensorflow.python.framework.errors_impl.InternalError: Tensorflow type 21 not convertible to numpy dtype
```
