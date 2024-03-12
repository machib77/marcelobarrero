document.addEventListener('DOMContentLoaded', function () {
  // CANDLESTICK
  const canvas = document.getElementById('candlestick');
  const ctx = canvas.getContext('2d');

  const commonY = 400; // Set a common y value for all candles

  const UP_COLOR = '#7a7d7e'; // Green
  const DOWN_COLOR = '#6b6d6e'; // Red

  function generateRandomWalk(
    numCandles,
    min = 0,
    max = 400,
    stdDeviation,
    minCandleHeight = 100
  ) {
    const candles = [];
    let prevClose = 200;

    for (let i = 0; i < numCandles; i++) {
      // Add some drift towards 200
      const drift = (200 - prevClose) * 0.1;

      const randomChange = stdDeviation * (Math.random() - 0.5);
      let newClose = prevClose + randomChange + drift;

      // Ensure the newClose stays within the min and max bounds
      newClose = Math.max(min, Math.min(max, newClose));

      // Ensure the candle height is at least minCandleHeight (absolute value)
      let candleHeight = Math.abs(newClose - prevClose);
      if (candleHeight < minCandleHeight) {
        if (newClose > prevClose) {
          newClose = prevClose + minCandleHeight;
        } else {
          newClose = prevClose - minCandleHeight;
        }
      }

      candles.push({ openPrice: prevClose, closePrice: newClose });
      prevClose = newClose;
    }

    return candles;
  }

  // Example usage
  const numCandles = 100;
  const minPrice = 250;
  const maxPrice = 400;
  const stdDev = 300;
  const minCandleHeight = 60;

  const candles = generateRandomWalk(
    numCandles,
    minPrice,
    maxPrice,
    stdDev,
    minCandleHeight
  );

  console.log(candles);

  const candlestickWidth = 20;
  const candlestickGap = 5; // Smaller gap between candles
  const animationDuration = 50; // In milliseconds

  let currentCandleIndex = 0;
  let animationStartTime = null;

  // Calculate total width needed for all candles
  const totalCandlesWidth =
    (candlestickWidth + candlestickGap) * candles.length;

  // Start the candles from the left side of the canvas
  const startX = 0;

  // Animation loop
  function animate(timestamp) {
    if (!animationStartTime) {
      animationStartTime = timestamp;
    }

    const elapsed = timestamp - animationStartTime;
    const progress = Math.min(elapsed / animationDuration, 1);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < candles.length; i++) {
      const candle = candles[i];

      // Calculate x position for the candle
      const x = startX + i * (candlestickWidth + candlestickGap);

      const y = commonY;
      const height = Math.abs(candle.closePrice - candle.openPrice);

      // Determine color based on openPrice and closePrice
      const candleColor =
        candle.closePrice > candle.openPrice ? UP_COLOR : DOWN_COLOR;

      if (i <= currentCandleIndex) {
        // Draw completed or current animating candle
        const candleHeight = Math.abs(candle.closePrice - candle.openPrice);
        const currentCandleStartY =
          candle.closePrice > candle.openPrice
            ? y - candle.openPrice
            : y - candle.closePrice;
        const currentCandleEndY =
          candle.closePrice > candle.openPrice
            ? y - candle.closePrice
            : y - candle.openPrice;
        const currentCandleAnimHeight =
          i === currentCandleIndex ? progress * candleHeight : candleHeight;

        ctx.fillStyle = candleColor;
        ctx.fillRect(
          x,
          candle.closePrice > candle.openPrice
            ? currentCandleStartY - currentCandleAnimHeight
            : currentCandleEndY,
          candlestickWidth,
          currentCandleAnimHeight
        );
      }
    }

    if (progress === 1) {
      currentCandleIndex++;

      if (currentCandleIndex >= candles.length) {
        // Animation complete, draw the final state
        drawFinalState();
        return; // Stop the animation loop
      }

      // Reset animation start time for the next candle
      animationStartTime = null;
    }

    requestAnimationFrame(animate);
  }

  // Draw the final state of the chart
  function drawFinalState() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < candles.length; i++) {
      const candle = candles[i];

      // Calculate x position for the candle
      const x = startX + i * (candlestickWidth + candlestickGap);

      const y = commonY;
      const height = Math.abs(candle.closePrice - candle.openPrice);

      // Determine color based on openPrice and closePrice
      const candleColor =
        candle.closePrice > candle.openPrice ? UP_COLOR : DOWN_COLOR;

      ctx.fillStyle = candleColor;
      ctx.fillRect(
        x,
        candle.closePrice > candle.openPrice
          ? y - candle.closePrice
          : y - candle.openPrice,
        candlestickWidth,
        height
      );
    }
  }

  // Start the animation loop
  animate();

  // Get a reference to the .marquee element
  const marquee = document.getElementById('name-marquee');

  // Function to set canvas dimensions to match marquee
  function setCanvasSize() {
    // Get the computed width and height of the marquee
    const marqueeWidth = marquee.offsetWidth;
    const marqueeHeight = marquee.offsetHeight;

    // Set the canvas width and height to match the marquee
    canvas.width = marqueeWidth * 0.7;
    canvas.height = marqueeHeight * 0.5;
  }

  // Call the function once to set initial dimensions
  setCanvasSize();

  // Optionally, add an event listener to resize if the window is resized
  window.addEventListener('resize', setCanvasSize);
});
