# Simulador de un sistema OFDM

Aplicación interactiva para observar la transmisión y recepción de señales OFDM en banda base. Permite modificar los parámetros del sistema y analizar el efecto del ruido y del multitrayecto sobre la señal recibida.

## Requisitos

- Python 3.10 o superior
- Conexión a Internet para instalar las dependencias

No se requiere hardware de radio. El canal y la transmisión se modelan en software.

## Instalación y ejecución en Windows

1. Descargue el repositorio y abra esta carpeta en Visual Studio Code o el Explorador de archivos.
2. Ejecute `Iniciar_OFDM.bat`. El iniciador crea el entorno virtual si hace falta, instala las dependencias y abre la aplicación.
3. Streamlit mostrará una dirección local, normalmente `http://localhost:8501`. Ábrala en el navegador y mantenga la ventana de terminal abierta mientras usa la aplicación.

También se puede iniciar desde una terminal en esta carpeta:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

Para detener la aplicación, presione `Ctrl+C` en la terminal.

## Uso

En el panel de configuración seleccione el orden QAM, el número de subportadoras, el prefijo cíclico, el canal, la SNR, la cantidad de símbolos y la semilla aleatoria. Pulse **Transmitir y recibir** para ejecutar el enlace. Las pestañas muestran las señales y constelaciones de transmisión, canal y recepción, además de las métricas calculadas. La vista **Curva BER** compara la tasa de error de bit para varios valores de SNR.

La BER corresponde al número de bits errados dividido por el total de bits transmitidos. La semilla fija permite repetir una configuración. Los valores son resultados de simulación y pueden variar al cambiar los parámetros.

## Pruebas y experimentos

Con las dependencias instaladas, desde la carpeta del proyecto ejecute:

```powershell
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe run_all.py --quick
```

Los experimentos generan figuras en `results/`. Para ejecutar el barrido completo, use `run_all.py` sin `--quick`.

## Estructura

- `app.py`: interfaz interactiva.
- `src/ofdm_sim/`: implementación de OFDM, canal, transformadas y enlace.
- `experiments/`: experimentos reproducibles.
- `tests/`: pruebas automatizadas.
- `results/`: figuras de salida.
- `docs/informe_tecnico.md`: descripción del modelo, metodología y limitaciones.

## Modelo y limitaciones

La simulación considera banda base compleja y sincronización ideal. La ecualización supone conocida la respuesta del canal. No se modelan transmisión RF, pilotos, codificación de canal ni errores de sincronización. En la interfaz, la transmisión y la curva BER se calculan con prefijo cíclico activado.
