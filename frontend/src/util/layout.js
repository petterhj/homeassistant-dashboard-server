export const cssvar = (name) => {
  return getComputedStyle(document.documentElement).getPropertyValue(name);
};
