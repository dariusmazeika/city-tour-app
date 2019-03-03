export function setToLocalStorage(name: string, token: any) {
  localStorage.setItem(name, token);
}

export function deleteFromLocalStorage(name: string) {
  return localStorage.removeItem(name);
}

export function getFromLocalStorage(name: string) {
  return localStorage.getItem(name) || null;
}
