## ASR Component
This repository contains the code for the finetuning, training and inference of ASR models. During the SignOn project, hybrid ASR models were created with the help of Kaldi ASR, of which a sample Kaldi inference code is present in `/src/kaldi_inference`  directory. 

The Kaldi based models can be served via webservice. The webservice inference code is available at `src/webservice_inference/signon_api_v1_.py` The API documentation is available at [restasr.cls.ru.nl/api-docs/](https://restasr.cls.ru.nl/api-docs/).  English, Spanish, Dutch and Irish language ASR models are deployed via webservice. 

After Kaldi based hybrid ASR models, end-to-end models, are created by finetuning transformer based models i.e. [XLS-R 300Million parameters model](https://huggingface.co/facebook/wav2vec2-xls-r-300m). The finetuning scripts and inference scripts are present in the directory `src/wav2vec2_inference` . Spanish, Dutch and Irish language ASR models are finetuned with XLS-R. These models are deployed via webservice and the inference code can be found at `src/webservice_inference/signon_api_v2_.py` 

Finally in the directory, `src/whisper_inference` inference of [Whisper models](https://huggingface.co/openai/whisper-large-v3) are shown. For English, Spanish and Dutch language Whisper model can also be deployed via webservice. The documentation of the webservice for end-to-end and Whisper models are present in [signon-wav2vec2.cls.ru.nl/docs](https://signon-wav2vec2.cls.ru.nl/docs). 

The dependencies for each ASR inference is present in the respective directories. 

### LICENSE
This code is licensed under the Apache License, Version 2.0 (LICENSE or [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)).
