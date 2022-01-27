function unpackColorHex(colorhex) {
  console.log(colorhex);
  const figure = parseInt(colorhex.slice(1), 16)
  const ret = []
  ret.push(figure >> 16)
  ret.push((figure >> 8) & 0x00FF)
  ret.push(figure & 0x0000FF)
  return ret
}

function clampValue(value, min=0, max=255) {
  return Math.min(max, Math.max(min, value))
}

function  packColorHex(color) {
  // clamps values between 0-255 and assembles color hex
  console.log(color)
  return "#" + color.reduce((existing, value) => existing << 8 | value).toString(16);
}

export function lightenColor(colorhex, percent=20) {
  const amount = percent * 2.55;
  let color = unpackColorHex(colorhex);
  color = color.map(value => clampValue(parseInt(value + amount)));
  return packColorHex(color)
}

export function invertColor(colorhex) {
  const figure = parseInt(colorhex.slice(1), 16)
  return "#" + ((figure & 0x000000) | (~figure & 0xFFFFFF))
    .toString(16)
    .padStart(6, "0")
    .toUpperCase()
}