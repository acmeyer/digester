/* eslint-disable no-nested-ternary */
import LoadingSpinner from "@/components/LoadingSpinner";

type LoadingContainerProps = {
  additionalClasses?: string;
  size: "small" | "medium" | "large";
};

const LoadingContainer = ({ size, additionalClasses }: LoadingContainerProps) => (
  <div
    className={`${
      size === "small" ? "h-6" : size === "medium" ? "h-20" : "h-96"
    } ${additionalClasses}`}
  >
    <div
      className={`${
        size === "small" ? "py-1" : "py-10"
      } loading-container flex min-h-full justify-center items-center`}
    >
      <LoadingSpinner size={size} />
    </div>
  </div>
);

export default LoadingContainer;
