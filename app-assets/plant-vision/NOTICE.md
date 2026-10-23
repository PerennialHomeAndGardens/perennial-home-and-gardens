# Leaf comparison attribution and scope

Model: Greenathon Plant AI by Rishit Dagli and contributors. Apache License 2.0.
Source: https://github.com/Rishit-dagli/Greenathon-Plant-AI
Pinned revision: b7e8c6f5a1b3e1b7847f3e78f41a65a8a9110235.
The 224×224 RGB model uses values divided by 255 and outputs 38 PlantVillage crop/condition classes. Model weights are unchanged. Perennial added a separate interface, crop restriction, field-photo validation and local-only loading.

TensorFlow.js 4.22.0, Copyright Google LLC, Apache License 2.0. https://github.com/tensorflow/tfjs
License texts are included alongside these files. The runtime and weights are served from this website; visitors' photos are not transmitted to a model provider.

Training data: PlantVillage, David P. Hughes and Marcel Salathé, https://arxiv.org/abs/1511.08060 . This is primarily controlled leaf imagery. A model trained on it may fail on field photographs, unsupported species, mixed symptoms or unrelated objects. A model score is not a calibrated probability of diagnosis.

Validation: deterministic samples from the PlantDoc test directories, https://github.com/pratikkayal/PlantDoc-Dataset at 5467f6012d78d1c446145d5f582da6096f852ae8. Dataset supplied under CC BY 4.0 (see upstream LICENSE.txt). Field-image rights and original sources are described by that dataset's maintainers. Test images are used during QA only and are not republished as website artwork. Results and exact sample URLs appear in /qa/leaf-model-validation.json.
