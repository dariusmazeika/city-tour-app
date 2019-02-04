export type LocalizationState = {
  readonly currentLanguage: string,
};

export interface ChangeLanguagePayload {
  lang: string;
}
