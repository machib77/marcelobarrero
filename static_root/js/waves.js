function SineWaveDrawer(options) {
  Object.assign(this, options || {});

  if (!this.el) {
    throw 'No Canvas Selected';
  }

  this.ctx = this.el.getContext('2d');

  if (!this.waves.length) {
    throw 'No waves specified';
  }

  this._resizeCanvas();
  window.addEventListener('resize', this._resizeCanvas.bind(this));

  if (typeof this.initialize === 'function') {
    this.initialize.call(this);
  }

  this.draw();
}

SineWaveDrawer.prototype.amplitude = 50;
SineWaveDrawer.prototype.wavelength = 50;
SineWaveDrawer.prototype.segmentLength = 10;
SineWaveDrawer.prototype.lineWidth = 2;
SineWaveDrawer.prototype.strokeStyle = 'rgba(228, 228, 228, 1)';

SineWaveDrawer.prototype._resizeCanvas = function () {
  this.dpr = window.devicePixelRatio || 1;
  this.width = this.el.width = this.el.offsetWidth * this.dpr;
  this.height = this.el.height = this.el.offsetHeight * this.dpr;
};

SineWaveDrawer.prototype.clear = function () {
  this.ctx.clearRect(0, 0, this.width, this.height);
};

SineWaveDrawer.prototype.draw = function () {
  const waves = this.waves;
  const drawWaveSegment = waveIndex => {
    const wave = waves[waveIndex];
    const amplitude = wave.amplitude || this.amplitude;
    const wavelength = wave.wavelength || this.wavelength;
    const lineWidth = wave.lineWidth || this.lineWidth;
    const strokeStyle = wave.strokeStyle || this.strokeStyle;
    const segmentLength = wave.segmentLength || this.segmentLength;
    const yAxis = this.height / 2;

    let x = 0;
    let y = 0;
    let startX = 0;
    let endX = segmentLength;

    const drawSegment = () => {
      if (x >= this.width) {
        x = 0;
        startX = 0;
        endX = segmentLength;
      }

      this.ctx.lineWidth = lineWidth * this.dpr;
      this.ctx.strokeStyle = strokeStyle;
      this.ctx.lineCap = 'round';
      this.ctx.lineJoin = 'round';

      this.ctx.beginPath();
      this.ctx.moveTo(
        startX,
        Math.sin(startX / wavelength) * amplitude + yAxis
      );
      for (let i = startX + 1; i <= endX; i++) {
        x = i;
        y = Math.sin(x / wavelength) * amplitude + yAxis;
        this.ctx.lineTo(x, y);
      }
      this.ctx.stroke();

      startX = endX;
      endX += segmentLength;
      requestAnimationFrame(drawSegment);
    };

    drawSegment();
  };

  for (let i = 0; i < waves.length; i++) {
    drawWaveSegment(i);
  }
};

new SineWaveDrawer({
  el: document.getElementById('waves'),
  waves: [
    {
      amplitude: 150,
      wavelength: 200,
      lineWidth: 3,
      strokeStyle: 'rgba(228, 228, 228, 1)',
    },
    {
      amplitude: 100,
      wavelength: 150,
      lineWidth: 2,
      strokeStyle: 'rgba(228, 228, 228, 1)',
    },
    {
      amplitude: -100,
      wavelength: 100,
      lineWidth: 1,
      strokeStyle: 'rgba(228, 228, 228, 1)',
    },
  ],
  initialize: function () {},
});
