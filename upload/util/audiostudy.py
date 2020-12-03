import librosa  

import librosa.filters
import math
import numpy as np #파이썬 수학대표적으로 배열이 존재 
import tensorflow as tf
import scipy
from hparams import hparams

# _stft_파라미터 설정 .
def _stft_parameters():
  n_fft = (hparams.num_freq -1) * 2 #기본 설정 num_freq=1025
  hop_length = int(hparams.frame_shift_ms / 1000 * hparams.sample_rate)
  #frame_shift_ms= 12.5 sample_rate = 20000 
  win_length = int(hparams.frame_length_ms / 1000* hparams.sample_rate)
  return n_fft, hop_length, win_length 

#preprocess
def load_wav(path):
  return librosa.core.load(path, sr=hparams.sample_rate)

#preemph~ IIR 필터 설정 
#stft  파라미터 값 설정후 librosa.stft 함수 매개변수에 대입해주는 함수.
#return은 입력된 y값을 필터로 거른뒤 stft함수에 넣어주고 이를 dB단위로 변환하고
#일반화를 통해 0~1값만 남게 한다. 
def spectrogram(y):
  D= _stft(_preemphasis(y))
  S= _amp_to_db(np.abs(D))- hparams.ref_level_db #ref_level_db=20
  return _normalize(S)

def melspectrogram(y):
  D=_stft(_preemphasis(y))
  S=_amp_to_db(_linear_to_mel(np.abs(D))) - hparams.ref_level_db
  return _normalize(S)

# stft 함수의 파라미터를 설정해주는 stftpara 함수를 포함,이용하여 
# 해당 파라미터 값들을 librosa.stft함수 속 매개변수로 넣어주는 함수.
def _stft(y):
 n_fft, hop_length, win_length=_stft_parameters()
 return librosa.stft(y=y, n_fft=n_fft, hop_length=hop_length, win_length=win_length) 

#IIR filter  구현.. 수학이다. s
#scipy.singal.lfilter(b,a,x,asix,zi) b= 분자 다항식 차수 a= 분모 다항식 차수
#x= signal ,axis = 행렬 , zi= 기본 모델 
def _preemphasis(x):
  return scipy.signal.lfilter([1, -hparams.preemphasis], [1], x)
#hparams.preemphasis =0.97


#전력간 계산이 편한 단위인 dB 단위로 변환하는 함수. 
def _amp_to_db(x):
  return 20*np.log10(np.maximum(1e-5, x))

#np.clip()
#np.clip(배열,최소값기준,최대값 기준, out배열)
# 설정된 최대,최소값을 넘는 배열속의 원소들은 각,최소 최대값으로 변환됨
# array =[-2,-1,0,5] 일때 최소 0 최대 4로 지정하면 -2,-1 은 0으로 5는 4로 변환
#  out=a 까지 값을 준다면 a라는 이름으로 변환된 값이 기록된 배열 저장.
#즉 이 함수는 결과가 0~1만 나온다는 것.
def _normalize(S):
  return np.clip((S - hparams.min_level_db) / -hparams.min_level_db ,0,1)

#np.dot는 행렬간 곱을 수행하는 함수이다.
#멜스펙토그램을 만든 함수와 스펙토그램을 곱하는 함수이다.
def _linear_to_mel(spectrogram):
  _mel_basis= _build_mel_basis()
  return np.dot(_mel_basis, spectrogram)

#멜스펙토그램 기본설정
def _build_mel_basis():
  n_fft = (hparams.num_freq -1)*2
  return librosa.filters.mel(hparams.sample_rate, n_fft, n_mels=hparams.num_mels)

# train
def inv_spectrogram(spectrogram):
    S= _db_to_amp(_denormalize(spetrogram) + hparams.ref_level_db)
    return inv_preemphasis(_griffin_lim(S ** hparams.power))


def _db_to_amp(x):
    return np.power(10.0, x*0.05) #np.power (a,b) a를 b제곱 
def _denormalize(S):
    return (np.clip(S,0,1)* -hparams.min_level_db) + hparams.min_level_db
    #(S 값을 0~1 값으로 일반화)* -(음성 최소 데시벨)+ 음성 최소 데시벨
    #(음성 다듬는 역할으로 추정)
def inv_preemphasis(x):
    return scipy.signal.lfilter([1], [1, -hparams.preemphasis]. x)

def _griffin_lim(S):
  angles = np.exp(2j * np.pi * np.random.rand(*S.shape))
  S_complex = np.abs(S).astype(np.complex)
  y = _istft(S_complex * angles)
  for i in range(hparams.griffin_lim_iters):
    angles = np.exp(1j * np.angle(_stft(y)))
    y = _istft(S_complex * angles)
  return y

def _istft(y):
  _, hop_length, win_length = _stft_parameters()
  return librosa.istft(y, hop_length=hop_length, win_length=win_length)

