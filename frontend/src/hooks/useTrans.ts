import { useCallback } from "react";

const translations: Record<string, Record<string, string>> = {
  en: {},
};

export const useTrans = () => {
  const language = "en";
  const translate = useCallback((str: string, args: object | null = null) => {
    let translatedString = translations[language][str] || str;
    if (args) {
      for (const [key, value] of Object.entries(args)) {
        translatedString = translatedString.replace(`{${key}}`, value);
      }
    }
    return translatedString;
  }, []);
  return { t: translate };
};
