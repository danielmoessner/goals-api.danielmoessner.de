var SkyconsInit = require ('skycons');
const Skycons = SkyconsInit(window);


module.exports = function () {
  const icons = new Skycons({ 'color': '#ff6849' });
  const list  = [
    'clear-day',
    'clear-night',
    'partly-cloudy-day',
    'partly-cloudy-night',
    'cloudy',
    'rain',
    'sleet',
    'snow',
    'wind',
    'fog',
  ];
  let i = list.length;

  while (i--) {
    const
      weatherType = list[i],
      elements    = document.getElementsByClassName(weatherType);
    let j = elements.length;

    while (j--) {
      icons.set(elements[j], weatherType);
    }
  }

  icons.play();
}();