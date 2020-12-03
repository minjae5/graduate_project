import argparse
import falcon
from hparams import hparams, hparams_debug_string
import os
from synthesizer2 import Synthesizer

html_body = '''<html><title>Demo</title>
<style>
body {background-color:#f1bbba; padding: 16px; font-family: sans-serif; font-size: 14px; color: #444}
input {font-size: 30px; padding: 8px 12px; outline: none; border: 1px solid #ddd}
input:focus {box-shadow: 0 1px 2px rgba(0,0,0,.15)}
p {padding: 12px}
button {
  background-color: #d8e9ef;
  width: 160px;
  height: 45px;
  font-weight: bolder;
  font-size: 30px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: 500;
  color: #000;
  
  border: none;
  border-radius: 45px;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease 0s;
  cursor: pointer;
  outline: none;
  }

button:hover {
  background-color: #e85a71;
  box-shadow: 0px 15px 20px rgba(46, 229, 157, 0.4);
  color: #fff;
  transform: translateY(-7px);
}

.flex-container{ width: 100%; height: 100vh; display: -webkit-box; display: -ms-flexbox; display: flex; -webkit-box-align: center; -ms-flex-align: center; align-items: center; -webkit-box-pack: center; -ms-flex-pack: center; justify-content: center; }

.greenbox { background: #f8ecc9; text-align: center; padding: 2em; }


</style>
<body>
<div class="flex-container">
<div class="greenbox">
<form>
  <input id="text" type="text" size="40" placeholder="Enter Text">
  <button id="button" name="synthesize"><strong>Speak</strong></button>
</form>
<p id="message"></p>
<audio id="audio" controls autoplay hidden></audio>
</div>
</div>

</body>


<script>
function q(selector) {return document.querySelector(selector)}
q('#text').focus()
q('#button').addEventListener('click', function(e) {
  text = q('#text').value.trim()
  if (text) {
    q('#message').textContent = 'Synthesizing...'
    q('#button').disabled = true
    q('#audio').hidden = true
    synthesize(text)
  }
  e.preventDefault()
  return false
})
function synthesize(text) {
  fetch('/synthesize?text=' + encodeURIComponent(text), {cache: 'no-cache'})
    .then(function(res) {
      if (!res.ok) throw Error(res.statusText)
      return res.blob()
    }).then(function(blob) {
      q('#message').textContent = ''
      q('#button').disabled = false
      q('#audio').src = URL.createObjectURL(blob)
      q('#audio').hidden = false
    }).catch(function(err) {
      q('#message').textContent = 'Error: ' + err.message
      q('#button').disabled = false
    })
}
</script></body></html>
'''


class UIResource:
  def on_get(self, req, res):
    res.content_type = 'text/html'
    res.body = html_body


class SynthesisResource:
  def on_get(self, req, res):
    if not req.params.get('text'):
      raise falcon.HTTPBadRequest()
    res.data = synthesizer.synthesize(req.params.get('text'))
    res.content_type = 'audio/wav'


synthesizer = Synthesizer()
api = falcon.API()
api.add_route('/synthesize', SynthesisResource()) 
api.add_route('/', UIResource())



if __name__ == '__main__':
  from wsgiref import simple_server
  parser = argparse.ArgumentParser()
  parser.add_argument('--checkpoint', required=True, help='Full path to model checkpoint')
  parser.add_argument('--port', type=int, default=9000)
  parser.add_argument('--hparams', default='',
    help='Hyperparameter overrides as a comma-separated list of name=value pairs')
  args = parser.parse_args()
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
  hparams.parse(args.hparams)
  print(hparams_debug_string())
  synthesizer.load(args.checkpoint)
  print('Serving on port %d' % args.port)
  simple_server.make_server('', args.port, api).serve_forever()
else:
  synthesizer.load(os.environ['CHECKPOINT'])
