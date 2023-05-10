import { useState, useRef, useCallback } from "react";
import { useFormikContext } from "formik";
import { ArrowUpTrayIcon, XMarkIcon } from "@heroicons/react/24/outline";
import FormFieldError from "./FormFieldError";

type FileUploadProps = {
  name: string;
  maxFileSizeMB: number;
  label?: string;
};

const fileTypeRegex = /(text\/plain|application\/(pdf|msword|vnd\.openxmlformats-officedocument\.wordprocessingml\.document))/;

const FileUpload = ({ name, label, maxFileSizeMB }: FileUploadProps) => {
  const [dragOver, setDragOver] = useState(false);
  const dropzoneRef = useRef<HTMLDivElement>(null);
  const [file, setFile] = useState<File | undefined>(undefined);
  const [fileError, setFileError] = useState<string | null>(null);
  const { setFieldValue } = useFormikContext();

  const resetFile = useCallback(() => {
    setFieldValue("file", undefined);
    setFile(undefined);
  }, [setFieldValue]);

  const handleOnChange = useCallback((selectedFiles: FileList | null) => {
    if (selectedFiles && selectedFiles.length > 0) {
      if (selectedFiles.length > 1) {
        setFileError("You can only upload 1 file at a time.");
        resetFile();
        return;
      }

      const file = selectedFiles[0];

      if (
        file.type.match(fileTypeRegex) && // AND file isnt too big
        file.size < maxFileSizeMB * 1024 * 1024
      ) {
        setFileError(null);
        setFieldValue("file", file);
        setFile(file);
      } else {
        setFileError(`Invalid file type or size. Only TXT, PDF or DOCX are allowed, up to ${maxFileSizeMB}MB.`);
        resetFile();
        return;
      }
    }
  }, [resetFile, setFieldValue, maxFileSizeMB]);

  const handleDragEnter = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
  }, []);

  const handleDragLeave = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    setDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      setDragOver(false);
      const droppedFiles = event.dataTransfer.files;
      handleOnChange(droppedFiles);
    },
    [handleOnChange]
  );

  return (
    <>
      {label && (
        <label
          htmlFor={name}
          className="block text-sm font-medium leading-6 text-gray-900 dark:text-white"
        >
          {label}
        </label>
      )}
      {file && (
        <div className="mt-2 flex items-center justify-between">
          <div className="text-base">
            {file.name}
          </div>
          <div className="hover:cursor-pointer p-1" onClick={resetFile}>
            <XMarkIcon className="mx-auto h-5 w-5 text-gray-400 dark:text-gray-300" aria-hidden="true" />
          </div>
        </div>
      )}
      <div 
        className={`bg-white dark:bg-white/5 mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 dark:border-zinc-700 px-6 py-10 ${dragOver ? "ring-indigo-600 bg-indigo-100" : ""}`}
        ref={dropzoneRef}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}  
      >
        <div className="text-center">
          <ArrowUpTrayIcon className="mx-auto h-12 w-12 text-gray-300 dark:text-gray-500" aria-hidden="true" />
          <div className="mt-4 flex text-sm leading-6 text-gray-600 dark:text-gray-400">
            <label
              htmlFor={name}
              className="relative cursor-pointer rounded-md bg-transparent font-semibold text-indigo-600 focus-within:outline-none hover:text-indigo-500"
            >
              <span>Upload a file</span>
              <input 
                id={name} 
                name={name} 
                type="file" 
                className="sr-only" 
                onChange={(event) => handleOnChange(event.target.files)}
              />
            </label>
            <p className="pl-1">or drag and drop</p>
          </div>
          <p className="text-xs leading-5 text-gray-600 dark:text-gray-400">PDF, DOCX or TXT up to {maxFileSizeMB}MB</p>
        </div>
      </div>
      {fileError && (<FormFieldError error={fileError} />)}
    </>
  )
}

export default FileUpload;