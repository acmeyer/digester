import React from "react";

type ErrorStateProps = {
  title: string;
  text: string;
  icon?: React.ReactNode;
};

const ErrorState = ({ title, text, icon }: ErrorStateProps) => (
  <div className="text-center">
    {icon}
    <h3 className="mt-2 text-sm font-medium">{title}</h3>
    <p className="mt-1 text-sm text-gray-500">{text}</p>
  </div>
);

export default ErrorState;
