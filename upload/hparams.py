import tensorflow as tf

# Default hyperparameters:
hparams = tf.contrib.training.HParams(

  # Audio:
  num_mels=80,
  num_freq=1025,
  sample_rate=20000,    # 논문에서는 24000
  frame_length_ms=50,
  frame_shift_ms=12.5,
  preemphasis=0.97,
  min_level_db=-100,
  ref_level_db=20,

  # Model:
  outputs_per_step=5,
  len_symbols=70,
  embed_depth=256,
  prenet_depths=[256, 128],
  encoder_depth=256,
  postnet_depth=256,
  attention_depth=256,
  decoder_depth=256,

  # Training:
  batch_size=4,
  adam_beta1=0.9,
  adam_beta2=0.999,
  initial_learning_rate=0.002,  # 논문에서는 0.001
  decay_learning_rate=True,

  # Eval:
  max_iters=900,
  griffin_lim_iters=60,
  power=1.5,              # 논문에서는 1.2
)
def hparams_debug_string():
  values=hparams.values()
  hp = [' %s: %s' %(name, values[name]) for name in sorted(values)]
  return 'Hyperparameters:\n' + '\n'.join(hp)
