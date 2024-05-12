import type { IError } from "@/interfaces/errors";
import { notification } from "antd";
import type { FormInstance } from "rc-field-form";
import { useCallback } from "react";
import { useTrans } from "./useTrans";

const capitalize = (s: string) => s && s[0].toUpperCase() + s.slice(1);

export const useFormErrors = () => {
  const { t } = useTrans();

  const setFormErrors = useCallback(
    (form: FormInstance, error: IError) => {
      const errors = error?.response?.data?.detail || error?.response?.data?.description;
      if (!Array.isArray(errors)) {
        if (typeof errors === "string") {
          notification.error({
            message: t("Error"),
            description: capitalize(errors),
          });
        } else {
          notification.error({
            message: t("Error"),
            description: t(
              "Apologies for the inconvenience. Our server is currently experiencing technical difficulties. To resolve this issue, please reach out to us by email. We appreciate your understanding and patience, and our team will be happy to assist you promptly.",
            ),
            duration: 10,
          });
        }
        return;
      }

      const errorsData: Record<string, string[]> = {};
      for (const item of errors) {
        const fieldArray = item?.loc || [];
        const field = fieldArray[fieldArray.length - 1];
        if (!field || !item?.msg) {
          continue;
        }
        errorsData[field] = [capitalize(item?.msg)];
      }

      const errorsFields = Object.keys(form.getFieldsValue())
        .filter((key) => key in errorsData)
        .map((key) => ({
          name: key,
          errors: errorsData[key],
        }));

      if (errorsFields.length > 0) {
        form.setFields(errorsFields);
      }

      if (errorsData.body?.[0]) {
        notification.error({
          duration: 10,
          message: t("Error"),
          description: errorsData.body[0],
        });
      }
    },
    [t],
  );

  const cleanFormErrors = useCallback((form: FormInstance) => {
    const errorsFields = Object.keys(form.getFieldsValue()).map((key) => ({
      name: key,
      errors: [],
    }));

    form.setFields(errorsFields);
  }, []);

  return {
    setFormErrors,
    cleanFormErrors,
  };
};
