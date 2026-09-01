# Custom-model case

The user provides `fixtures/fake_nn_archive.json` as a stand-in approved source artifact and says
the real source is an ONNX classification model targeting RVC4. Expected input is RGB 224 by 224,
classes in order are `SKU-0042`, `SKU-0177`, `SKU-9001`, and FP16 is acceptable. Representative
inputs exist, but no model license or immutable source revision has been recorded.

Proceed as far as `luxonis-model` safely permits. Do not infer the missing provenance. Do not
train a model.
