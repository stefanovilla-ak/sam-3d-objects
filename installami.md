# COME INSTALLARE sam-3d-objects

### sudo password for stefano 
```
stefano
```

### installare python3.10 se non esiste

```
sudo apt update
sudo apt install -y software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

sudo apt install -y python3.10 python3.10-venv python3.10-dev
```

## 1. COME INSTALLARE dal repo originale facebookresearch/sam-3d-objects



```
git clone https://github.com/facebookresearch/sam-3d-objects.git
cd sam-3d-objects
```


### **MODIFICARE IL FILE 'requirements.p3d.txt'**
commentare la prima riga:
```
pytorch3d @ git+https://github.com/facebookresearch/pytorch3d.git@75ebeeaea0908c5527e7b1e305fbc7681382db47
flash_attn==2.8.3
```
diventa:
```
# pytorch3d @ git+https://github.com/facebookresearch/pytorch3d.git@75ebeeaea0908c5527e7b1e305fbc7681382db47
flash_attn==2.8.3
```

### **MODIFICA requirements.txt**
commenta linea con 'bpy==4.3.0'
```
bpy==4.3.0
```
diventa:
```
#bpy==4.3.0
```

### **MODIFICA environments/default.yml**
commenta linea che dichiara la versione di python
```
  - python=3.11...
```
diventa:
```
  - python=3.10
```

### installare conda se mancante


```
conda env create -f environments/default.yml
```

attivare l'environment
```
conda activate sam3d-objects
```
per disattvarlo
```
conda deactivate
```




### 3. RIMUOVI flash-attn-triton se è stato installato dall'environment file
```
pip uninstall flash-attn-triton -y
```
### 4. Installa PyTorch 2.5.1 con CUDA 12.1 (sovrascrive eventuali versioni dall'env file)
```
pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 --index-url https://download.pytorch.org/whl/cu121
```

### Installa build tools
```
pip install setuptools wheel cython numpy
```

### Clona gsplat e installa
```
git clone https://github.com/nerfstudio-project/gsplat.git
cd gsplat
git checkout 2323de5905d5e90e035f792fe65bad0fedd413e7

cd gsplat/cuda/csrc/third_party/
git clone https://github.com/g-truc/glm.git
cd ../../../../
pip install .
cd ..
```



### 4.1. Installa xformers 0.0.28.post3 (richiesto da sam3d-objects)
```
pip install xformers==0.0.28.post3
```


### 5. Installa dipendenze per compilare flash-attn
```
pip install ninja packaging wheel
```


### 6. Installa flash-attn (quello GIUSTO, non flash-attn-triton)
```
pip install flash-attn==2.8.3 --no-build-isolation
```

### 7. Installa il progetto in modalità development
```
pip install -e '.[dev]'
```

### 8. VERIFICA FINALE - rimuovi flash-attn-triton se è rispuntato
```
pip uninstall flash-attn-triton -y
```

### 9. Test che tutto funzioni
```
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
python -c "import flash_attn; print(f'FlashAttention: {flash_attn.__version__}')"
```
### 10. installa pytorch3d
```
pip install wrapt
pip install --no-build-isolation "git+https://github.com/facebookresearch/pytorch3d.git@75ebeeaea0908c5527e7b1e305fbc7681382db47"
```

### 13. Ora reinstalla il progetto
```
pip install -e '.[p3d]'

export PIP_FIND_LINKS="https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.5.1_cu121.html"
pip install -e '.[inference]'
```
### 14.installa hugginface
```
pip install 'huggingface-hub[cli]<1.0'
```
### 15.loggarsi su hugginface per il download
```
huggingface-cli login
```

### 16. infine effettaure il downlaod dei modelli
```
TAG=hf
hf download --repo-type model --local-dir checkpoints/${TAG}-download --max-workers 1 facebook/sam-3d-objects
mv checkpoints/${TAG}-download/checkpoints checkpoints/${TAG}
rm -rf checkpoints/${TAG}-download
```
