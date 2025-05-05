#!/bin/bash

# Atualiza os pacotes e instala o Tesseract OCR
apt-get update && apt-get install -y tesseract-ocr

# (opcional) Adiciona suporte a idiomas extras, se necessário
# apt-get install -y tesseract-ocr-por tesseract-ocr-eng

# Garante permissões corretas e local do binário no PATH
which tesseract
