# Informe técnico del simulador OFDM

## Resumen
Este proyecto implementa una simulación de banda base de un enlace OFDM y una interfaz local para explorar sus parámetros. El transmisor mapea bits en símbolos QAM, aplica IFFT e inserta prefijo cíclico. El canal añade ruido AWGN y, opcionalmente, multitrayecto. El receptor elimina el prefijo, aplica FFT, ecualiza y demodula. La interfaz muestra formas de onda, constelaciones y BER.

## Objetivo
Integrar y demostrar computacionalmente un sistema multiportadora OFDM, observar el efecto del ruido y del multitrayecto, y validar la recuperación de datos mediante FFT/IFFT.

## Fundamento
En OFDM los símbolos se distribuyen entre subportadoras ortogonales. Para N subportadoras y frecuencia de muestreo fs, la separación es Δf=fs/N y el tiempo útil es T=N/fs, por lo que Δf=1/T. La IFFT sintetiza las subportadoras en tiempo discreto; el receptor usa FFT. El prefijo cíclico copia muestras finales al comienzo para mitigar interferencia intersimbólica si cubre la dispersión temporal del canal.

## Arquitectura
- `src/ofdm_sim/ofdm.py`: parámetros, QAM Gray, IFFT/FFT, prefijo cíclico y ecualización.
- `channel.py`: AWGN, canal multitrayecto y respuesta frecuencial.
- `link.py`: cadena extremo a extremo y estimación BER.
- `experiments/`: adquisición, ortogonalidad, canal y curva BER.
- `app.py`: panel interactivo Streamlit que consume los módulos del paquete.

## Metodología y parámetros
Los valores interactivos iniciales son N=64, CP=16, 16-QAM, AWGN, SNR=24 dB y semilla fija. La aplicación deja cambiar N (32/64/128), CP (0–32), 4/16/64-QAM, canal, SNR, número de símbolos y semilla. Se utiliza un modelo discreto complejo de banda base; no representa un transmisor RF físico. La tasa/eficiencia reportada se calcula según las ecuaciones del paquete y no incluye pilotos, codificación ni sobrecarga de trama.

## Validación
El repositorio incluye pruebas con pytest para muestreo, transformadas, modulación, ortogonalidad, canal y enlace. Ejecución: `pytest -q`. Experimentos completos: `python run_all.py --quick` o `python run_all.py`. La BER es errores de bits divididos por bits transmitidos. Para comparaciones científicas, conserve la semilla y reporte cantidad de símbolos y canales por punto SNR.

## Resultados e interpretación
La aplicación calcula las métricas al pulsar Transmitir y recibir; no se consignan cifras fijas aquí porque dependen de los parámetros elegidos. En general, al subir SNR se espera reducir BER. El multitrayecto distorsiona de forma dependiente de frecuencia; el prefijo cíclico permite aproximar cada subportadora por una ganancia compleja cuando su duración es suficiente y la sincronización es ideal. El zero-forcing puede amplificar ruido en subportadoras con respuesta pequeña.

## Limitaciones
Modelo sincronizado de banda base; sin CFO, ruido de fase, estimación práctica de canal, pilotos, codificación de canal, AGC ni hardware. El ecualizador supone conocer la respuesta del canal. Las métricas son simuladas y no mediciones de radio. El resultado texto se deja como extensión; la demo actual transmite tramas de bits aleatorios.

## Conclusión
El código integra la cadena OFDM y permite observar interactivamente cómo modulación, canal, SNR y prefijo cíclico se relacionan con la recepción y la BER. Las extensiones más valiosas serían estimación de canal con pilotos, sincronización y transmisión de texto con manejo de longitud/CRC.
