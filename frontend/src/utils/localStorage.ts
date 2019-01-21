export function setLocalStorage(name: string, token: string) {
  localStorage.setItem(name, token);
}

export function getLocalStorage(name: string) {
  return localStorage[name] || null;
}
