import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from ofdm_sim.ofdm import OFDMParams,qam_modulate,qam_demodulate,ofdm_modulate,ofdm_demodulate,equalize
from ofdm_sim.channel import awgn,example_channel,awgn_channel,multipath,frequency_response
from ofdm_sim.link import ber_curve,qam_ber_awgn
st.set_page_config(page_title='Simulador OFDM',page_icon='📡',layout='wide')
st.title('Simulador educativo de un enlace OFDM')
st.caption('Transmisor · canal · receptor · métricas reproducibles')
st.markdown('OFDM divide los datos entre subportadoras ortogonales. La IFFT genera la señal temporal y la FFT permite recuperar los símbolos en el receptor.')
with st.sidebar:
 st.header('Configuración')
 mod=st.selectbox('Modulación QAM',[4,16,64],index=1,format_func=lambda x:f'{x}-QAM')
 n=st.selectbox('Subportadoras (N)',[32,64,128],index=1)
 cp=st.slider('Prefijo cíclico (muestras)',0,32,16)
 chan=st.selectbox('Canal',['AWGN','Multitrayecto + AWGN'])
 snr=st.slider('SNR (dB)',0,36,24,step=3)
 count=st.slider('Símbolos OFDM',5,200,30,step=5)
 seed=st.number_input('Semilla aleatoria',min_value=0,max_value=999999,value=42)
 run=st.button('Transmitir y recibir',type='primary')
params=OFDMParams(n_fft=n,cp_len=cp,mod_order=mod)
st.info(f"Separación subportadoras Δf = {params.subcarrier_spacing/1e3:.2f} kHz · Duración útil T = {params.useful_duration*1e6:.2f} μs · Eficiencia CP = {params.cp_efficiency*100:.1f}%")
if run:
 rng=np.random.default_rng(seed); bits=rng.integers(0,2,count*params.bits_per_ofdm_symbol)
 grid=qam_modulate(bits,mod).reshape(count,n); tx=ofdm_modulate(grid,params,True)
 h=awgn_channel() if chan=='AWGN' else example_channel()
 clean=multipath(tx,h); rx=awgn(clean,snr,rng,signal_power=np.mean(np.abs(tx)**2))
 rg=ofdm_demodulate(rx,params,True); eq=equalize(rg,frequency_response(h,n)); out=qam_demodulate(eq.reshape(-1),mod)[:len(bits)]
 errors=int(np.count_nonzero(bits!=out)); ber=errors/len(bits)
 c1,c2,c3=st.columns(3); c1.metric('Bits transmitidos',len(bits)); c2.metric('Errores',errors); c3.metric('BER',f'{ber:.4g}')
 tabs=st.tabs(['Transmisor','Canal','Receptor','Curva BER'])
 with tabs[0]:
  st.write('Bits → QAM → IFFT → prefijo cíclico'); fig,ax=plt.subplots(1,2,figsize=(10,3)); ax[0].plot(np.real(tx[:min(250,len(tx))])); ax[0].set_title('Señal OFDM, componente real'); ax[0].set_xlabel('Muestra'); ax[1].scatter(grid[0].real,grid[0].imag,s=12); ax[1].set_title('Constelación transmitida'); ax[1].set_xlabel('I'); ax[1].set_ylabel('Q'); st.pyplot(fig); plt.close(fig)
 with tabs[1]:
  st.write(f'Canal: {chan}; SNR configurada: {snr} dB.'); fig,ax=plt.subplots(1,2,figsize=(10,3)); ax[0].stem(np.arange(len(h)),np.abs(h)); ax[0].set_title('Respuesta impulsional |h[n]|'); ax[1].plot(np.real(rx[:min(250,len(rx))])); ax[1].set_title('Señal recibida, componente real'); st.pyplot(fig); plt.close(fig)
 with tabs[2]:
  st.write('Eliminar CP → FFT → ecualizar → demodular'); st.write(f'BER = {errors}/{len(bits)} = {ber:.6g}'); fig,ax=plt.subplots(1,2,figsize=(10,3)); ax[0].scatter(rg.real,rg.imag,s=10); ax[0].set_title('Antes de ecualizar'); ax[1].scatter(eq.real,eq.imag,s=10); ax[1].set_title('Después de ecualizar'); st.pyplot(fig); plt.close(fig)
 with tabs[3]:
  if st.button('Calcular curva (puede tardar)'):
   snrs=np.arange(0,37,6); fn=(lambda r:awgn_channel()) if chan=='AWGN' else (lambda r:example_channel()); vals=ber_curve(params,snrs,fn,True,np.random.default_rng(seed),trials=8,n_ofdm=30); fig,ax=plt.subplots(); ax.semilogy(snrs,np.maximum(vals,1e-6),'o-',label='Simulación'); ax.set(xlabel='SNR (dB)',ylabel='BER',title=f'BER frente a SNR · {mod}-QAM'); ax.grid(True,which='both'); ax.legend(); st.pyplot(fig); plt.close(fig)
