export function setToLocalStorage(name: string, token: any) {
  localStorage.setItem(name, token);
}

export function getFromLocalStorage(name: string) {
  return localStorage.getItem(name) || null;
}
