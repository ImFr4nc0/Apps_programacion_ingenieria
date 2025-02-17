{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMrd0uqBaNXKaUYH44G/tAe"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "-ZuR_eQVTtQo"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "\n",
        "# Título de la app\n",
        "st.title(\"Mi primera app\")\n",
        "\n",
        "# Autor de la app\n",
        "st.write(\"Esta app fue elaborada por COLOQUE AQUÍ SU NOMBRE.\")\n",
        "\n",
        "# Solicitar nombre del usuario\n",
        "nombre_usuario = st.text_input(\"¿Cómo te llamas?\")\n",
        "\n",
        "# Mostrar mensaje de bienvenida\n",
        "if nombre_usuario:\n",
        "    st.write(f\"{nombre_usuario}, te doy la bienvenida a mi primera app.\")\n"
      ]
    }
  ]
}