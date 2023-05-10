'use client'

import { Formik, Form, Field, ErrorMessage, FormikHelpers } from "formik"
import * as Yup from "yup";
import TextInput from "./TextInput";
import FileUpload from "./FileUpload";
import FormFieldError from "./FormFieldError";
import LoadingOverlay from "./LoadingOverlay";
import axios from "axios";
import { useRouter } from 'next/navigation';
import { SERVER_ADDRESS } from "@/lib/constants";

type FormValues = {
  url: string;
  file: File | undefined;
};

const SummaryRequestSchema = Yup.object().shape({
  url: Yup.string().url("URL must be a valid URL.").when(
    "file",
    {
      is: (file: File | undefined) => file === undefined,
      then: (schema) => schema.required("URL or File is required."),
    }
  ),
  file: Yup.mixed().nullable()
});

const initialSummaryRequestValues: FormValues = {
  url: "",
  file: undefined,
}

const GetSummaryForm = () => {
  const router = useRouter();

  const onSubmit = async (
    values: FormValues,
    { setSubmitting, resetForm }: FormikHelpers<FormValues>
  ) => {
    try {
      const formData = new FormData();
      formData.append('url', values.url);
      if (values.file) {
        formData.append('file', values.file);
      }

      const response = await axios.post(
        `${SERVER_ADDRESS}/summarize`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (
        response.status === 200 &&
        response.data
      ) {
        const data = response.data;
        // Redirect to the summary page
        router.push(`/summaries/${data.item.id}`);
      } else {
        console.error("Error processing file", response);
      }
      setSubmitting(false);
      resetForm();
    } catch (error) {
      alert(error);
      setSubmitting(false);
    }
  };

  return (
    <Formik
      initialValues={initialSummaryRequestValues}
      validationSchema={SummaryRequestSchema}
      onSubmit={onSubmit}
    >
      {({ isSubmitting }) => (
        <div className="pt-3">
          <LoadingOverlay isVisible={isSubmitting} />
          <Form>
            <div className="mt-4 grid grid-cols-1 gap-x-4 gap-y-6">
              <div className="col-span-full">
                <Field
                  as={TextInput}
                  id="url"
                  name="url"
                  label="URL"
                />
                <ErrorMessage
                  name="url"
                  render={(error) => <FormFieldError error={error} />}
                />
              </div>
              <div className="col-span-full">
                <Field
                  as={FileUpload}
                  id="file"
                  name="file"
                  label="File"
                  maxFileSizeMB={25}
                />
              </div>
            </div>
            <div className="mt-6 flex items-center justify-end gap-x-4">
              <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
                {isSubmitting ? "Generating a Summary..." : "Get a Summary"}
              </button>
            </div>
          </Form>
        </div>
      )}
    </Formik>
  )
}

export default GetSummaryForm;